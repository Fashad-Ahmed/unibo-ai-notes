Why do we use levels = np.logspace(-1, 3, ncontours) for Rosenbrock?
Short answer (exam style)

We use log-spaced contour levels because the Rosenbrock function’s values change over several orders of magnitude, especially near the narrow valley.
Logarithmic spacing lets us see both large-scale structure and fine details near the minimum in the same plot.

1. What is the problem with linear contour levels?

If we use something like:

levels = np.linspace(min_L, max_L, ncontours)


then:

Most contour lines concentrate in high-value regions

Near the minimum (1,1), contours are:

either extremely dense

or completely invisible

The narrow curved valley is poorly visualized

This happens because Rosenbrock values vary a lot:

Far from minimum: L(θ) ≈ hundreds or thousands

Near minimum: L(θ) ≈ 0

A single linear scale cannot represent both well.

2. Why Rosenbrock needs logarithmic spacing

The Rosenbrock function is:

L(θ1, θ2) = (1 − θ1)^2 + 100 (θ2 − θ1^2)^2


Key properties:

Very steep walls (large curvature)

Very flat valley floor

Function values span multiple orders of magnitude

Example values:

Far away from valley → L ≈ 10^2 – 10^3
Near the minimum     → L ≈ 10^-2 – 10^-6


Linear contours cannot handle this range well.

3. What does np.logspace(-1, 3, ncontours) do?
levels = np.logspace(-1, 3, ncontours)


This means:

10^-1, 10^0, 10^1, 10^2, 10^3


So contour lines are placed at:

small values → many contours near the minimum

large values → fewer contours far away

This gives a balanced visualization.

4. What improves visually when using log-spaced levels?

Using logarithmic levels:

Reveals the curved valley shape

Makes zig-zagging trajectories visible

Shows how GD:

first enters the valley

then slowly progresses along it

Prevents contour plots from being:

overly dense

or completely washed out

This is why your friend’s plots look cleaner and less cluttered.

5. Why this is standard practice (important for exams)

Log-spaced contours are commonly used for:

Rosenbrock function

Ill-conditioned optimization problems

Loss landscapes with steep + flat regions

In optimization lectures, this choice is intentional, not cosmetic.

6. One-line exam justification (memorize this)

We use logarithmic contour levels for the Rosenbrock function because its loss values span several orders of magnitude, and log spacing allows us to visualize both the narrow valley near the minimum and the steep outer regions simultaneously.

7. When NOT to use log-spaced contours

Simple quadratic functions

Well-conditioned problems

When loss values lie in a narrow numeric range

In those cases, linear spacing is fine.

Final takeaway

Rosenbrock ≠ normal function








----------------------------------------------------------------



---

# Exercise 5 — Observations and Explanation

**Gradient Descent on the Rosenbrock Function**

We analyze the behavior of Gradient Descent (GD) on the Rosenbrock function

```
L(θ1, θ2) = (1 − θ1)^2 + 100 (θ2 − θ1^2)^2
```

for multiple initial points and using:

* constant step sizes η ∈ {1e−3, 1e−4, 1e−5}
* backtracking line search (Armijo)

The global minimum is at:

```
θ* = (1, 1),   L(θ*) = 0
```

---

## 1. Does the method enter the valley?

### Constant step size GD

* For **η = 1e−3**
  The method often **enters the valley quickly**, but may overshoot or oscillate before aligning with it.
* For **η = 1e−4**
  The method **reliably enters the valley**, but more slowly.
* For **η = 1e−5**
  The method **does enter the valley**, but extremely slowly.

### Backtracking GD

* Backtracking **always enters the valley** from all tested initial points.
* It automatically reduces the step size when the curvature becomes steep.
* Entry into the valley is **more reliable and stable** than with fixed η.

**Conclusion:**
Backtracking consistently and safely guides the iterates into the Rosenbrock valley, while constant step sizes may enter fast or slow depending on η.

---

## 2. How long does it take to “turn” along the valley direction?

The Rosenbrock valley is:

* narrow
* curved
* poorly aligned with the gradient direction

### Constant step size GD

* With **η = 1e−3**
  Turning happens **late**, after noticeable zig-zagging.
* With **η = 1e−4**
  Turning is smoother but still requires many iterations.
* With **η = 1e−5**
  Turning happens almost immediately, but progress is **extremely slow**.

### Backtracking GD

* The method adapts η dynamically.
* It **turns into the valley direction earlier** than constant-η methods.
* Curvature information is implicitly handled via Armijo’s condition.

**Conclusion:**
Backtracking reaches the correct valley direction faster and more smoothly than fixed step sizes.

---

## 3. Does the method zig-zag?

### Why zig-zag happens

* Gradients are almost **orthogonal** to the valley direction.
* Large curvature in one direction (θ2) and small curvature in the other (θ1).

### Constant step size GD

* **η = 1e−3** → strong zig-zagging across the valley
* **η = 1e−4** → mild zig-zagging
* **η = 1e−5** → almost no zig-zag, but very slow progress

### Backtracking GD

* Zig-zagging is **greatly reduced**.
* Step size shrinks automatically when oscillations would occur.

**Conclusion:**
Zig-zagging is severe for larger constant step sizes and minimal with backtracking.

---

## 4. Do step sizes become too small or too large?

### Constant step size GD

* Step size is **fixed**, regardless of curvature.
* If η is:

  * too large → risk of divergence or oscillation
  * too small → convergence is extremely slow
* No adaptation to the geometry of the function.

### Backtracking GD

* Step sizes **decrease automatically** in steep regions.
* Larger steps are used in flat regions.
* Prevents divergence and excessive oscillations.

**Conclusion:**
Backtracking avoids both extremes:

* it does not get stuck with too small steps
* it does not explode with too large steps

---

## 5. Interpretation of the loss curves L(θᵏ) vs iteration

### Constant step size

* Loss decreases monotonically.
* For small η, loss curve is very flat → slow convergence.
* For larger η, loss drops fast initially but may plateau or oscillate.

### Backtracking

* Loss decreases smoothly and consistently.
* Faster reduction in early iterations.
* Fewer wasted iterations.

---

## Final Summary (Exam-Ready)

* The Rosenbrock function has a **narrow, curved valley**, making GD difficult.
* Constant step size GD:

  * may zig-zag,
  * may take long to align with the valley,
  * requires careful tuning of η.
* Backtracking GD:

  * reliably enters the valley,
  * adapts step sizes to curvature,
  * reduces zig-zagging,
  * converges more robustly.

**Key takeaway:**
Backtracking line search significantly improves the stability and efficiency of Gradient Descent on ill-conditioned, non-convex landscapes like the Rosenbrock function.

---

If you want, I can also:

* condense this into **5–6 bullet points for quick exam answers**, or
* rewrite it in **very short viva-style explanations**.
