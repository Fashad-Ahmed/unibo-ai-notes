
### **The Undecidable & $\mathbf{NP}$-Hard Language**

This question tests your understanding of the absolute limits of computation.

* **"There cannot be any nondeterministic Turing machine deciding $\mathcal{L}$" (Correct):** Decidability is a hard mathematical boundary. If a problem is undecidable, it means *no computing model in existence* can reliably solve it and halt. Nondeterministic Turing Machines (NTMs) do not possess more absolute computing power than standard deterministic machines; they compute the exact same set of decidable languages, they just do it faster. If a problem is undecidable, an NTM cannot decide it either.
* **"The language $\mathcal{L}$ is strictly harder to decide than SAT" (Correct):** SAT is the foundational $\mathbf{NP}$-Complete problem. Because it lives inside $\mathbf{NP}$, it is 100% **decidable** (you can easily write an algorithm to brute-force a truth table in exponential time, and it is guaranteed to halt with an answer). $\mathcal{L}$, on the other hand, is undecidable, meaning no algorithm will ever be guaranteed to halt. An unsolvable problem is strictly harder than a solvable one.
* *(Why the other two are wrong):* We already know $\mathbf{P}$ and $\mathbf{NP}$ only deal with *decidable* problems. Introducing an undecidable language tells us absolutely nothing about whether $\mathbf{P}$ and $\mathbf{NP}$ are equal or different.

---

### **PAC Learning Axis-Aligned Squares**

This question connects geometric VC-dimension to computational efficiency.

* **"PAC learnable" (Correct):** According to the Fundamental Theorem of PAC Learning, a concept class is PAC learnable if and only if it has a finite VC-dimension. The VC-dimension of axis-aligned squares in $\mathbb{R}^2$ is exactly 3 (you can shatter 3 points, but not 4). Because 3 is a finite number, the class is mathematically guaranteed to be PAC learnable.
* **"Efficiently PAC learnable" (Correct):** "Efficiently" means that the algorithm to find a consistent hypothesis runs in polynomial time. For axis-aligned squares, the algorithm is incredibly simple and fast: just scan the training data and draw the tightest possible square that encloses all the positive examples. This takes linear time ($\mathcal{O}(n)$). Because both the sample complexity (amount of data needed) and the computational complexity (time to process the data) are bounded by polynomials, it is efficiently PAC learnable.
* *(Why both are checked):* If something is *efficiently* PAC learnable, it automatically means it is PAC learnable. You have to check both boxes to be fully correct!


---


A problem is classified as **$\mathbf{NP}$-hard** when it acts as a "universal bottleneck" for the entire complexity class $\mathbf{NP}$.

Here is the exact mathematical definition and what it actually means.

### **The Formal Definition**

A problem $H$ is $\mathbf{NP}$-hard if **every single problem** $L$ in the class $\mathbf{NP}$ can be reduced to $H$ in polynomial time.

Mathematically, this is written as:


$$\forall L \in \mathbf{NP}, L \le_p H$$

### **The Intuition (What this actually means)**

If a problem is $\mathbf{NP}$-hard, it means it is **at least as hard as the hardest problems in $\mathbf{NP}$**.

Think of an $\mathbf{NP}$-hard problem as a master key. Because *every* problem in $\mathbf{NP}$ can be quickly (in polynomial time) transformed into this $\mathbf{NP}$-hard problem, finding a fast polynomial-time algorithm to solve the $\mathbf{NP}$-hard problem would instantly give you a fast algorithm to solve every single problem in $\mathbf{NP}$. It would prove that $\mathbf{P} = \mathbf{NP}$.

### **How to Prove a Problem is $\mathbf{NP}$-Hard**

If you discover a new problem and want to prove it is $\mathbf{NP}$-hard, you don't actually sit down and write a reduction for every single problem in $\mathbf{NP}$ (that would take infinite time).

Instead, you use transitivity. You take **one known $\mathbf{NP}$-hard problem** (like 3SAT or the Traveling Salesperson Problem) and prove that you can reduce *it* to your new problem in polynomial time.

* "If I can turn 3SAT into my problem, and 3SAT is already known to be a bottleneck for all of $\mathbf{NP}$, then my problem is also a bottleneck for all of $\mathbf{NP}$."

### **$\mathbf{NP}$-Hard vs. $\mathbf{NP}$-Complete**

People often mix these two up, but there is a massive difference:

* **$\mathbf{NP}$-Complete:** The problem must be $\mathbf{NP}$-hard **AND** it must live inside $\mathbf{NP}$ (meaning its solutions can be verified in polynomial time).
* **$\mathbf{NP}$-Hard:** There is no upper limit on how hard the problem can be. It does **not** have to be in $\mathbf{NP}$. An $\mathbf{NP}$-hard problem could require exponential time, or it could even be completely **undecidable** (like the Halting Problem).

