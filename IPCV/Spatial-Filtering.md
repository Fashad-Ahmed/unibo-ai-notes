
### What an image filter actually does

An image filter is just a rule for computing a new pixel value using its neighbors.

Instead of looking at one pixel in isolation, you take a **small window** (called a *neighborhood* or *support*) around it—say a 3×3 or 5×5 patch—and combine those values to produce a new value.

* If the rule **averages** neighbors → you smooth noise
* If it **emphasizes differences** → you highlight edges

So filters are local operations applied across the whole image.

---

### Why filters are useful

By changing how you combine neighboring pixels, you can achieve different effects:

* **Denoising** → remove random variations
* **Sharpening / edge enhancement** → highlight boundaries
* **Feature extraction** → detect patterns like edges, corners, textures

These are foundational steps in Computer Vision.

---

### Linear and Translation-Equivariant (LTE) filters

This sounds intimidating, but it boils down to two simple properties:

#### 1. Linear

The filter behaves nicely with addition and scaling:

* Filtering (A + B) = filtering(A) + filtering(B)
* Filtering (k·A) = k·filtering(A)

This makes analysis easier and connects directly to signal processing math.

---

#### 2. Translation-equivariant

If you shift the input image, the output shifts the same way.

* Move an object to the right → filtered result also moves right
* The filter doesn’t “care” where something is, only what it looks like

This is crucial for detecting patterns anywhere in an image.

---

### Convolution: how LTE filters are applied

LTE filters are implemented using **2D convolution**, a core idea from Convolution.

Think of it like this:

1. Take a small matrix (called a **kernel** or **filter**)
2. Place it over a patch of the image
3. Multiply corresponding values
4. Sum them up → that’s the new pixel value
5. Slide the kernel across the whole image

The kernel is also called a **point spread function**, because it defines how a single pixel’s influence spreads to its neighbors.

---

### Example intuition

A simple blur filter kernel:

[
\frac{1}{9}
\begin{bmatrix}
1 & 1 & 1 \
1 & 1 & 1 \
1 & 1 & 1
\end{bmatrix}
]

This averages nearby pixels → reduces noise but softens details.

An edge detector kernel:

[
\begin{bmatrix}
-1 & -1 & -1 \
-1 & 8 & -1 \
-1 & -1 & -1
\end{bmatrix}
]

This highlights intensity changes → reveals edges.

---

### Connection to CNNs

In Convolutional Neural Networks:

* The “filters” are **learned automatically** instead of manually designed
* Each filter detects patterns (edges, textures, shapes)
* Because convolution is translation-equivariant, the network can detect features anywhere in the image

So CNNs are basically stacking many learned LTE filters.

---

### Big picture

* Filters = local rules applied across an image
* LTE filters = a mathematically clean and powerful subset
* Convolution = the mechanism that applies them
* CNNs = systems that learn these filters automatically

---


# Step-by-step: how convolution works

Imagine a tiny grayscale image (values 0–255):

[
\begin{bmatrix}
10 & 10 & 10 \
10 & 50 & 10 \
10 & 10 & 10
\end{bmatrix}
]

And a simple **edge detection kernel**:

[
\begin{bmatrix}
-1 & -1 & -1 \
-1 & 8 & -1 \
-1 & -1 & -1
\end{bmatrix}
]

---

### Apply the filter to the center pixel

We multiply element-by-element and sum:

[
(10×-1) + (10×-1) + (10×-1) \

* (10×-1) + (50×8) + (10×-1) \
* (10×-1) + (10×-1) + (10×-1)
  ]

[
= -10 -10 -10 -10 + 400 -10 -10 -10 -10 = 320
]

 The result is **large**, meaning:

* The center pixel is very different from neighbors
* So it's likely an **edge or feature**

---

### Slide across the image

You repeat this for every pixel (sliding window).
That sliding process is exactly what Convolution does.

---

# Python example (OpenCV)

Here’s a minimal working example using OpenCV:

