
### **1. The Complexity Hierarchy ($\mathbf{P}$ vs $\mathbf{NP}$ vs $\mathbf{EXP}$)**

* **The Golden Chain:** $\mathbf{P} \subseteq \mathbf{NP} \subseteq \mathbf{EXP}$. If a problem is in $\mathbf{P}$, it is automatically in $\mathbf{NP}$ and $\mathbf{EXP}$.
* **The Time Hierarchy Theorem (Proven):** $\mathbf{P} \subsetneq \mathbf{EXP}$. Polynomial time is strictly smaller than exponential time. They will never be equal.
* **The Unproven Gap:** It is assumed, but *not mathematically proven*, that $\mathbf{P} \neq \mathbf{NP}$. Therefore, an option saying "EXP is a subset of NP" ($\mathbf{EXP} \subseteq \mathbf{NP}$) cannot currently be proven false.
* **NP-Complete Facts:** * To be NP-Complete, a problem must be in **NP** AND be **NP-Hard**.
* If a problem is NP-Complete (like 3SAT or CLIQUE), it is *guaranteed* to be in $\mathbf{EXP}$ (solvable by brute force).
* *Every* problem in $\mathbf{NP}$ can be reduced to an NP-Complete problem in polynomial time ($A \le_p \text{3SAT}$).



### **2. Turing Machine Rules & Traps**

* **Tapes and Class $\mathbf{P}$:** The number of tapes does **NOT** change the class $\mathbf{P}$. A 100-tape machine can be simulated on a 1-tape machine with at most a quadratic slowdown ($\mathcal{O}(t(n)^2)$). Squaring a polynomial is still a polynomial.
* **Tapes and Strict Time Limits:** The number of tapes **DOES** change strict deterministic time bounds like $\text{DTIME}(n)$.
* *Palindrome Example:* 2-tape TM solves it in linear time $\mathcal{O}(n)$. 1-tape TM solves it in quadratic time $\mathcal{O}(n^2)$ because of back-and-forth head movement.


* **Time Bounds are Ceilings:** If a TM works in time $\mathcal{O}(n^2)$, it is mathematically true that it also works in time $\mathcal{O}(n^3)$. It just finishes early.
* **Nondeterminism:** Nondeterministic TMs do not have more absolute computing power (they compute the exact same set of decidable languages as deterministic TMs), they just compute some things much faster.

### **3. Asymptotic Notation (Growth Rates)**

* **Big-O ($\mathcal{O}$):** The Upper Bound ($\le$). $f \in \mathcal{O}(g)$ means $f$ grows *no faster* than $g$.
* **Big-Omega ($\Omega$):** The Lower Bound ($\ge$). $f \in \Omega(g)$ means $f$ grows *at least as fast* as $g$.
* **Big-Theta ($\Theta$):** The Exact Match ($=$). $f \in \Theta(g)$ means they grow at the same rate.
* *Cheat Code for Limits:* Constants ($10^5$, $10^{-5}$) are invisible in asymptotic math. Exponentials ($2^n$) crush polynomials ($n^2$). Polynomials crush polylogarithms ($\log^2 n$).

### **4. Computational Learning Theory**

* **PAC Learning Sample Complexity:** To guarantee an error less than $\varepsilon$ with probability $1 - \delta$, you need $m \ge \frac{4}{\varepsilon} \ln \frac{4}{\delta}$ samples.
* **Hardness of Learning:** Efficiently finding a consistent Boolean formula for training data is **NP-Hard** (proven by reduction from 3-Coloring). Therefore, Boolean formulas are not efficiently PAC learnable unless $\mathbf{RP} = \mathbf{NP}$.
* **VC-Dimension:** The maximum number of points a hypothesis class can perfectly "shatter" (classify every possible $+/-$ combination).
* *Union of 2 intervals:* $VC = 4$.
* *Triangles:* $VC = 7$.
* *Parity Functions on strings of length $d$:* $VC = d$ (because any $d+1$ vectors in a $d$-dimensional space are linearly dependent).



**Golden Rule for MCQs:** If a question says "Suppose $\mathcal{L}$ is in $\mathbf{NP}$ and $\mathbf{EXP}$", remember the "and EXP" part is a trick. Everything in NP is already in EXP! Read carefully for traps like that. You've got this, bro.
