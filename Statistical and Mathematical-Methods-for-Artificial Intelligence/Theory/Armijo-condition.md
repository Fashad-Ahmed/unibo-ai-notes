Below is a **GitHub-supported Markdown** version of the explanation.
You can **copy-paste this directly into a `.md` file** and all equations will render correctly on GitHub.

---

# Backtracking Line Search & Armijo Condition (Easy Explanation)

---

## Big Picture

**Backtracking line search** is a method to automatically choose the step size in Gradient Descent so that **each step decreases the loss by a meaningful amount**.

Instead of fixing the step size in advance, we **start with a large step** and **shrink it until it works**.

---

## The Problem It Solves

In Gradient Descent, we update the parameters as:

$$
\theta^{(k+1)} = \theta^{(k)} - \eta_k g^{(k)}
$$

where:

$$
g^{(k)} = \nabla L(\theta^{(k)})
$$

The key question is:

> How large should the step size ( \eta_k ) be?

* Too large → overshoot, loss may increase
* Too small → very slow convergence

Backtracking line search finds a **safe and effective step size automatically**.

---

## Core Idea (In Simple Words)

1. Start with an initial step size ( \bar{\eta} )
2. Try taking a step in the gradient direction
3. Check if the loss decreases **enough**
4. If not, shrink the step size and try again
5. Repeat until the decrease is satisfactory

---

## Armijo Condition

The step size ( \eta_k ) is accepted only if:

$$
L(\theta^{(k)} - \eta_k g^{(k)})
;\le;
L(\theta^{(k)}) - c , \eta_k |g^{(k)}|^2
$$

where:

* ( g^{(k)} = \nabla L(\theta^{(k)}) )
* ( c \in (0,1) ) is a small constant

---

## What the Inequality Means

### Left-hand side

$$
L(\theta^{(k)} - \eta_k g^{(k)})
$$

The loss **after** taking the step.

---

### Right-hand side

$$
L(\theta^{(k)}) - c , \eta_k |g^{(k)}|^2
$$

The loss **before** the step minus a **minimum required decrease**.

---

### Interpretation

> The new loss must be **smaller than the old loss by at least a certain amount**.

This prevents accepting steps that only reduce the loss by a negligible amount.

---

## Meaning of Each Parameter

### Gradient Norm ( |g^{(k)}|^2 )

* Measures how steep the loss is
* Large gradient → expect large decrease
* Small gradient → expect small decrease

This makes the condition scale naturally.

---

### Constant ( c \in (0,1) )

* Controls how strict the condition is
* Typical values: ( c = 0.01 ) or ( c = 0.1 )

Smaller ( c ) → easier to satisfy
Larger ( c ) → stricter requirement

---

### Shrinking Factor ( \beta \in (0,1) )

When the condition is not satisfied, the step size is reduced:

$$
\eta_k \leftarrow \beta \eta_k
$$

Typical values: ( \beta = 0.5 ) or ( \beta = 0.8 )

---

## Backtracking Line Search Algorithm

For iteration ( k ):

1. Initialize:
   $$
   \eta_k = \bar{\eta}
   $$

2. While the Armijo condition is **not satisfied**:
   $$
   L(\theta^{(k)} - \eta_k g^{(k)}) >
   L(\theta^{(k)}) - c , \eta_k |g^{(k)}|^2
   $$

3. Shrink the step size:
   $$
   \eta_k \leftarrow \beta \eta_k
   $$

4. Accept ( \eta_k ) and update:
   $$
   \theta^{(k+1)} = \theta^{(k)} - \eta_k g^{(k)}
   $$

---

## Intuition (Real-Life Analogy)

Imagine walking downhill:

* You first try a **big step**
* If you slip or don’t go down enough, the step is too big
* You take **smaller steps** until the descent is safe and effective

The Armijo condition checks:

> “Did this step take me downhill enough?”

---

## Why This Method Is Useful

* Prevents overshooting
* Avoids useless tiny steps
* Automatically adapts to the shape of the loss function
* Works for both convex and non-convex optimization problems

---

## Exam-Ready Summary

