from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .heap import BinaryHeap
from .process import Process


@dataclass
class ScheduleResult:
    timeline: List[str]                 # pid per tick (or "IDLE")
    completion_times: Dict[str, int]
    waiting_times: Dict[str, int]
    average_waiting_time: float


class PriorityAgingScheduler:
    """
    Preemptive priority scheduler with aging.
    Smaller priority value = higher priority.

    Aging approach:
      effective_priority = max(1, base_priority - floor(waited / aging_interval))
    This avoids O(n) heap updates each interval: we reinsert only when needed.
    """

    def __init__(self, aging_interval: int = 10):
        if aging_interval <= 0:
            raise ValueError("aging_interval must be > 0")
        self.aging_interval = aging_interval

    def run(self, processes: List[Process], max_time: Optional[int] = None) -> ScheduleResult:
        if not processes:
            return ScheduleResult([], {}, {}, 0.0)

        # Sort by arrival for efficient intake
        procs = sorted(processes, key=lambda p: (p.arrival, p.base_priority, p.pid))
        n_total = len(procs)

        ready = BinaryHeap()
        clock = 0
        idx = 0
        current: Optional[Process] = None
        timeline: List[str] = []
        completed = 0

        # For waiting time computation
        first_seen: Dict[str, int] = {p.pid: p.arrival for p in procs}
        executed_ticks: Dict[str, int] = {p.pid: 0 for p in procs}

        def eff_priority(p: Process, now: int) -> int:
            waited = max(0, now - p.last_enqueued)
            boost = waited // self.aging_interval
            return max(1, p.base_priority - boost)

        while completed < n_total:
            # Stop if max_time set (safety for infinite loops)
            if max_time is not None and clock >= max_time:
                break

            # Enqueue arrivals at this clock
            while idx < n_total and procs[idx].arrival == clock:
                p = procs[idx]
                p.last_enqueued = clock
                ready.insert(p.pid, p, priority=(p.base_priority, p.arrival, 0))

                idx += 1

            # Decide if need to pick a process
            if current is None and not ready.is_empty():
                p = ready.extract_min()
                if p.start_time is None:
                    p.start_time = clock
                current = p

            # Preemption check: compare effective priorities
            if current is not None and not ready.is_empty():
                # refresh effective priority of head candidate (approx):
                # We pop-and-reinsert if aging changed a lot; keep simple + correct.
                cand = ready.extract_min()
                cand_eff = eff_priority(cand, clock)
                ready.insert(cand.pid, cand, priority=(cand_eff, cand.arrival, 0))

                cur_eff = eff_priority(current, clock)

                top_eff, top_arrival, _ = ready.peek_min_priority()
                # preempt if someone is strictly higher priority
                if top_eff < cur_eff:
                    # requeue current with updated effective priority
                    current.last_enqueued = clock
                    ready.insert(current.pid, current, priority=(cur_eff, current.arrival, 0))

                    current = ready.extract_min()
                    if current.start_time is None:
                        current.start_time = clock

            # Execute 1 tick
            if current is None:
                timeline.append("IDLE")
                clock += 1
                continue

            timeline.append(current.pid)
            current.remaining -= 1
            executed_ticks[current.pid] += 1

            if current.remaining <= 0:
                current.completion_time = clock + 1
                completed += 1
                current = None

            clock += 1

        completion_times: Dict[str, int] = {}
        waiting_times: Dict[str, int] = {}
        for p in procs:
            if p.completion_time is None:
                continue
            completion_times[p.pid] = p.completion_time
            turnaround = p.completion_time - p.arrival
            waiting = turnaround - p.burst
            waiting_times[p.pid] = waiting

        avg_wait = (sum(waiting_times.values()) / len(waiting_times)) if waiting_times else 0.0
        return ScheduleResult(
            timeline=timeline,
            completion_times=completion_times,
            waiting_times=waiting_times,
            average_waiting_time=avg_wait,
        )
