This problem is a classic application of graph theory known as the **Maximum Independent Set** problem.

### Problem Formalization

1. **Vertices ():** The set of all candidate invitees .
2. **Edges ():** The set of incompatible pairs .
3. **Goal:** Find the largest subset  such that no two vertices in  are connected by an edge in .

### Complexity and Solvability

* **Computational Class:** This is an **NP-hard** optimization problem.
* **Decision Version:** Determining if there is an invitee list of size  is **NP-complete**.
* **Implication:** For a small number of candidates, you can solve this using exact algorithms (like backtracking or branch-and-bound). However, as the number of potential guests () grows, finding the absolute maximum becomes computationally "impossible" to solve quickly with a standard computer.

### Practical Solutions

While finding the *perfect* maximum is hard, you can use several strategies:

* **Heuristics:** Use a "Greedy" approach—repeatedly invite the person with the fewest conflicts, remove them and their neighbors from the list, and repeat.
* **Approximation:** For certain graph structures (like if your friends only form simple social circles without complex overlaps), the problem becomes much easier (polynomial time).
* **Integer Linear Programming (ILP):** Modern solvers can often find the optimal solution for hundreds or even thousands of guests in a reasonable timeframe.

