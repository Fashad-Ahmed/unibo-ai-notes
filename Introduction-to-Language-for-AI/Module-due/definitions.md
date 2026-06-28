These terms are the absolute core of mathematical logic. They all deal with one fundamental question: **Do these statements contain a logical contradiction?**

In many logic courses, "Satisfiable" and "Consistent" mean the exact same thing when talking about a group of formulas, but they are used in slightly different contexts. Here is the breakdown:

### 1. Satisfiable (Usually applied to a single formula)

A formula is **satisfiable** if it is *possible* for it to be True.
It means there is at least one specific scenario (interpretation) where the math works out. It doesn't have to be True all the time; it just has to be True at least once.

* **Example:** $A \land B$
* **Why:** It is satisfiable because if you assign $A = \text{True}$ and $B = \text{True}$, the statement works.

### 2. Consistent (Usually applied to a *group* of formulas)

A set of statements is **consistent** if they do not contradict each other.
It means it is possible for **all** the statements in the group to be True at the exact same time. If a set of formulas is consistent, we say the set is *satisfiable*.

* **Example Set:** $\{A \rightarrow B, \quad A = \text{True}, \quad B = \text{True}\}$
* **Why:** These statements are consistent. They "agree" with each other. There is no mathematical clash.

### 3. Inconsistent (Unsatisfiable)

A set of statements is **inconsistent** if it contains a fatal contradiction.
It means it is mathematically **impossible** for all the statements to be True at the same time. If you assume they are all True, you will be forced to make a variable both True and False simultaneously.

* **Example Set:** $\{A \rightarrow B, \quad A = \text{True}, \quad B = \text{False}\}$
* **Why:** The first rule ($A \rightarrow B$) says that if $A$ is True, $B$ *must* be True. But the third statement explicitly says $B$ is False. This is a direct contradiction. The system is inconsistent (and therefore unsatisfiable).

---

### The Exam Cheat Sheet

Here is a quick reference table for how these terms relate to each other when evaluating your truth tables or proofs:

| Term | What it means in plain English | Truth Table Result |
| --- | --- | --- |
| **Valid (Tautology)** | Impossible to be False. | Evaluates to **True in ALL** rows. |
| **Satisfiable / Consistent** | Possible to be True. | Evaluates to **True in AT LEAST ONE** row. |
| **Unsatisfiable / Inconsistent** | Impossible to be True. | Evaluates to **False in ALL** rows. |