from __future__ import annotations

import heapq
from typing import Any, Dict, List, Tuple

_REMOVED = object()


class BinaryHeap:
    """
    Priority queue with lazy deletion.
    Uses a hashable key (e.g., process pid) to track entries.
    """

    def __init__(self) -> None:
        self._heap: List[list] = []
        self._entry_finder: Dict[str, list] = {}
        self._counter: int = 0

    def __len__(self) -> int:
        return len(self._entry_finder)

    def is_empty(self) -> bool:
        return len(self._entry_finder) == 0

    def insert(self, key: str, item: Any, priority: Tuple[int, int, int]) -> None:
        """
        Insert/update an item.
        key: unique identifier (e.g., process pid)
        priority: tuple for ordering
        """
        if key in self._entry_finder:
            self.remove(key)
        entry = [priority, self._counter, key, item]
        self._entry_finder[key] = entry
        heapq.heappush(self._heap, entry)
        self._counter += 1

    def remove(self, key: str) -> None:
        entry = self._entry_finder.pop(key)
        entry[3] = _REMOVED  # mark item removed

    def extract_min(self) -> Any:
        while self._heap:
            priority, count, key, item = heapq.heappop(self._heap)
            if item is not _REMOVED:
                del self._entry_finder[key]
                return item
        raise KeyError("Empty heap")

    def peek_min_priority(self) -> Tuple[int, int, int]:
        while self._heap:
            priority, count, key, item = self._heap[0]
            if item is _REMOVED:
                heapq.heappop(self._heap)
                continue
            return priority
        raise KeyError("Empty heap")
