# Applied Algorithms and Data Structures (502IT)

## Individual Technical Portfolio

This repository contains my **individual portfolio submission** for the *Applied Algorithms and Data Structures (502IT)* module. The project demonstrates the practical application of core algorithmic concepts through the design, implementation, testing, and evaluation of three distinct computational systems. The work emphasises algorithm selection, data structure efficiency, complexity analysis, and reflective practice, in line with academic portfolio requirements.

---

## Project Overview

The portfolio focuses on solving three real-world inspired problems using appropriate algorithms and data structures:

1. **Delivery Route Optimisation**
   A heuristic solution to the Travelling Salesperson Problem (TSP) using the Nearest Neighbour algorithm combined with 2-opt local search optimisation.

2. **Dynamic Resource Allocation**
   A preemptive, priority-based CPU scheduling system implemented using a binary heap, including an aging mechanism to prevent starvation.

3. **Recommendation Engine for a Bookstore**
   A user–user collaborative filtering recommendation system using Jaccard similarity and an inverted index for scalability.

Each problem is implemented independently using Python and object-oriented design principles, with supporting tests and performance evaluation.

---

## Technologies and Concepts

* Python 3
* Graph algorithms
* Greedy heuristics and local search (2-opt)
* Priority queues and heap data structures
* Scheduling algorithms
* Collaborative filtering
* Similarity metrics (Jaccard)
* Algorithmic time and space complexity analysis
* Unit and performance testing (pytest)

---

## Repository Structure

The repository is organised into logical modules reflecting each problem domain:

* `src/routing/` – Graph representation and TSP solver
* `src/scheduling/` – Process model, binary heap, and priority scheduler
* `src/recommendation/` – Recommendation engine, similarity functions, and data structures
* `src/utils/` – Benchmarking and visualisation utilities
* `tests/` – Unit tests for each major component
* `tools/` – Optional scripts for dataset generation and running recommendations
* `main.py` – Demonstration script that runs all three systems

---

## How to Run the Project

### Install Dependencies

First, install the required Python libraries:

```
pip install -r requirements.txt
```

### Run the Full Demonstration

To execute all three components (TSP, scheduler, and recommendation engine), run:

```
python main.py
```

This will:

* Generate and solve a TSP instance and save visualisations
* Simulate the priority-based scheduler and print execution statistics
* Run the recommendation engine and display recommended books for a sample user

---

## Running Tests

Unit tests are provided to validate correctness of each subsystem. To run all tests:

```
pytest
```

To include test coverage:

```
pytest --cov=src
```

---

## Recommendation Engine (Detailed Explanation)

The recommendation engine uses a **user–user collaborative filtering** approach:

1. An inverted index maps each book to the users who have purchased it.
2. For a target user, only users sharing at least one book are considered as candidates.
3. Jaccard similarity is calculated between the target user and each candidate user.
4. Books not yet purchased by the target user are scored using weighted ratings:
   similarity × rating.
5. The top-k books with the highest scores are returned as recommendations.

This design significantly reduces unnecessary similarity calculations and improves scalability.

---

## Academic Context

This repository serves as:

* An assessed **individual technical portfolio**
* Evidence of applied algorithmic engineering
* A demonstration of translating theoretical concepts into working systems
* A record of reflective and professional software development practice

All implementations were manually written, tested, and evaluated. Any AI tools used were limited to research assistance or suggestion review and are documented separately in the portfolio submission.

---

## Author

**[Waseeq Ahmed]**
Student ID: **[15146137]**
Module: Applied Algorithms and Data Structures (502IT)
