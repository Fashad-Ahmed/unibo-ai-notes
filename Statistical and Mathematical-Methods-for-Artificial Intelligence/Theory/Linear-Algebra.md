# Lecture Notes: Statistical and Mathematical Methods for AI


## Table of Contents
1.  [Numerical Computation and Finite Numbers](#1-numerical-computation-and-finite-numbers)
    * [1.1 Machine representation of number](#11-machine-representation-of-number)
2.  [Linear Algebra basics for AI](#2-linear-algebra-basics-for-ai)
    * [2.1 Vector spaces](#21-vector-spaces)
    * [2.2 Matrices](#22-matrices)
    * [2.3 Scalar Product and Norms in Vector Spaces](#23-scalar-product-and-norms-in-vector-spaces)

---

## 1. Numerical Computation and Finite Numbers


[cite_start]A **numerical method** is a mathematical tool that can be run on a computer to solve numerical problems[cite: 15]. [cite_start]The implementation of this method is called a **numerical algorithm**[cite: 16].

[cite_start]When using algorithms, we encounter approximations and errors[cite: 17]:
* [cite_start]**Measure errors:** Caused by the measuring instrument[cite: 18].
* [cite_start]**Algorithmic errors:** Caused by the propagation of rounding errors during computation[cite: 19].
* [cite_start]**Truncation errors:** Caused by cutting an infinite procedure short (e.g., approximating an infinite series with a finite sum)[cite: 20].
* [cite_start]**Inherent errors:** Caused by the finite representation of the data itself[cite: 21].

### Definitions of Error

[cite_start]**Definition 1.1:** Given a true value $x$ and an approximation $\tilde{x}$[cite: 23]:
* [cite_start]**Absolute Error:** $E_{x}=|x-\tilde{x}|$ [cite: 23, 25]
* [cite_start]**Relative Error:** $R_{x}=|\frac{x-\tilde{x}}{x}|$, for $x \ne 0$ [cite: 24, 25]

**Definition 1.2: Accuracy**
* [cite_start]Accuracy is the number of correct significant digits in an approximation[cite: 26].
* [cite_start]This is different from **machine precision**, which is the total number of digits a number is expressed with[cite: 28].

**Definition 1.3: Significant Digits**
* [cite_start]$\tilde{x}$ approximates $x$ to $d$ significant digits if $d$ is the largest non-negative integer such that[cite: 29]:
    $$|\frac{x-\tilde{x}}{x}| < \frac{10^{1-d}}{2}$$
    [cite_start][cite: 30]

> [cite_start]**Example 1.1:** [cite: 31]
> [cite_start]* Let $x = 3.141592$ and $\tilde{x} = 3.14$[cite: 31].
> * $|\frac{x-\tilde{x}}{x}| [cite_start]= 0.000507$[cite: 32].
> [cite_start]* $0.000507 < \frac{10^{1-3}}{2} = 0.5 \cdot 10^{-2} = 0.005$[cite: 32].
> [cite_start]* Thus, $\tilde{x}$ approximates $x$ to $d=3$ significant digits[cite: 33].

**Total Error**
If we want to compute $f(x)$ but use an approximate input $\tilde{x}$ and an approximate function $\tilde{f}$:
* [cite_start]**Total Error** = $\tilde{f}(\tilde{x}) - f(x)$ [cite: 39, 40]
* This can be split into:
    $\tilde{f}(\tilde{x}) - f(x) = \underbrace{(\tilde{f}(\tilde{x}) - f(\tilde{x}))}_\text{Algorithmic Error} + \underbrace{(f(\tilde{x}) - f(x))}_\text{Inherent Error}$
    [cite_start][cite: 40, 41]

### 1.1 Machine representation of number


**1. Positional Representation (Base $\beta$)**
$x_{\beta} = sign(x)(x_{n}\beta^{n} + \dots + x_{1}\beta + x_{0} + x_{-1}\beta^{-1} + \dots + x_{-m}\beta^{-m})$
[cite_start][cite: 45, 46]

**2. Floating-Point Representation**
[cite_start]This is how computers store real numbers, using a base $\beta$, precision $t$, and an exponent range $[L, U]$ [cite: 52-55]. [cite_start]The set of these numbers is $\mathcal{F}(\beta, t, L, U)$[cite: 57].
* [cite_start]$x = sign(x) \cdot m \cdot \beta^{e-t+1}$ [cite: 49]
* [cite_start]$m$ is the **mantissa** (the significant digits)[cite: 50].
* [cite_start]$e$ is the **exponent**[cite: 50].

**Normalized Representation**
[cite_start]To ensure a unique representation, it's assumed the first digit $x_0 \ne 0$[cite: 58]. [cite_start]This is called **normalized representation**[cite: 59].

> [cite_start]**Example 1.2: 32-bit floating point** [cite: 60]
> [cite_start]* A 32-bit number is decoded[cite: 61].
> [cite_start]* $sign = 0$ (positive) [cite: 63]
> * $e = -3$ [cite: 64]
> [cite_start]* $m = 1.010...$ (in binary, including the "hidden bit") [cite: 65]
> [cite_start]* Value in base 10: $(1.01)_{2} \cdot 2^{-3} = (1 \cdot 2^{0} + 0 \cdot 2^{-1} + 1 \cdot 2^{-2}) \cdot 2^{-3} = 0.15625$ [cite: 67]

**Rounding Rules**
How a real number $x$ is approximated to a floating-point number $fl(x)$[cite: 75]:
1.  **Round-by-chop:** Truncate the digits after $t$ digits[cite: 76].
2.  **Round-to-nearest:** Set $fl(x)$ to the *nearest* floating-point number. If there's a tie, round to the number whose last digit is even[cite: 77, 78].

**Definition 1.4: Machine Precision ($\epsilon_{mach}$)**
[cite_start]This characterizes the accuracy of a floating-point system[cite: 79].
* [cite_start]Using round-by-chop: $\epsilon_{mach} = \beta^{1-t}$ [cite: 79]
* [cite_start]Using round-to-nearest: $\epsilon_{mach} = \frac{1}{2}\beta^{1-t}$ [cite: 80]

[cite_start]**Definition 1.5:** $\epsilon_{mach}$ is also the smallest positive number satisfying $fl(1 + \epsilon_{mach}) > 1$[cite: 82, 83].

**Proposition 1.1: Maximum Relative Error**
[cite_start]The maximum relative error in representing a real number $x$ is given by[cite: 84]:
$$|\frac{fl(x)-x}{x}| \le \epsilon_{mach}$$
[cite_start][cite: 85]

---

## 2. Linear Algebra basics for AI


### 2.1 Vector spaces


**Definition 2.1: Vector Space**
[cite_start]A vector space $V$ over a field $F$ (like $\mathbb{R}$ or $\mathbb{C}$) is a set of **vectors** that is closed under finite vector addition and scalar multiplication[cite: 95, 96].

[cite_start]These two operations must satisfy 8 properties[cite: 97]:
1.  [cite_start]**Commutativity of addition:** $v+w = w+v$ [cite: 98, 99]
2.  [cite_start]**Associativity of addition:** $u+(v+w) = (u+v)+w$ [cite: 100, 101]
3.  [cite_start]**Identity element of addition:** There exists a $0$ vector such that $v+0=v$ [cite: 102, 104]
4.  [cite_start]**Additive inverse:** For every $v$, there exists a $-v$ such that $v+(-v)=0$ [cite: 105, 106]
5.  [cite_start]**Identity element of scalar multiplication:** $1v = v$ [cite: 107, 108]
6.  [cite_start]**Compatibility of scalar multiplication:** $(ab)v = a(bv)$ [cite: 109, 110]
7.  [cite_start]**Distributivity (field addition):** $(a+b)v = av+bv$ [cite: 112, 113]
8.  [cite_start]**Distributivity (vector addition):** $a(v+w) = av+aw$ [cite: 114]

**Definition 2.2: Subspace**
[cite_start]A set $W$ is a subspace of $V$ if $W \subset V$ and $W$ is also a vector space over $F$[cite: 120, 121, 122].

### 2.1.1 Linear independence


**Definition 2.3: Span**
[cite_start]The set $W$ of all finite linear combinations of vectors $\{v_1, \dots, v_m\}$ is called the **subspace spanned** by them[cite: 135].
$W = span\{v_1, \dots, v_m\} = \{\sum_{i=1}^{m} \alpha_i v_i \mid v_i \in V, \alpha_i \in F\}$
[cite_start][cite: 136]

**Definition 2.4: Linear Independence**
[cite_start]A set of vectors $\{v_1, \dots, v_m\}$ is **linearly independent** if[cite: 139]:
$\alpha_{1}v_{1}+...+\alpha_{m}v_{m}=0 \Rightarrow \alpha_{1}=\alpha_{2}=...=\alpha_{m}=0$
[cite_start][cite: 140]
* [cite_start]If this is not true, the system is **linearly dependent**[cite: 141].
* Geometrically, $n$ dependent vectors lie on the same $(n-1)$-dimensional hyperplane[cite: 142].

**Definition 2.5: Basis**
A **basis** for a vector space $V$ is any system of linearly independent generators of $V$[cite: 147].
* [cite_start]**Example:** $\{(1,0,0), (0,1,0), (0,0,1)\}$ is a basis for $\mathbb{R}^3$[cite: 148, 149].

**Proposition 2.1: Dimension**
[cite_start]If a vector space $V$ has a basis of $n$ vectors, then every other basis of $V$ also has exactly $n$ elements[cite: 150, 151]. [cite_start]This number $n$ is the **dimension** of $V$, or $dim(V)$[cite: 152].

### 2.2 Matrices


**Definition 2.6: Matrix**
[cite_start]A matrix $A$ is a rectangular array of $m$ rows and $n$ columns of elements in a field $F$, denoted $A \in F^{m \times n}$[cite: 156, 158]. [cite_start]If $m=n$, the matrix is **square**[cite: 158].

**Definition 2.7: Rank**
[cite_start]The **rank** of $A$, or $rank(A)$, is the maximum number of linearly independent columns (or rows) of $A$[cite: 161].
* $A$ has **full rank** if $rank(A) = min(m, n)$[cite: 162].

**Definition 2.8: Triangular Matrices**
* [cite_start]**Lower triangular (L):** $l_{ij} = 0$ if $i < j$ (zeros above the diagonal)[cite: 163].
* **Upper triangular (U):** $u_{ij} = 0$ if $i > j$ (zeros below the diagonal)[cite: 164].

### 2.2.1 Operations with matrices


Let $A, B \in \mathbb{R}^{m \times p}$, $C \in \mathbb{R}^{p \times n}$, $\lambda \in F$[cite: 167].

1.  **Matrix Addition:** $A+B = (a_{ij} + b_{ij})$[cite: 168, 169].
2.  **Matrix Multiplication by a Scalar:** $\lambda A = (\lambda a_{ij})$[cite: 172, 173].
3.  **Matrix Multiplication (Product):** $A C = (\sum_{k=1}^{p} a_{ik} c_{kj})$. The resulting matrix is $m \times n$[cite: 174, 175, 177].
    * [cite_start]**Note:** This is only defined if the columns of $A$ equal the rows of $C$[cite: 176].
    * [cite_start]It is **not** commutative: $AC \ne CA$ in general[cite: 179].
4.  **Transposition:** $A^T = (a_{ji})$. [cite_start]A $m \times p$ matrix becomes a $p \times m$ matrix[cite: 180, 181].
    * **Properties:** $(A^T)^T = A$, $(A+B)^T = A^T + B^T$, $(AC)^T = C^T A^T$[cite: 183].

**Definition 2.10: Identity Matrix ($I$)**
The **identity matrix** $I_n$ is a square ($n \times n$) matrix with 1s on the main diagonal and 0s elsewhere[cite: 191]. It's the identity element for multiplication: $AI = IA = A$[cite: 193].

**Definition 2.11: Invertible Matrix**
A square matrix $A$ is **invertible** (or **nonsingular**) if there exists a matrix $B$, (denoted $A^{-1}$), such that $AB = BA = I$[cite: 194].
* [cite_start]A non-invertible matrix is called **singular**[cite: 195].
* [cite_start]**Properties:** $(A^{-1})^{-1} = A$, $(AB)^{-1} = B^{-1}A^{-1}$, $(A^T)^{-1} = (A^{-1})^T$[cite: 196, 197].

[cite_start]**Proposition 2.2:** A square matrix is invertible if and only if its column vectors are linearly independent[cite: 198].

[cite_start]**Definition 2.12: Special Square Matrices** [cite: 204]
* **Symmetric:** $A = A^T$[cite: 204].
* [cite_start]**Anti-symmetric:** $A = -A^T$[cite: 204].
* [cite_start]**Orthogonal:** $A^{-1} = A^T$, which means $AA^T = A^T A = I$[cite: 204].

### 2.2.2 Determinant of a matrix


**Definition 2.13: Determinant ($det(A)$)**
[cite_start]The determinant is a scalar value associated with a square matrix $A \in \mathbb{C}^{n \times n}$[cite: 212]. [cite_start]It can be defined recursively using **Laplace's rule**[cite: 217]:
$det(A) = \sum_{j=1}^{n}(-1)^{i+j} a_{ij} det(A_{ij})$ (expansion along row $i$)
[cite_start][cite: 213, 215]
* [cite_start]$A_{ij}$ is the submatrix of $A$ obtained by removing row $i$ and column $j$[cite: 216].

**Properties of Determinants:**
* [cite_start]If $A$ is triangular or diagonal, $det(A) = \prod_{i=1}^{n} a_{ii}$ (product of diagonal elements)[cite: 219].
* $det(A) = det(A^T)$ [cite: 221]
* [cite_start]$det(AB) = det(A)det(B)$ [cite: 221]
* [cite_start]$det(A^{-1}) = \frac{1}{det(A)}$ [cite: 221]
* $det(\alpha A) = \alpha^n det(A)$ for $A(n \times n)$ [cite: 222]

**Proposition 2.3:** Every orthogonal matrix $A$ has $det(A) = \pm 1$[cite: 224, 225].

> **Example 2.10: 2x2 Determinant** [cite: 227]
> $A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$ [cite: 228]
> $det(A) = a_{11}a_{22} - a_{21}a_{12} = (1)(4) - (3)(2) = -2$ [cite: 230]

**Proposition 2.4: Formula for the Inverse** [cite: 250]
$A^{-1} = \frac{C^T}{det(A)}$
[cite_start][cite: 251]
* [cite_start]$C$ is the **cofactor matrix**, where $c_{ij} = (-1)^{i+j} det(A_{ij})$[cite: 252].

**Proposition 2.5: Equivalent Properties for Nonsingularity**
[cite_start]For an $n \times n$ matrix $A$, the following are equivalent[cite: 253]:
* $A$ is nonsingular (invertible)[cite: 254].
* [cite_start]$det(A) \ne 0$[cite: 255].
* [cite_start]$rank(A) = n$[cite: 256].
* The columns (and rows) of $A$ are linearly independent[cite: 257].

### 2.2.3 Eigenvalues and eigenvectors


**Definition 2.14: Eigenvalue and Eigenvector**
Let $A \in \mathbb{C}^{n \times n}$. A number $\lambda \in \mathbb{C}$ is an **eigenvalue** of $A$ if[cite: 274]:
$\exists x \in \mathbb{C}^n, x \ne 0$ such that $Ax = \lambda x$
[cite_start][cite: 275]
* [cite_start]The vector $x$ is the **eigenvector** associated with $\lambda$[cite: 276].
* [cite_start]The set of all eigenvalues is the **spectrum** of $A$, $\sigma(A)$[cite: 276].
* Eigenvalues are found by solving the **characteristic equation**: $p_A(\lambda) = det(A - \lambda I) = 0$[cite: 277, 278].

**Definition 2.15: Algebraic Multiplicity**
The number of times an eigenvalue $\lambda_i$ appears as a root in the characteristic polynomial[cite: 281, 282].

**Definition 2.16: Spectral Radius ($\rho(A)$)**
The maximum eigenvalue in terms of magnitude (absolute value or modulus)[cite: 283]:
$\rho(A) = \max_{\lambda \in \sigma(A)} |\lambda|$
[cite_start][cite: 284]

**Properties of Eigenvalues:**
* [cite_start]Eigenvectors are not unique: If $x$ is an eigenvector, so is $cx$ for any $c \ne 0$[cite: 287, 288].
* [cite_start]**Prop 2.6:** $det(A) = \prod_{i=1}^{n} \lambda_i$ (The determinant is the product of the eigenvalues)[cite: 290, 291].
* **Prop 2.7:** A matrix is singular (non-invertible) if and only if it has at least one eigenvalue equal to zero[cite: 292].
* [cite_start]**Prop 2.8:** If $A$ is triangular or diagonal, its eigenvalues are its diagonal entries, $\lambda_i = a_{ii}$[cite: 293].

**Definition 2.17: Similar Matrices**
[cite_start]Two matrices $A$ and $B$ are **similar** if there exists a non-singular matrix $P$ such that $B = PAP^{-1}$[cite: 295].
* Similar matrices have the same eigenvalues[cite: 296].

### 2.3 Scalar Product and Norms in Vector Spaces


**Definition 2.19: Norm**
A **norm** $||\cdot||$ is a map from a vector space $V$ to $F$ ($||\cdot|| : V \to F$) that satisfies[cite: 298]:
1.  $||v|| \ge 0$, and $||v|| = 0 \iff v = 0$ (Positivity) [cite: 299]
2.  $||\alpha v|| = |\alpha| \cdot ||v||$ (Scaling) [cite: 299]
3.  $||v+w|| \le ||v|| + ||w||$ (Triangle Inequality) [cite: 300]

A vector space with a norm is a **normed space**[cite: 301].

**Vector p-norms:** $||v||_p = \left( \sum_{i=1}^n |v_i|^p \right)^{1/p}$ [cite: 306, 307, 310, 311]
* [cite_start]**Example 2.15 (p=1): One norm:** $||v||_1 = \sum_{i=1}^n |v_i|$[cite: 304, 305].
* **Example 2.14 (p=2): Euclidean norm:** $||v||_2 = \sqrt{\sum_{i=1}^n |v_i|^2}$[cite: 302, 303].
* [cite_start]**Example 2.17 (p=$\infty$): Infinity norm:** $||v||_\infty = \max_{i} |v_i|$[cite: 313, 314].

### 2.3.1 Matrix norms


**Definition 2.21: Matrix Norm**
A map $||\cdot|| [cite_start]: \mathbb{R}^{m \times n} \to \mathbb{R}$ satisfying the same three properties as vector norms (positivity, scaling, triangle inequality) [cite: 319-322].

**Definition 2.22: Compatible Norm**
A matrix norm is **compatible** with a vector norm if:
$||Ax|| \le ||A|| \cdot ||x||$
[cite_start][cite: 323, 324]

**Common Matrix Norms:**
* **Example 2.18: Spectral Norm ($||A||_2$):**
    [cite_start]$||A||_2 = \sqrt{\rho(A^T A)}$ (This is the "stretching power" of the matrix)[cite: 326, 327].
* **Example 2.19: 1-Norm ($||A||_1$):**
    [cite_start]$||A||_1 = \max_{j} \sum_{i=1}^n |a_{ij}|$ (Maximum absolute column sum)[cite: 330, 331].
* **Example 2.20: Infinity-Norm ($||A||_\infty$):**
    [cite_start]$||A||_\infty = \max_{i} \sum_{j=1}^n |a_{ij}|$ (Maximum absolute row sum)[cite: 334, 335].
* **Example 2.21: Frobenius Norm ($||A||_F$):**
    [cite_start]$||A||_F = \sqrt{\sum_{i,j=1}^n |a_{ij}|^2}$ (Treated as one long vector)[cite: 338, 339].