In short: $\mathbf{NP}$-hard means "at least this hard, but possibly way harder or even impossible."


--- 



### **Question 1: Asymptotic Bounds of $f$ and $g$**

**Correct Answer: $f \in \Omega(g)$**

**Explanation:**
You are comparing $f(n) = n^2 2^n$ against $g(n) = n 2^n$.
If you cancel out the shared $2^n$ term, you are basically comparing $n^2$ to $n$. Because a quadratic ($n^2$) grows strictly faster than a linear function ($n$), $f(n)$ completely outpaces $g(n)$ as $n$ goes to infinity.
Therefore, $g(n)$ acts as a lower bound for $f(n)$, which is the definition of Big-Omega ($\Omega$). It is not $\mathcal{O}$ or $\Theta$ because $g$ cannot upper-bound $f$.

---

### **Question 2: In Turing Machines**

**Correct Answers:**

* **The presence of many tapes can make the class $\mathbf{DTIME}(n)$ different.**
* **What can be computed in exponential time is different from what can be computed in polynomial time.**

**Explanation:**

* **$\mathbf{DTIME}(n)$ is tape-dependent:** Simulating a 2-tape machine on a 1-tape machine introduces a quadratic slowdown. So, a problem that takes strict linear time $\mathcal{O}(n)$ on a multi-tape machine might take $\mathcal{O}(n^2)$ on a single-tape machine, pushing it outside of $\mathbf{DTIME}(n)$.
* **Polynomial vs Exponential:** The second checked option is the literal definition of the **Time Hierarchy Theorem**, which mathematically proves $\mathbf{P} \subsetneq \mathbf{EXP}$.
* *(Why the others are false):* The class $\mathbf{P}$ is robust; a polynomial squared is still a polynomial, so tapes don't break $\mathbf{P}$. And $\mathbf{EXP}$ can *never* equal $\mathbf{P}$ due to the Time Hierarchy Theorem.

---

### **Question 3: The problem 3SAT is**

**Correct Answers:**

* **such that INDSET can be reduced to it, i.e., INDSET $\le_p$ 3SAT**
* **$\mathbf{NP}$-hard**
* **In the class $\mathbf{EXP}$**

**Explanation:**
3SAT is the textbook definition of an **$\mathbf{NP}$-Complete** problem.

* Because it is $\mathbf{NP}$-Complete, it is by definition **$\mathbf{NP}$-hard**.
* Because it is a universal bottleneck for $\mathbf{NP}$, *every* problem in $\mathbf{NP}$ (including INDSET / Independent Set) can be reduced to it in polynomial time.
* Finally, *every* problem in $\mathbf{NP}$ is automatically in **$\mathbf{EXP}$** because you can always just brute-force the verification process in exponential time.

---

### **Question 4: Suppose a language $\mathcal{L}$ is both in $\mathbf{NP}$ and in $\mathbf{EXP}$**

**Correct Answers:**

* **$\mathcal{L}$ can even be $\mathbf{NP}$-complete**
* **The classes $\mathbf{EXP}$ and $\mathbf{NP}$ are maybe different.**

**Explanation:**
This question starts with a slight trick: *Everything* in $\mathbf{NP}$ is already in $\mathbf{EXP}$. Therefore, the premise just means "Suppose $\mathcal{L}$ is in $\mathbf{NP}$".

* Could it be $\mathbf{NP}$-Complete? Absolutely. 3SAT is in $\mathbf{NP}$ (and thus in $\mathbf{EXP}$) and is $\mathbf{NP}$-Complete.
* Are $\mathbf{EXP}$ and $\mathbf{NP}$ different? We know $\mathbf{NP} \subseteq \mathbf{EXP}$, and it is widely believed that they are not equal, so saying they are "maybe different" is a perfectly valid theoretical statement.
* *(Why the others are false):* It *could* be in $\mathbf{P}$ (since $\mathbf{P}$ is inside $\mathbf{NP}$). And $\mathbf{EXP}$ and $\mathbf{NP}$ are certainly not *necessarily* equal.

---

### **Question 5: The notion of PAC-learnable concept class**

**Correct Answers:**

* **Needs to hold for every distribution $\mathbf{D}$ on the instance class.**
* **Does not make any reference to the time complexity of the learning algorithm**

**Explanation:**
This is the exact same question you saw earlier, just with the options shuffled!

* Standard PAC learnability is "distribution-free," meaning the bounds must hold no matter how the data is distributed in reality.
* Pure PAC learnability only deals with *sample complexity* (how much data is needed). It completely ignores *time complexity* (how long the algorithm takes to run). If you care about time, you have to specify *Efficiently* PAC-learnable.


