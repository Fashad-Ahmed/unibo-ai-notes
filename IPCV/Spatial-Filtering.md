
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