> Backtracking line search is a technique to select the step size in gradient descent by starting from an initial value and repeatedly shrinking it until the Armijo condition is satisfied. The Armijo condition ensures that each step produces a sufficient decrease in the loss proportional to the gradient norm, preventing both overly large and overly small steps.

---

Below is a **clear mathematical explanation** of **why the Armijo condition guarantees descent**, written in an **exam-friendly, paper-and-pen style**.
You can also copy this into GitHub Markdown if you want — equations will render.

---

# Why the Armijo Condition Guarantees Descent (Mathematical Explanation)

---

## Goal

We want to show that **when the Armijo condition holds, the loss function decreases**, i.e.

[
L(\theta^{(k+1)}) < L(\theta^{(k)})
]

---

## Setup

Gradient Descent update:

[
\theta^{(k+1)} = \theta^{(k)} - \eta_k g^{(k)},
\quad
g^{(k)} = \nabla L(\theta^{(k)})
]

Armijo condition:

[
L(\theta^{(k)} - \eta_k g^{(k)})
;\le;
L(\theta^{(k)}) - c,\eta_k |g^{(k)}|^2,
\quad c \in (0,1)
]

---

## Step 1: First-order Taylor approximation

For a differentiable function (L), the first-order Taylor expansion around (\theta^{(k)}) gives:

[
L(\theta^{(k)} - \eta_k g^{(k)})
\approx
L(\theta^{(k)}) - \eta_k \langle \nabla L(\theta^{(k)}), g^{(k)} \rangle
]

Since ( g^{(k)} = \nabla L(\theta^{(k)}) ), this becomes:

[
L(\theta^{(k)} - \eta_k g^{(k)})
\approx
L(\theta^{(k)}) - \eta_k |g^{(k)}|^2
]

---

## Step 2: Meaning of the approximation

* The term ( -\eta_k |g^{(k)}|^2 ) is **strictly negative** if:

  * ( \eta_k > 0 )
  * ( g^{(k)} \neq 0 )

So for **small enough step sizes**, moving in the **negative gradient direction always decreases the loss**.

This is the fundamental descent property of gradient descent.

---

## Step 3: Why we need Armijo (real functions are not linear)

The Taylor approximation is **only approximate**.

* For large ( \eta_k ), higher-order terms matter
* The actual loss decrease may be **less than predicted**
* The loss might even increase

So we enforce a **conservative lower bound** on the decrease.

---

## Step 4: Armijo enforces sufficient decrease

Armijo requires:

[
L(\theta^{(k+1)})
;\le;
L(\theta^{(k)}) - c,\eta_k |g^{(k)}|^2
]

where ( 0 < c < 1 ).

This means:

* We accept only a **fraction (c)** of the ideal (linear) decrease
* The decrease is **strictly positive** whenever ( g^{(k)} \neq 0 )

Since:
[
c,\eta_k |g^{(k)}|^2 > 0
]

we get:

[
L(\theta^{(k+1)}) < L(\theta^{(k)})
]

✅ **Strict descent is guaranteed**

---

## Step 5: Why backtracking always finds such a step

For sufficiently small ( \eta_k ):

* Higher-order terms become negligible
* Taylor approximation becomes accurate
* Armijo inequality is satisfied

Backtracking line search:
[
\eta_k \leftarrow \beta \eta_k, \quad \beta \in (0,1)
]

guarantees that we will **eventually reach a small enough step size**.

---

## Key Mathematical Insight (Exam Gold)

> The negative gradient is a descent direction, and the Armijo condition enforces that the step size is small enough so that the actual decrease in the function value is proportional to the squared gradient norm.

---

## One-Paragraph Exam Answer (Memorize)

> The Armijo condition guarantees descent by enforcing a sufficient decrease in the objective function proportional to the squared gradient norm. Since the negative gradient is a descent direction, for sufficiently small step sizes the loss decreases according to the first-order Taylor approximation. Backtracking line search ensures that the step size is reduced until higher-order effects are negligible, guaranteeing a strict decrease in the objective value at each accepted iteration.

---