------



Here is the breakdown of the correct answers for each question along with the theoretical explanations for why.

---

### **Question 1: Encoding sets as binary strings**

**Correct Answer:**

* **The set of pairs of rational numbers, i.e., $\mathbb{Q} \times \mathbb{Q}$.**

**Explanation:**
To encode a set into finite binary strings, the set must be **countable** (finite or countably infinite).

* The set of rational numbers ($\mathbb{Q}$) is countably infinite. The Cartesian product of two countable sets ($\mathbb{Q} \times \mathbb{Q}$) remains countable, meaning you can systematically assign a unique binary string to every pair.
* The real numbers ($\mathbb{R}$) and complex numbers ($\mathbb{C}$) are **uncountable**. The infinity of these sets is too large to map uniquely to finite binary strings.

---

### **Question 2: Checking Turing Machine states**

**Correct Answers:**

* **In the class $\mathbf{NP}$**
* **Decidable in exponential time**

**Explanation:**
This is a test of your ability to distinguish between *syntactic* and *semantic* properties.

* **Semantic properties** (what the machine actually computes/does) are subject to Rice's Theorem and are usually Undecidable.
* **Syntactic properties** (the physical code/structure of the machine) are easy to check. Counting the number of states is purely syntactic. You just look at the string encoding of the Turing machines and count the states listed in their transition functions.
Because this just requires reading a string, it can be done extremely fast in deterministic polynomial time ($\mathbf{P}$).
Since it is in $\mathbf{P}$, it is automatically also in $\mathbf{NP}$ and also decidable in exponential time ($\mathbf{EXP}$), due to the hierarchy $\mathbf{P} \subseteq \mathbf{NP} \subseteq \mathbf{EXP}$.

---

### **Question 3: Inclusions compatible with current knowledge**

**Correct Answers:**

* **$\mathbf{NP} \subseteq \mathbf{NPC}$**
* **$\mathbf{P} \supseteq \mathbf{NPC}$**

**Explanation:**
This question asks what *could* be true because we haven't proven it false yet.

* **$\mathbf{NP} \subseteq \mathbf{NPC}$ and $\mathbf{P} \supseteq \mathbf{NPC}$:** Both of these statements are mathematically equivalent to saying $\mathbf{P} = \mathbf{NP}$. Because no one has proven whether $\mathbf{P}$ equals $\mathbf{NP}$ or not, these statements are compatible with our current (incomplete) knowledge.
* *(Why the others are wrong):* The Time Hierarchy Theorem mathematically proves that $\mathbf{P} \subsetneq \mathbf{EXP}$ (they cannot be equal). The Space Hierarchy Theorem proves that $\mathbf{L} \subsetneq \mathbf{PSPACE}$. Those two options are definitively false.

---

### **Question 4: SAT algorithm in polynomial space**

**Correct Answers:**

* **Your friend's algorithm might be correct, but one has of course to check the details.**
* **Even if your friend is correct, SAT would stay $\mathbf{NP}$-complete.**

**Explanation:**
It is already a well-known mathematical fact that SAT can be solved in polynomial space ($\mathbf{PSPACE}$). A standard brute-force algorithm testing all $2^n$ truth assignments only needs to keep track of the current assignment in memory, which takes linear space $\mathcal{O}(n)$.

* Because we already know SAT is in $\mathbf{PSPACE}$, a friend claiming to have a poly-space algorithm is completely unremarkable. It doesn't break complexity theory, nor does it prove $\mathbf{P} = \mathbf{NP}$ (which requires polynomial *time*, not space). SAT firmly remains $\mathbf{NP}$-complete regardless of this space discovery.

---

### **Question 5: Representation class of closed intervals in $\mathbb{R}$**

**Correct Answers:**

* **Is efficiently PAC-learnable.**
* **Has VC-dimension equal to 2**

**Explanation:**

* **VC-dimension is 2:** A single interval can easily shatter 2 points (you can include neither, just the left, just the right, or both). However, it cannot shatter 3 points. If you have points $x_1 < x_2 < x_3$ and you want to classify $x_1$ and $x_3$ as positive but $x_2$ as negative, a single continuous interval physically cannot bridge $x_1$ and $x_3$ without trapping $x_2$ inside.
* **Efficiently PAC-learnable:** Because the VC-dimension is finite (2), the Fundamental Theorem of PAC Learning guarantees it is learnable. Because you can find the target interval just by scanning the training data for the minimum and maximum positive values—which takes linear time $\mathcal{O}(n)$—it is *efficiently* PAC-learnable.