```python
import cv2
import numpy as np

# Load grayscale image
img = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)

# 1. Blur kernel (denoising)
blur_kernel = np.ones((3, 3), np.float32) / 9

# 2. Edge detection kernel
edge_kernel = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
])

# Apply filters
blurred = cv2.filter2D(img, -1, blur_kernel)
edges = cv2.filter2D(img, -1, edge_kernel)

# Show results
cv2.imshow("Original", img)
cv2.imshow("Blurred (Denoised)", blurred)
cv2.imshow("Edges", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

# What’s happening in practice

* `filter2D` performs the convolution operation
* The **kernel defines behavior**:

  * Averaging kernel → smooths noise
  * Edge kernel → highlights intensity changes

---

# Link to CNNs

In Convolutional Neural Networks:

* Instead of manually choosing kernels like above
* The network **learns the kernel values automatically**
* Early layers often learn edge detectors similar to the one we used

---

# Key intuition to remember

* Kernel = “what pattern am I looking for?”
* Convolution = “scan the image for that pattern”
* Output value = “how strongly that pattern exists here”


Understood.

Let’s go a bit deeper and make padding and stride crystal clear in an exam-oriented way.

---

# 1. Stride

**Definition:**
Stride is the number of pixels the kernel moves at each step during convolution.

### Cases

* **Stride = 1**
  The filter moves one pixel at a time → maximum overlap → detailed output

* **Stride = 2 (or more)**
  The filter skips pixels → fewer computations → smaller output

### Key effect

* Increasing stride reduces the **spatial resolution** of the output
* It effectively performs **downsampling**

---

# 2. Padding

**Definition:**
Padding adds extra pixels (usually zeros) around the border of the image.

### Why padding is needed

Without padding:

* The kernel cannot fully cover border pixels
* Output becomes smaller after each convolution

---

### Types

#### Valid padding (P = 0)

* No padding
* Output shrinks

#### Same padding (P chosen properly)

* Keeps output size equal to input size (if stride = 1)
* Common in Convolutional Neural Networks

---

# 3. Output size formula

For each dimension (height or width):

[
\text{Output} = \frac{N - K + 2P}{S} + 1
]

Where:

* (N) = input size
* (K) = kernel size
* (P) = padding
* (S) = stride

Important: the result must be an integer (otherwise the configuration is invalid or requires adjustment).

---

# 4. Concrete example

Input: 5 × 5
Kernel: 3 × 3

### Case 1: No padding, stride 1

[
(5 - 3)/1 + 1 = 3
]

Output: 3 × 3

You lose the border.

---

### Case 2: Padding = 1, stride 1

[
(5 - 3 + 2)/1 + 1 = 5
]

Output: 5 × 5

Size is preserved.

---

### Case 3: Padding = 1, stride 2

[
(5 - 3 + 2)/2 + 1 = 3
]

Output: 3 × 3

Here you both preserve borders (via padding) and reduce size (via stride).

---

# 5. Intuition summary

* **Stride**

  * Controls how densely you scan the image
  * Larger stride → less detail, smaller output

* **Padding**

  * Controls what happens at the borders
  * Prevents shrinking and preserves edge information

---

# 6. Common exam traps

* Forgetting the **+1** in the formula
* Not checking that the output size is an integer
* Assuming padding always keeps size (it only does when chosen correctly)
* Confusing stride with kernel size

---

# 7. Conceptual link

In Computer Vision and deep learning:

* Early layers often use **stride = 1** to preserve detail
* Later layers may use **stride > 1** to reduce dimensionality
* Padding is used to avoid losing important spatial information too early

---

## 1. Linearity

An operator ( T ) is **linear** if it satisfies:

[
T{\alpha, i_1(x,y) + \beta, i_2(x,y)}
= \alpha, T{i_1(x,y)} + \beta, T{i_2(x,y)}
]

where:

* ( i_1, i_2 ) are input signals (images),
* ( \alpha, \beta ) are constants,
* ( o_1 = T{i_1}, ; o_2 = T{i_2} ).

👉 Meaning: applying the operator to a weighted sum = weighted sum of outputs.

---

## 2. Translation Equivariance

An operator is **translation-equivariant** if shifting the input results in the same shift in the output:

[
T{ i(x - x', y - y') }
= o(x - x', y - y')
]

👉 Meaning: the operator doesn’t care **where** something is, only **what** it is.

---

## 3. Why this leads to Convolution

Here’s the key result:

> Any operator that is **both linear and translation-equivariant** can be written as a **convolution**.

So:

[
o(x,y) = T{i(x,y)} = (i * h)(x,y)
]

where:

* ( h(x,y) ) is the **impulse response** (or kernel),
* ( * ) denotes convolution.

Expanded:

[
o(x,y) = \sum_{u,v} i(u,v), h(x - u, y - v)
]

---

## 4. Intuition

* **Linearity** → lets you decompose the image into simple components
* **Translation equivariance** → ensures the same operation is applied everywhere
* Together → the operator behaves like a **sliding filter** → convolution

---

## 5. Practical Meaning (e.g., in CNNs)

This is exactly why **convolutional layers** work:

* Same filter applied across the image
* Detects patterns regardless of position
* Efficient and structured


# Step 1: Build the image from impulses

Any 2D signal ( i(x,y) ) can be written as a sum of shifted **impulses**:

[
i(x,y) = \sum_{u,v} i(u,v), \delta(x - u, y - v)
]

👉 Think of this as:

* At every position ((u,v)), you place a spike (impulse)
* Its weight is the pixel value ( i(u,v) )

So the image is just a **sum of shifted impulses**.

---

# Step 2: Apply the operator ( T )

Apply ( T ) to both sides:

[
T{i(x,y)}
= T\left{ \sum_{u,v} i(u,v), \delta(x - u, y - v) \right}
]

---

# Step 3: Use linearity

Because ( T ) is linear:

[
= \sum_{u,v} i(u,v), T{\delta(x - u, y - v)}
]

---

# Step 4: Use translation equivariance

Translation equivariance tells us:

[
T{\delta(x - u, y - v)}
= h(x - u, y - v)
]

where:
[
h(x,y) = T{\delta(x,y)}
]

👉 This ( h ) is the **impulse response** (the output when input is a single spike).

---

# Step 5: Put it all together

[
o(x,y) = \sum_{u,v} i(u,v), h(x - u, y - v)
]

And that is exactly **convolution**:

[
o(x,y) = (i * h)(x,y)
]

---

# Intuition (this is the important part)

* Break image into **tiny spikes**
* See how the system responds to **one spike** → gives kernel ( h )
* Rebuild the output by summing all shifted responses

👉 So convolution is just:

> “Add up shifted copies of the impulse response, weighted by the input.”

---

# Visual way to think about it

Imagine:

* ( h ) is a small filter (e.g., edge detector)
* You **slide it across the image**
* At each position, you compute a weighted sum

That sliding process is exactly what the formula describes.

---

# Why this matters

This derivation explains:

* Why filters are shared across space (CNNs)
* Why convolution is the *only* operation with these properties
* Why kernels fully define the system

---

# 1) Numerical Example (3×3 image + 2×2 kernel)

Take a small image:

[
i =
\begin{bmatrix}
1 & 2 & 3 \
4 & 5 & 6 \
7 & 8 & 9
\end{bmatrix}
]

and a kernel:

[
h =
\begin{bmatrix}
1 & 0 \
0 & -1
\end{bmatrix}
]

---

## Step-by-step convolution

We slide the kernel over the image and compute:

[
o(x,y) = \sum i(u,v), h(x-u, y-v)
]

For simplicity, we’ll compute **valid convolution** (no padding).

---

### Top-left position

[
\begin{bmatrix}
1 & 2 \
4 & 5
\end{bmatrix}
\quad \text{with} \quad
\begin{bmatrix}
1 & 0 \
0 & -1
\end{bmatrix}
]

Compute:

[
(1 \cdot 1) + (2 \cdot 0) + (4 \cdot 0) + (5 \cdot -1)
= 1 - 5 = -4
]

---

### Top-right

[
\begin{bmatrix}
2 & 3 \
5 & 6
\end{bmatrix}
]

[
2\cdot1 + 3\cdot0 + 5\cdot0 + 6\cdot(-1)
= 2 - 6 = -4
]

---

### Bottom-left

[
\begin{bmatrix}
4 & 5 \
7 & 8
\end{bmatrix}
]

[
4 - 8 = -4
]

---

### Bottom-right

[
\begin{bmatrix}
5 & 6 \
8 & 9
\end{bmatrix}
]

[
5 - 9 = -4
]

---

## Final output

[
o =
\begin{bmatrix}
-4 & -4 \
-4 & -4
\end{bmatrix}
]

---

## What just happened (intuition)

This kernel is basically computing:

[
\text{top-left} - \text{bottom-right}
]

So it’s detecting a kind of **diagonal contrast**.

---

# 2) Convolution vs Correlation (VERY important)

Here’s the subtle but critical difference:

---

## Convolution

[
o(x,y) = \sum i(u,v), h(x-u, y-v)
]

👉 Kernel is **flipped** (both horizontally and vertically)

---

## Correlation

[
o(x,y) = \sum i(u,v), h(x+u, y+v)
]

👉 Kernel is used **as-is (no flipping)**

---

## Key Difference

| Operation   | Kernel flipped? | Used in practice     |
| ----------- | --------------- | -------------------- |
| Convolution | ✅ Yes           | Math / theory        |
| Correlation | ❌ No            | CNNs (almost always) |

---

## Example of flipping

Kernel:

[
\begin{bmatrix}
1 & 2 \
3 & 4
\end{bmatrix}
]

Flipped (for convolution):

[
\begin{bmatrix}
4 & 3 \
2 & 1
\end{bmatrix}
]

---

## Why CNNs “ignore” flipping

In deep learning:

* Kernels are **learned**
* Whether flipped or not doesn’t matter—the network adjusts weights

So frameworks like:

* TensorFlow
* PyTorch

actually implement **correlation**, but call it “convolution”.

---

# Final intuition

* **Convolution** = flip + slide + multiply + sum
* **Correlation** = slide + multiply + sum

👉 Same mechanics, just one subtle flip difference.


---

# 1) Finite image + kernel → why borders are a problem

In theory, convolution assumes **infinite signals**.
In practice:

* Image = finite matrix (e.g., ( M \times N ))
* Kernel = small matrix (e.g., ( 3 \times 3 ), ( 5 \times 5 ))

👉 When the kernel reaches the **edges**, part of it falls *outside* the image.

So the question is:

> “What values do we use outside the image?”

---

# 2) Two main strategies

## A) CROP (a.k.a. “valid convolution”)

* Only compute where the kernel **fully overlaps** the image
* Ignore borders

### Result:

* Output is **smaller**

Example:

* ( 5 \times 5 ) image + ( 3 \times 3 ) kernel → ( 3 \times 3 ) output

👉 Common in **classical image processing**

---

## B) PAD (a.k.a. “same convolution”)

* Extend the image artificially
* Allows kernel to be applied everywhere

### Result:

* Output size is **same as input** (if padding chosen properly)

👉 Preferred in **CNNs**, because:

* Keeps spatial dimensions stable
* Easier to stack layers

---

# 3) Padding methods (this is the key part)

Let’s say your 1D signal is:

[
[a ; b ; c ; d]
]

We extend it differently depending on the rule.

---

## 1) Zero Padding

[
[0 ; 0 ; a ; b ; c ; d ; 0 ; 0]
]

👉 Most common in deep learning

* Simple
* But introduces **artificial dark borders**

---

## 2) Replicate Padding (a.k.a. edge padding)

[
[a ; a ; a ; b ; c ; d ; d ; d]
]

👉 Border values are **repeated**

* Avoids artificial zeros
* Can create “flat” edges

---

## 3) Reflect Padding

[
[c ; b ; a ; b ; c ; d ; c ; b]
]

👉 Mirror the signal **including edge**

Pattern:

* Left side mirrors inward
* Edge value is repeated in reflection

---

## 4) Reflect_101 (a.k.a. symmetric without repeating edge)

[
[d ; c ; b ; a ; b ; c ; d ; c]
]

👉 Mirror **without duplicating the border pixel**

This is often used in libraries like OpenCV.

---

# 4) Visual intuition (2D case)

For a small image:

[
\begin{bmatrix}
a & b \
c & d
\end{bmatrix}
]

### Zero padding:

[
\begin{bmatrix}
0 & 0 & 0 \
0 & a & b \
0 & c & d \
0 & 0 & 0
\end{bmatrix}
]

---

### Replicate:

[
\begin{bmatrix}
a & a & b \
a & a & b \
c & c & d \
c & c & d
\end{bmatrix}
]

---

### Reflect:

[
\begin{bmatrix}
d & c & d \
b & a & b \
d & c & d \
b & a & b
\end{bmatrix}
]

---

# 5) Why different padding matters

Padding affects:

### 🔹 Edge behavior

* Zero padding → artificial edges
* Reflect → smoother transitions

### 🔹 Feature detection

* Bad padding can create **fake edges**
* Good padding preserves structure

### 🔹 CNN performance

* Zero padding is standard because:

  * Simple
  * Works well with learned filters

---

# 6) Summary

* **CROP** → smaller output, no assumptions
* **PAD** → same size, requires assumptions

Padding types:

* Zero → simplest, most used
* Replicate → repeats borders
* Reflect → mirror including edge
* Reflect_101 → mirror excluding edge

---



---

# 1) Numerical example: how padding changes the result

Take a simple image:

[
i =
\begin{bmatrix}
1 & 2 \
3 & 4
\end{bmatrix}
]

and a kernel:

[
h =
\begin{bmatrix}
1 & 1 \
1 & 1
\end{bmatrix}
]

This kernel just **sums neighbors**.

---

## A) Without padding (CROP / valid)

Only one position fits:

[
o = [1+2+3+4] = [10]
]

👉 Output:
[
\begin{bmatrix}
10
\end{bmatrix}
]

---

## B) Zero padding

Pad with zeros:

[
\begin{bmatrix}
0 & 0 & 0 \
0 & 1 & 2 \
0 & 3 & 4 \
0 & 0 & 0
\end{bmatrix}
]

Now compute all positions:

### Top-left:

[
0+0+0+1 = 1
]

### Top-right:

[
0+0+1+2 = 3
]

### Bottom-left:

[
0+1+0+3 = 4
]

### Bottom-right:

[
1+2+3+4 = 10
]

👉 Output:
[
\begin{bmatrix}
1 & 3 \
4 & 10
\end{bmatrix}
]

⚠️ Notice:

* Borders are **smaller values** → artificial effect from zeros

---

## C) Replicate padding

Pad by repeating edges:

[
\begin{bmatrix}
1 & 1 & 2 \
1 & 1 & 2 \
3 & 3 & 4 \
3 & 3 & 4
\end{bmatrix}
]

Now:

### Top-left:

[
1+1+1+1 = 4
]

### Top-right:

[
1+2+1+2 = 6
]

### Bottom-left:

[
1+1+3+3 = 8
]

### Bottom-right:

[
1+2+3+4 = 10
]

👉 Output:
[
\begin{bmatrix}
4 & 6 \
8 & 10
\end{bmatrix}
]

✔️ Much smoother than zero padding

---

## D) Reflect padding (intuitive result)

Would give values similar to replicate but:

* Better preserves **gradients**
* Less artificial flattening

---

# 2) How to compute padding size (“same” convolution)

Goal:

> Keep output size = input size

---

## General formula

For 1D (applies per dimension in 2D):

[
\text{output} =
\left\lfloor
\frac{N + 2P - K}{S}
\right\rfloor + 1
]

Where:

* ( N ) = input size
* ( K ) = kernel size
* ( P ) = padding
* ( S ) = stride

---

## For “same” output

We want:

[
\text{output} = N
]

So:

[
N = \frac{N + 2P - K}{S} + 1
]

---

## Case: stride = 1 (most common)

[
N = N + 2P - K + 1
]

Solve:

[
2P = K - 1
\quad \Rightarrow \quad
P = \frac{K - 1}{2}
]

---

## Examples

### 3×3 kernel

[
P = (3-1)/2 = 1
]

👉 Add 1 pixel border

---

### 5×5 kernel

[
P = (5-1)/2 = 2
]

👉 Add 2 pixels border

---

### Even kernel (e.g., 4×4)

[
P = (4-1)/2 = 1.5
]

⚠️ Not symmetric → frameworks handle this by:

* asymmetric padding (e.g., 1 left, 2 right)

---

# 3) Key takeaways

* Padding is not just technical—it **changes results**
* Zero padding → introduces artificial edges
* Replicate/reflect → more natural borders
* CNNs use zero padding mainly for **simplicity and consistency**

---

# 4) Mental model

* Kernel = “window”
* Padding = “what exists outside the image”
* Different padding = different assumptions about the world beyond the image

---


A **Gaussian filter** is one of the most important smoothing (blurring) filters in image processing and computer vision. It is widely used because it removes noise while preserving overall structure better than simple averaging.

---

# 1) What is a Gaussian filter?

A Gaussian filter replaces each pixel with a **weighted average of its neighbors**, where:

* nearby pixels matter a lot
* far pixels matter very little
* weights follow a **Gaussian (bell-shaped) distribution**

---

# 2) The Gaussian function (kernel definition)

In continuous form (2D):

[
G(x,y) = \frac{1}{2\pi\sigma^2} \exp\left(-\frac{x^2 + y^2}{2\sigma^2}\right)
]

Where:

* ( \sigma ) = standard deviation (controls blur strength)
* ( (x,y) ) = distance from center

---

# 3) What the kernel looks like (example)

A typical **3×3 Gaussian kernel**:

[
\frac{1}{16}
\begin{bmatrix}
1 & 2 & 1 \
2 & 4 & 2 \
1 & 2 & 1
\end{bmatrix}
]

Or a **5×5 version** (stronger smoothing):

[
\frac{1}{256}
\begin{bmatrix}
1 & 4 & 6 & 4 & 1 \
4 & 16 & 24 & 16 & 4 \
6 & 24 & 36 & 24 & 6 \
4 & 16 & 24 & 16 & 4 \
1 & 4 & 6 & 4 & 1
\end{bmatrix}
]

👉 Notice:

* center weight is largest
* values decrease smoothly outward

---

# 4) What it does to an image

Applying a Gaussian filter:

### Before:

* sharp edges
* noise present

### After:

* smooth image
* reduced noise
* blurred edges

---

# 5) Why Gaussian filtering works well

## Key reasons:

### ✔ Smooth weighting

Unlike averaging filters, it avoids harsh changes.

### ✔ Natural model of noise

Many real-world noises approximate Gaussian distributions.

### ✔ No ringing artifacts

Better than some frequency-domain filters.

---

# 6) Important property (VERY useful)

Gaussian filtering is:

> **separable**

Meaning:

[
2D ; Gaussian = (1D ; Gaussian_x) * (1D ; Gaussian_y)
]

So instead of a 2D convolution:

* first blur horizontally
* then vertically

👉 Much faster computation.

---

# 7) Effect of ( \sigma )

| σ value        | Effect                      |
| -------------- | --------------------------- |
| small (≈0.5–1) | slight smoothing            |
| medium (≈1–2)  | noticeable blur             |
| large (>2)     | strong blur, loss of detail |

---

# 8) Why it is used in CNNs and vision

Gaussian filters are used for:

* noise reduction (preprocessing)
* scale-space representation
* edge detection pipelines (Sobel, Canny)
* anti-aliasing before downsampling

---

# 9) Intuition

Think of it as:

> “Each pixel is replaced by a soft spotlight of its neighbors, where the center matters most.”



