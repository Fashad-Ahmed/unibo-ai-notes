---> If every operator (node) has same cost in BFS then it is optimal solution otherwise not.
---> DFS : time complexity: exponential, Space complexity: exponential, always complete, optional as all operators have the same cost.
----> NO guarentte that BFS can find the optimal path
-----> Fringe is FIFO-Queue


<img width="1478" height="826" alt="image" src="https://github.com/user-attachments/assets/2341f466-4675-4202-abe0-3d3a62fa89fe" />



This response updates the study notes to include specific details regarding the Time Complexity of non-informed search strategies, as requested.

# Study Notes: AI Search and Non-Informed Strategies (Updated)

## I. Fundamentals of AI Search

Many Artificial Intelligence (AI) problems are solved by exploring the **solution space**, which contains all possible sequences of actions an agent might apply. The search process involves examining alternative sequences of actions that lead to known states and then choosing the best one.

*   **Search Tree:** Search is often visualized as building a search tree where **nodes are states** and **branches are operators/actions**. The tree represents the expansion of all states starting from the initial state (the root).
*   **Search Strategy:** The method used at each step to choose which state to expand.
*   **Execution:** Once the solution (a sequence of actions) is found, the suggested actions can be performed.

### A. Defining a Problem

A problem is typically defined by four points: the **Initial state** (e.g., "at Arad"), the **Successor functions $S(x)$** (set of action-state pairs), the **Test goal** (explicit, e.g., $x = \text{"At Bucharest"}$, or implicit, e.g., $\text{checkmap}(x)$), and the **Cost of the path $c(x, a, y) \geq 0$** (e.g., distance travelled or number of actions/hops performed).

### B. Node Implementation

Each node in the search tree corresponds to a data structure containing the **state**, the **parent node**, the **operator** used to obtain the node, the **depth** of the node, and the **cost of the path** from the initial state to the node.

## II. Evaluating Search Strategies

Strategies are assessed according to four criteria:

*   **Completeness:** Does the strategy guarantee finding a solution if one exists?
*   **Optimality:** Does the strategy find the best solution when multiple solutions exist? (measured by the minimum path solution, the on-line cost).
*   **Time complexity:** **How long does it take to find a solution?** (the off-line cost).
*   **Space complexity:** How much memory is needed to carry out the search?.

The **Total cost** of a search is the sum of the search path cost and the cost of the search.

### Diagram 1: Key Complexity Definitions

| Parameter | Definition |
| :--- | :--- |
| **$b$** | Maximum of the search tree **branching factor**. |
| **$d$** | The **depth of the least-cost solution**. |
| **$m$** | Maximum depth of the state space (which may be infinite). |
| **$l$** | Depth limit (used in Limited Depth Search). |

---

## III. Non-Informed Search Strategies

**Non-informed strategies** perform an **exhaustive search** without using any domain knowledge.

### A. Breadth-First Search (BFS)

BFS always **expands the less deep tree nodes** first.

*   **Implementation:** The fringe is a **FIFO queue**; successors are added to the end of the queue (at the bottom).
*   **Optimality:** Always finds the **minimum-cost path** if the cost equals the depth.
*   **Completeness:** This strategy ensures completeness.
*   **Disadvantage:** The main problem is the **excessive memory footprint**.

### B. Uniform-Cost Search (UCS)

UCS is preferred over BFS when operators have **non-uniform costs**. It always expands the **least cost node** (labeled with cost $g(n)$).

*   **Completeness:** It is comprehensive.

### C. Depth-First Search (DFS)

DFS **expands the deepest nodes first**; nodes at equal depth are arbitrarily selected (e.g., leftmost).

*   **Implementation:** The fringe is a **LIFO stack**; successors are entered to the top of the stack. It is efficient from an implementation viewpoint because only one path is stored at a time.
*   **Memory:** Requires a **modest memory occupation**; $b \times d$ nodes must be stored for a maximum search depth $d$ and branching factor $b$.
*   **Completeness:** Can be **non-complete** if infinite branches or loops are present in the state space.

### D. Limited Depth Search (LDS)

LDS is a depth-first variant that includes a **maximum depth parameter ($l$)** to avoid infinite branches. When the maximum depth is reached, or a failure occurs, it explores alternative paths (backtracking).

### E. Iterative Deepening Search (IDS)

IDS avoids the problem of choosing a fixed maximum depth limit by trying all possible depth limits sequentially (starting $L=0, 1, 2, ...$).

*   **Advantages:** It is generally the **favourite search strategy** when the search space is very large. It combines the advantages of depth and breadth-first strategies, is **complete**, and explores a single branch at a time.
*   **Operation:** It can emulate the breadth-first search by repeatedly applying depth-first search with an increasing depth limit.

---

## IV. Time Complexity Analysis

### Diagram 2: Time Complexity (Maximum Nodes Expanded)

| Strategy | Worst-Case Time Complexity (Maximum Nodes Expanded) | Notes |
| :--- | :--- | :--- |
| **Breadth-First Search (BFS)** | $\mathbf{O(b^d)}$ | In the worst case, the maximum number of nodes expanded will be $b^d$. The complexity is derived from $1 + b + b^2 + b^3 + \dots + (b^d - 1)$, which is approximated to $b^d$. |
| **Uniform-Cost Search (UCS)** | **Similar to BFS** | UCS shares the same **temporal** (and spatial) complexity as breadth-first search. |
| **Depth-First Search (DFS)** | $\mathbf{O(b^d)}$ | The temporal complexity is rather similar to that of breadth-first search. In the worst case, the maximum number of nodes expanded is $b^d$. |
| **Iterative Deepening Search (IDS)** | $\mathbf{(d+1)1 + (d)b + (d-1)b^2 + \dots + 3b^{d-2} + 2b^{d-1} + b^d}$ | This formula describes the total number of expansions. Although many states are expanded multiple times, this does not worsen the execution time considerably. |

---

## V. Production Systems and Reasoning Modes

**Production Systems** are programs that perform search methods on problems represented as a state space.

### Diagram 3: Production System Components

| Component | Description |
| :--- | :--- |
| **Set of Rules (Operators)** | Typically in the form `IF <pattern> THEN <body>`. They are activated based on **pattern-matching**, not invoked by name. |
| **Working Memory** | Contains the current achieved states or initial knowledge. |
| **Control Strategy (Interpreter/Controller)** | Selects rules, performs **Matching**, **Selection**, and **Execution**, verifies preconditions, and tests the state goal. |

### Diagram 4: Reasoning Modes

| Mode | Driver | Rule Selection Criteria | Success Condition |
| :--- | :--- | :--- | :--- |
| **FORWARD (Data-Driven)** | Known facts / initial knowledge. | Rules whose **antecedent** matches the working memory (F-rules). | The goal to prove is inserted into the working memory. |
| **BACKWARD (Goal-Driven)** | Goals (or goal) of the problem. | Rules whose **consequent** matches the working memory (B-rules). | The initial state appears in the working memory. |
| **TWO-WAY (Mixed)** | Combination of F-rules and B-rules applied simultaneously. | N/A | Termination is achieved when the portion of the working memory created by backward chaining is equal to or a subset of the one obtained by forward chaining. |

