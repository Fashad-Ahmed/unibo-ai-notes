

# Part 1 — Why pixels aren't good features (Slides 2–7)

## The starting problem

$k$-NN and linear classifiers operating directly on raw pixel values are weak, because **raw pixel intensities are not a good feature space** for telling classes apart. Two images of the same object can differ enormously in raw pixel values (lighting, pose, position), while two images of *different* objects can have very similar raw pixels by coincidence. The classifier itself isn't the bottleneck — the **representation** is.

## The representation idea (Slide 3) — the classic polar coordinates example

This is the conceptual seed of the entire lecture. Suppose data points are arranged so that one class is a ring around the origin and the other class is everywhere else — this is **not linearly separable** in raw $(x_1,x_2)$ Cartesian coordinates (no straight line splits a ring from its surroundings). But apply a **change of coordinates**:

$$\rho = \sqrt{x_1^2+x_2^2}, \qquad \theta = \tan^{-1}\frac{x_2}{x_1}$$

In $(\rho,\theta)$ space, the ring becomes a horizontal band — and a band **is** linearly separable (two horizontal lines, or even one threshold on $\rho$, separate it cleanly).

**The lesson, stated generally:** a fixed nonlinear transformation of the input can turn a problem that's hard for a linear classifier into one that's easy for a linear classifier. **The art of classical computer vision was hand-designing this transformation** (polar coordinates, SIFT, HOG, color histograms, etc.); the art of deep learning is **learning** it from data instead.## Bag of Visual Words — BoVW (Slide 4) — the pre-deep-learning answer

This is the hand-crafted representation that dominated computer vision until 2012. The pipeline, borrowed conceptually from NLP's "bag of words" (where a document is represented by word-frequency counts, ignoring order):

1. Extract local descriptors at many points/patches in the image (e.g. **SIFT** descriptors).
2. Build a **codebook/dictionary** of "visual words" — representative descriptor clusters (typically via $k$-means clustering over a large pool of descriptors collected from many images).
3. For a new image, assign each of its local descriptors to its nearest codeword, and build a **histogram of codeword frequencies** — how many times each visual word occurred in the image.
4. **Classify using this histogram**, not the raw pixels: $f(\mathbf{x};\theta) = W\mathbf{x}+\mathbf{b}$, where $\mathbf{x}$ is now the histogram vector, not the pixel grid.

The key conceptual point: **the classifier never sees a raw pixel.** It only ever sees a fixed-length vector summarizing "what kinds of local patterns occurred, and how often" — that vector *is* the representation, and it's hand-engineered (the descriptor algorithm, the clustering, the histogram-building are all fixed, not learned end-to-end with the classifier).

## The concrete BoVW pipeline used pre-2012 (Slide 5) and the 2011 ILSVRC winner (Slide 6)

The lecture gives the literal recipe that was state-of-the-art:
- **Precomputed dense SIFT descriptors at 3 scales.**
- **1000 codewords** obtained by running $k$-means on 1 million randomly sampled SIFT descriptors.
- **Train a linear SVM with SGD** (chosen specifically because SGD scales to large datasets better than other SVM solvers).

The 2011 ILSVRC-winning system (Perronnin & Sánchez) pushed this further with **Fisher Vectors (FV)** instead of plain BoVW histograms — conceptually a richer, higher-order statistic of how local descriptors deviate from a generative (Gaussian Mixture) model of the descriptor space, not just simple counts. Concretely it used: low-level features = SIFT (128-dim, PCA-reduced to 64-dim) and color (96-dim); FV extraction using $N=1024$ Gaussians and $R=4$ spatial regions producing a huge $>520K$-dimensional vector, **compressed** down (8 bits/dim → eventually 1 bit/dim); then a one-vs-all linear SVM trained with SGD, with the SIFT-based and color-based systems **fused at a late stage** (i.e., each trained somewhat separately, combined at the end).

**Important exam point this slide makes implicitly**: representations got progressively *more complex and higher-dimensional* over years (BoVW histograms of length ~1000 → Fisher Vectors of length >500,000) as researchers tried to hand-engineer ever-richer fixed representations — and this arms race of cleverness is exactly what got displaced almost overnight once representation *learning* (deep nets) arrived in 2012.

## Representation learning (Slide 7) — the conceptual pivot of the whole course

The diagrams here contrast:
- **Fixed representation pipeline**: $x \to$ [hand-crafted feature extraction, codewords/frequency histogram — *not updated by gradients*] $\to$ classifier $\to$ loss. Only the **classifier** weights get updated by backward gradient flow; the feature-extraction step is frozen/fixed by design (no "backward" arrow reaches it).
- **Representation learning pipeline**: $x \to y \to z \to \ldots \to$ loss, where **every transform along the way is "learnable"**, and gradients flow **backward** through *all* of them, improving every stage, not just the final classifier.

This is precisely the definition given at the bottom of the section: **Deep learning ≈ Representation learning.** "Deep" doesn't just mean "many layers" — it means the **representation itself (not just the final decision boundary) is learned end-to-end from data via gradient descent**, rather than hand-engineered and frozen.

---

# Part 2 — From linear classifiers to neural networks (Slides 8–18)

## Linear classifier recap (Slide 8)

$$f(\mathbf{x};\theta) = W\mathbf{x}+\mathbf{b}, \quad W: 10\times3072,\ \mathbf{x}:3072\times1,\ \mathbf{b}:10\times1$$

(3072 = $32\times32\times3$ flattened CIFAR-10-style image; 10 = number of classes.)

## Adding one hidden layer = a neural network

$$f(\mathbf{x};\theta) = W_2\,\phi(W_1\mathbf{x}+\mathbf{b}_1) + \mathbf{b}_2$$

- New hyperparameters introduced: **dimension of the inner (hidden) representation $C$** and the choice of **activation function $\phi$**.
- Shapes: $W_1: C\times3072$, $\mathbf{b}_1: C\times1$, $W_2: 10\times C$, $\mathbf{b}_2:10\times1$.

This is genuinely the core trick: instead of mapping $x \to$ scores directly with **one** linear map, you map $x \to h$ (a learned intermediate representation) with one linear map + nonlinearity, then $h \to$ scores with a second linear map. **$h$ is exactly the learned representation** the "representation learning" framing promised — instead of hand-crafted SIFT/BoVW histograms, $h$ is whatever the network discovers is useful, driven purely by gradients from the loss.

## Why we need the activation function at all (Slide 9) — the crucial algebraic proof

This is one of the most important derivations in the whole lecture, and a classic exam question: **show that without a nonlinearity, stacking layers buys you nothing.**

$$f(\mathbf{x};\theta) = W_2(W_1\mathbf{x}+\mathbf{b}_1) + \mathbf{b}_2 = (W_2W_1)\mathbf{x} + (W_2\mathbf{b}_1+\mathbf{b}_2) = W_{21}\mathbf{x}+\mathbf{b}_{21}$$

Without $\phi$, the composition of two affine (linear+bias) maps **is just another affine map** ($W_{21}=W_2W_1$, $\mathbf{b}_{21}=W_2\mathbf{b}_1+\mathbf{b}_2$) — algebraically indistinguishable from a single-layer linear classifier, no matter how many layers you stack. **Depth without nonlinearity buys you literally zero extra expressive power.** This is exactly why the nonlinearity $\phi$ must sit *between* every pair of linear layers — it's what prevents the whole stack from collapsing back into one linear map.

## Activation functions in detail (Slides 10–12)

### Sigmoid

$$\phi(a) = \sigma(a) = \frac{1}{1+\exp(-a)}$$

Squashes any real input into $(0,1)$, historically motivated by analogy to biological neuron firing rates / probabilities.

### ReLU (Rectified Linear Unit)

$$\phi(a) = \text{ReLU}(a) = \max(0,a)$$

Simply zeroes out negative inputs and passes positive inputs through unchanged.

### The gradient comparison — this is the testable core of slide 11

$$\frac{d\sigma(a)}{da} = \sigma(a)(1-\sigma(a)) \qquad \frac{d\,\text{ReLU}(a)}{da} = \begin{cases}1 & a\ge0\\0 & \text{otherwise}\end{cases}$$

- **Sigmoid's gradient saturates** — for large $|a|$ (very positive or very negative inputs), $\sigma(a)(1-\sigma(a)) \to 0$. This is disastrous for training deep networks: during backpropagation, gradients get **multiplied together layer by layer** (chain rule), so if each layer's local gradient is tiny, the product **vanishes** exponentially with depth — this is the classic **vanishing gradient problem**, and it's precisely *why* sigmoid fell out of favor for hidden layers in deep nets.
- **ReLU's gradient is exactly 1 for all positive inputs** — no matter how large $a$ gets, the gradient never shrinks. This makes gradient flow through many stacked ReLU layers far more stable, which is the central reason ReLU enabled training of much deeper networks than sigmoid/tanh ever could.
- **The cost: "dead neurons."** If a ReLU unit's input $a$ is negative for *every* training example (which can happen due to unlucky initialization or large negative-pushing updates), its gradient is **always exactly 0** — that neuron **never updates again**, permanently "dead," contributing nothing to the network for the rest of training.

## Leaky ReLU (Slide 12) — the fix for dead neurons

$$\text{LeakyReLU}(a) = \begin{cases}a & a\ge0\\0.01a & \text{otherwise}\end{cases} \qquad \frac{d\,\text{LeakyReLU}(a)}{da} = \begin{cases}1 & a\ge0\\0.01 & \text{otherwise}\end{cases}$$

Instead of a hard zero for negative inputs, give them a **small but non-zero constant slope** (commonly 0.01). This guarantees the gradient is **never exactly zero**, so even a unit that's currently producing negative outputs still receives a (small) gradient signal and can, in principle, recover and start contributing again — directly solving the "dead neuron" problem at the cost of one extra hyperparameter (the leak slope).

## "Is ReLU enough?" — the geometric argument (Slides 13–15)

This sequence of three slides builds a beautiful, very exam-relevant geometric intuition for *why nonlinearity actually creates new decision boundaries*, not just "prevents collapse" algebraically.

**Slide 13 — affine maps alone don't help.** If $h = Wx+b$ (no nonlinearity), this is just a **linear/affine transformation of the whole space** — and affine transformations (rotation, scaling, shearing, translation) **preserve linear separability**: if points aren't linearly separable in $x$-space, they remain not-linearly-separable after any affine transform, because a straight line maps to a straight line under an affine map. So a purely linear hidden layer is geometrically powerless to fix a non-linearly-separable problem.

**Slide 14 — adding the ReLU, watching what happens to space.** With $h=\max(0,Wx+b)$, the **negative-half-space of each linear unit gets collapsed onto zero** — every point that would have produced a negative pre-activation for unit 1 gets squashed onto the $h_1=0$ axis (and similarly for unit 2 onto $h_2=0$). This is a genuinely **non-linear, non-invertible folding** of space — points that used to be distinguishable by sign get crushed together at zero.

**Slide 15 — the folding can make data linearly separable.** Because ReLU folds different *regions* of input space onto different "creases," cleverly chosen $W,b$ can use this folding to **rearrange data so that what was a complex, curved decision boundary in $x$-space becomes a simple straight line in $h$-space**. The headline conclusion (the exact phrase to remember): **"A linear classifier in representation space creates a nonlinear classifier in input space."** This is the deep justification for the entire neural-network paradigm: you're not avoiding linear classifiers, you're using a learned nonlinear *folding* of the input space so that a simple linear classifier downstream becomes sufficient.

Let's draw this folding intuition directly, since it's the kind of "see it once and never forget it" diagram:## Terminology you must know cold (Slide 16)

$$f(\mathbf{x};\theta) = W_2\,\mathbf{h}+\mathbf{b}_2 = W_2\phi(W_1\mathbf{x}+\mathbf{b}_1)+\mathbf{b}_2 = \mathbf{s}$$

- $\mathbf{x}$ = **input** (tensor).
- $\mathbf{h}, \mathbf{s}$ = **activations** (intermediate hidden output, and final output/score respectively). $\mathbf{h}$ is called the **hidden layer output**, $\mathbf{s}$ the **output layer**.
- $W_i, \mathbf{b}_i$ = **parameters**.
- Every layer of the form $W\mathbf{x}+\mathbf{b}$ is called a **fully connected (FC) layer**, because **every** element of the input influences **every** element of the output (the weight matrix is "dense" — no structural zeros).
- A neural network with **2 or more layers** is also called a **Multi-Layer Perceptron (MLP)**.

## Depth and width (Slides 17–18)

General $L$-layer network:

$$f(\mathbf{x};\theta) = W_L\mathbf{h}_{L-1}+\mathbf{b}_L = W_L\phi(W_{L-1}\mathbf{h}_{L-2}+\mathbf{b}_{L-1})+\mathbf{b}_L = \ldots = W_L\phi(W_{L-1}\phi(\ldots\phi(W_1\mathbf{x}+\mathbf{b}_1)\ldots)+\mathbf{b}_{L-1})+\mathbf{b}_L$$

- **Depth** = number of layers $L$. **Convention given explicitly in the slide: if $L>2$, the network is considered "deep."** (Memorize this exact threshold — it's the kind of small, precise fact that shows up in true/false exam questions.)
- **Width** = the number of activations computed by each layer, i.e. the length of the vector $\mathbf{h}_i$ at that layer.

---

# Part 3 — Why FC layers fail for images, and the birth of convolution (Slides 19–30)

This is the conceptual heart of the lecture, and almost certainly the most exam-tested section.

## The motivating thought experiment (Slide 19)

Suppose the first FC layer of a network, applied to a flattened image, needs to learn to detect a **local, low-level feature** like vertical edges. What would the weight matrix $W_1$ have to look like for this to happen well?

## Vertical edge detection with an FC layer (Slide 20) — showing how wasteful this is

To detect a vertical edge at *every* location in an $H\times W$ image using a fully connected layer, the weight matrix must, **independently and separately for every output position**, encode the same tiny local pattern: a row of weights like $[-1, 1, 0, 0, \ldots]$ placed at the right offset, repeated over and over for every single output pixel, in every row.

**Cost, as given explicitly in the slide:**
- **Parameters needed**: $H \times W \times H \times (W-1) \approx H^2W^2$
- **FLOPs needed**: $2\times H\times W\times H\times(W-1) \approx 2H^2W^2$
- For a $224\times224$ image: **more than $2.5\times10^9$ parameters** and **more than $5\times10^9$ FLOPs (5 GFLOPs)** — just to detect vertical edges, the simplest possible local feature!

The slide's own framing nails the diagnosis: *"It must learn the same and sparse feature extractor in every row."* The FC layer is forced to **re-learn the identical small pattern independently, over and over, at every spatial location**, wasting enormous numbers of parameters encoding something that is fundamentally the same operation everywhere.

## Convolution/correlation as the fix (Slide 21) — the three defining properties

The slide gives the textbook definition of what makes a convolution structurally different from an FC layer:

1. **Spatial structure preserved**: input and output are *not* flattened — a convolution keeps the image as a 2D (or 3D, with channels) grid throughout.
2. **Local receptive field**: each output unit is connected only to a **small neighborhood** of input units (the kernel's footprint), not to the entire input like an FC layer.
3. **Parameter sharing**: the **same** weights are reused at every output location — the kernel slides across the image, but its values don't change as it moves.

**Conclusion stated directly**: *"Convolutions embody inductive biases dealing with the structure of images: images exhibit informative local patterns that may appear everywhere across an image."* — this is the conceptual justification: since useful visual patterns (edges, textures) are inherently **local** and **translation-repeating** (an edge looks like an edge wherever it occurs), baking those two assumptions directly into the layer's structure is far more parameter-efficient than asking a generic FC layer to discover them from scratch.

## Vertical edge detection via correlation (Slide 22) — the dramatic cost comparison

With a $1\times2$ kernel $[-1, 1]$ correlated across the image:

- **Parameters needed**: just **2** (the two kernel weights $-1, 1$ — *shared* across every position, instead of a fresh pair per position).
- **FLOPs needed**: $3\times H\times(W-1)\approx 3HW$ — for a $224\times224$ image, only **~150K FLOPs**.

Compare: FC layer needed **billions** of parameters and FLOPs; the convolutional approach needs **2 parameters and 150 thousand FLOPs** for the *exact same conceptual task* (detecting vertical edges everywhere in the image). This side-by-side is one of the clearest "why convolution exists" arguments you can give in an exam — make sure you can reproduce both numbers.

## Correlation vs. convolution — the precise mathematical distinction (Slide 23)

This is a frequently-confused point that exams love to test.

**True convolution** (flips the kernel):
$$(I*K)(i,j) = \sum_l\sum_m I(l,m)\,K(i-l,j-m)$$
True convolution is **commutative**: $I*K = K*I$.

**Cross-correlation** (no flip):
$$(K\star I)(i,j) = \sum_l\sum_m K(l,m)\,I(i+l,j+m)$$

**The crucial fact, stated directly in the slide: what neural networks actually use is cross-correlation, not true mathematical convolution** — despite everyone (papers, frameworks, this very lecture) colloquially calling it "convolution." The slide also gives the clean geometric interpretation: at every spatial location, cross-correlation is simply **the dot product between the kernel and the local image patch at that location**.

*(Why does this distinction not matter much in practice? Because the kernel weights are learned anyway — if the network "wants" a flipped kernel, gradient descent will simply learn the flipped version of the weights. The flip is a pure bookkeeping/convention difference, not a representational limitation.)*

## Convolution as matrix multiplication (Slide 24) — an extremely important reframing

If you flatten the input and output, a (1D, for simplicity) convolution with kernel $[w_1, w_2]$ can be written as an explicit ordinary matrix multiplication with a special, highly structured matrix:

$$\begin{bmatrix} w_1 & w_2 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\ 0 & w_1 & w_2 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0&0&0&w_1&w_2&0&0&0&0 \\ 0&0&0&0&w_1&w_2&0&0&0 \\ 0&0&0&0&0&0&w_1&w_2&0 \\ 0&0&0&0&0&0&0&w_1&w_2 \end{bmatrix}$$

This matrix has exactly the same parameters $w_1,w_2$ repeated diagonally — that's parameter sharing made visually explicit. **This matrix is still a linear operator**, with four defining structural properties (this is a direct exam-quotable list):

1. **Shares parameters across its rows** (same $w_1,w_2$ reused diagonally).
2. **Sparse** — each output unit connects only to a small set of neighboring input entries (mostly zeros in each row).
3. **Seamlessly adapts to varying input sizes** — you can extend the matrix (add more rows/columns following the same diagonal pattern) for a bigger input without redesigning anything.
4. **Equivariant to translations of the input** — shifting the input shifts the output correspondingly.

## Equivariance, precisely (Slide 25)

$$T(\mathbf{x}\star K) = (T\mathbf{x})\star K$$

where $T$ is a translation operator. In words: **translating the input and then correlating gives the same result as correlating first and then translating the output** — translating then convolving = convolving then translating.

**Why this matters practically**: it means **you do not need to see a feature (e.g. an edge) at every possible location in your training set to learn to detect it everywhere** — because of parameter sharing + equivariance, learning the kernel from a few examples at a few positions automatically gives you a detector that works at *every* position. This is a massive **data efficiency** win over FC layers, which would need separate training signal for every spatial location independently.

**Important caveat explicitly stated**: *correlation is equivariant to translation, but **not** to rotation or scale.* (A classic exam trap: don't claim CNNs are automatically rotation-invariant — they are not, by the convolution operation alone.)

## Multiple input channels (Slide 26)

A color image has 3 channels, so kernels become 3D tensors of shape $C_{in}\times H_K\times W_K$ (e.g. $3\times5\times5$):

$$(K*I)(j,i) = \sum_{n=1}^{C_{in}}\sum_m\sum_l K_n(m,l)\,I_n(j-m,i-l) + b$$

Important clarifications directly from the slide:
- This is still called a **"2D" convolution**, even though the kernel itself is technically a 3D tensor — **we don't slide over the channel dimension**, only over the two spatial dimensions ($H,W$). The "2D" label refers to the *sliding directions*, not the kernel's dimensionality.
- It computes an **affine function over vector-valued inputs** (a sum across all input channels), and includes a **bias term** $b$.
- **A "5×5 convolution" with 3 input channels actually has $5\times5\times3=75$ parameters (76 with bias), not 25** — the channel dimension is *implicit* in casual naming but always present in the actual parameter count. (This exact "75 not 25" framing is a favorite small-but-precise exam gotcha.)

## Output activation / feature map (Slide 27)

By sliding the filter across the input image, you get a **single-channel output**, called the **output activation**, **feature map**, or **activation map** (all synonyms, used interchangeably — know all three names). At each spatial position $(j,i)$, the value is exactly the dot product between the kernel and the corresponding input patch, plus the bias.

## Multiple output channels (Slide 28)

Repeat the same sliding operation with a **second, independently-learned filter** (e.g. one tuned to horizontal edges instead of vertical), producing a second feature map. Stack filters together to get multiple output channels:

$$K^{(2)} * I(j,i) = \sum_n\sum_m\sum_l K_n^{(2)}(m,l)\,I(j-m,i-l)+b^{(2)}$$

## The full convolutional layer (Slides 29–30) — the general formula to memorize exactly

With $C_{out}$ filters, each of shape $C_{in}\times H_K\times W_K$:

$$(K*I)_k(j,i) = \sum_{n=1}^{C_{in}}\sum_m\sum_l K_n^{(k)}(m,l)\,I_n(j-m,i-l)+b^{(k)}, \qquad k=1,\ldots,C_{out}$$

**Shapes (memorize exactly, in this order — exams test this very directly):**

| Tensor | Shape |
|---|---|
| Input activation | $C_{in}\times H_{in}\times W_{in}$ |
| Conv 2D filter (the whole layer's weights) | $C_{out}\times C_{in}\times H_K\times W_K$ |
| Output activation | $C_{out}\times H_{out}\times W_{out}$ |

Let's visualize the full structural picture of a conv layer with these shapes:## Stacking multiple conv layers (Slide 31)

Just like with FC layers, you need a **nonlinear activation function between** conv layers, or the composition collapses back into a single linear operator (exact same algebraic argument as slide 9, just applied to convolutions instead of FC layers — convolutions, recall, *are* a constrained/structured form of linear layer, so the same "need nonlinearity to avoid collapse" logic applies identically).

---

# Part 4 — The spatial-size arithmetic of convolution (Slides 32–43)

This is the **numerically testable** section — almost guaranteed exam material, and exactly what we covered for AlexNet/VGG/etc. in the architectures lecture, but here it's derived from first principles.

## No padding ("valid" padding) — Slide 32

$$H_{out} = H_{in} - H_K + 1 \qquad W_{out} = W_{in}-W_K+1$$

Example given: $H_{in}\times W_{in}=6\times9$, kernel $3\times3$ → $H_{out}\times W_{out}=4\times7$. **Without padding, the feature map shrinks after every conv layer** — stack enough layers and you eventually run out of spatial size entirely.

## Zero padding ("same" padding) — Slide 33

Add a border of $P$ zeros around the input on each side:

$$H_{out} = H_{in}-H_K+1+2P \qquad W_{out}=W_{in}-W_K+1+2P$$

To get **output size equal to input size** ("same" padding), solve for $P$:

$$P = \frac{H_K-1}{2}$$

(This only divides evenly for **odd** kernel sizes — which is exactly why odd kernel sizes like 3×3, 5×5, 7×7 are so overwhelmingly common in practice; even kernels can't achieve exact "same" padding with a single symmetric integer $P$.)

## Receptive fields without stride (Slide 34)

The **receptive field** of a unit in the $L$-th activation = the set of input pixels that can influence that unit, through the chain of all preceding convolutions.

$$r_L = \Big(1+L(H_K-1)\Big) \times \Big(1+L(W_K-1)\Big)$$

**Key consequence, explicitly stated**: receptive field grows only **linearly** with the number of layers $L$ when there's no downsampling — so to "see" a large portion of the input, you'd need an impractically large number of layers. **This is exactly the motivating problem that pooling/striding/downsampling solves** (covered next): the lecture explicitly states *"to obtain larger receptive fields with a limited number of layers, we down-sample the activations inside the network."*

## Strided convolutions (Slides 35–39)

Instead of sliding the kernel by 1 pixel each step, slide by $S$ pixels (the **stride**). General output-size formula (the master formula, same one we used extensively in the architectures lecture):

$$H_{out} = \left\lfloor\frac{H_{in}-H_K+2P}{S}\right\rfloor + 1 \qquad W_{out} = \left\lfloor\frac{W_{in}-W_K+2P}{S}\right\rfloor+1$$

Worked example from the slides: $H_{in}\times W_{in}=6\times9$, kernel $3\times3$, $P=1, S=2$ → $H_{out}\times W_{out}=3\times5$. The slides literally animate this step by step (output positions 1,2,3,4,5 along the first row, each shifting the kernel 2 pixels at a time) — the mechanical takeaway: **larger stride directly produces smaller output, and is itself a form of downsampling, distinct from pooling.**

## Receptive field WITH stride (Slides 40–41) — the critical exponential-growth result

$$r_L = \left(1+\sum_{l=1}^{L}(H_K-1)\prod_{i=1}^{l-1}S_i\right)\times\left(1+\sum_{l=1}^{L}(W_K-1)\prod_{i=1}^{l-1}S_i\right)$$

If every layer uses the same stride $S$, this simplifies (since $\prod_{i=1}^{l-1}S_i = S^{l-1}$):

$$r_L = \left(1+\sum_{l=1}^{L}(H_K-1)S^{l-1}\right)\times\left(1+\sum_{l=1}^{L}(W_K-1)S^{l-1}\right)$$

**The headline result, stated explicitly and definitely exam-relevant: the receptive field grows *exponentially* with the number of layers when stride $S>1$**, versus only linearly when $S=1$. This is the precise mathematical justification for why architectures use strided/pooled downsampling — it's a vastly more efficient way to grow the effective "field of view" of deep units than simply stacking more stride-1 layers. This directly connects back to the "stem layer" concept from the architectures lecture: stems use early stride>1 operations specifically to grow receptive field fast and cheaply.## Convolution parameters and FLOPs — worked example (Slides 42–43)

This is the **exact** formula set from the architectures lecture, but here's how this lecture derives and presents it (slightly different notation, learn both):

**Setup**: input activation $8\times32\times32$, conv layer $16\times8\times5\times5$ (i.e. $C_{out}=16, C_{in}=8, H_K=W_K=5$), $P=2,S=1$.

**Output size:**
$$H_{out}=W_{out} = \frac{32-5+2\times2}{1}+1 = \frac{31}{1}+1 = 32$$

(stays the same size — exactly "same" padding, since $P=(5-1)/2=2$.)

**Number of learnable parameters:**
$$C_{out}\times(C_{in}\times H_K\times W_K+1) = 16\times(8\times5\times5+1) = 16\times201 = 3{,}216$$

(general formula: $C_{out}(C_{in}H_KW_K+1)$ — the "+1" is the bias **per filter**.)

**Number of values in the output activation:**
$$C_{out}\times H_{out}\times W_{out} = 16\times32\times32=16{,}384 \;(\approx 64\text{KB as float32})$$

**FLOPs**: for each output value, you do a dot product over $C_{in}\times H_K\times W_K = 8\times5\times5=200$ weights, requiring $200$ multiplications + $200$ additions $=2\times200$ FLOPs. The slide makes an important hardware-aside here: **if hardware supports Multiply-ACcumulate (MAC) operations executed in a single clock cycle, complexity is often expressed in MACs instead, dropping the factor of 2** (so "FLOPs ≈ 2×MACs").

$$\text{flops} = C_{out}H_{out}W_{out}\times(C_{in}H_KW_K)\times2 = 16{,}384\times200\times2 \approx 6.5\text{M flops} \;(\approx3.25\text{M MACs})$$

**General formula (memorize):**
$$\text{flops} = 2\,C_{out}H_{out}W_{out}\,C_{in}H_KW_K$$

This is algebraically identical to the formula from the architectures lecture (the architectures lecture additionally multiplies by mini-batch size for the batch total; this lecture states the **per-image** version).

## 1D and 3D convolutions (Slide 44) — generalizing the pattern

**1D convolution** (e.g. for audio, time-series, or 1D signals with $C_{in}$ channels):
$$(K*S)_k(i) = \sum_{n=1}^{C_{in}}\sum_l K_n^{(k)}(l)\,S_n(i-l)+b^{(k)}$$

**3D convolution** (e.g. for video, volumetric/medical data):
$$(K*V)_k(h,j,i) = \sum_{n=1}^{C_{in}}\sum_p\sum_m\sum_l K_n^{(k)}(p,m,l)\,V_n(h-p,j-m,i-l)+b^{(k)}$$

**The pattern across all of these (1D, 2D, 3D)**: you always sum over **all input channels** plus over the spatial extent of the kernel in however many spatial dimensions the data has — the channel dimension is *never* slid over (it's always fully summed/contracted), only the genuinely spatial (or temporal) dimensions get the sliding-window treatment. This is the unifying principle to state if asked to generalize convolution to a new data modality.

---

# Part 5 — Other layers that make up a CNN (Slides 45–53)

The lecture explicitly lists the building blocks of a CNN: **non-linear activation functions, fully connected (linear) layers, convolutional layers, pooling layers, and (batch-)normalization layers.** We've covered activations, FC, and conv. Now pooling and batch norm.

## Pooling layers (Slides 46–47)

### Definition

Pooling **aggregates several values into one output value** using a **pre-specified (not learned)** kernel function — common choices: max, average.

$$I'(j,i) = \max_{k=1,\ldots,C_{out}}\;\max_{l\in[0,W_K-1]}\;pool_k[I][k][(Sj+l,Si+l)]$$

(the formula expresses: for each output channel $k$ and output position $(j,i)$, take the max over the kernel's footprint in the corresponding input region.)

**Hyperparameters**: kernel width/height $H_K\times W_K$, the kernel function (max/avg/etc, fixed not learned), and stride $S$ (usually $>1$, since the whole point is downsampling).

Common default: **2×2, stride 2, max pooling** — exactly halves spatial resolution.


<img width="1226" height="310" alt="image" src="https://github.com/user-attachments/assets/70800d51-3e3b-4194-8912-baf33b995108" />


### The crucial structural difference from convolution

**"Key difference with convolution: each input channel is aggregated independently — the kernel works only along the spatial dimensions, and $C_{out}=C_{in}$."** Unlike a conv filter (which sums *across* channels, mixing them together), a pooling kernel operates **separately, per channel** — it never combines information across different channels, only within a channel's own spatial footprint. This is why pooling cannot change the number of channels (whereas conv routinely does).

### Max pooling worked numeric example (Slide 47/802)

Input single-channel $4\times4$:
```
-1  6  3  2
 0 -1  4  7
 0  0 -2 -1
 0  0  1  0
```
With $2\times2$, $S=2$ max pooling, output is $2\times2$:
```
6  7
0  1
```
(top-left $2\times2$ block max is $6$; top-right block max is $7$; bottom-left block max is $0$; bottom-right block max is $1$.) Verify yourself by hand — this kind of "compute the output of a small pooling example" is a classic short-answer exam question.

### The famous Hinton quote and the pro/con discussion (Slide 47)

The slide includes Geoffrey Hinton's provocative quote: *"The pooling operation used in convolutional neural networks is a big mistake and the fact that it works so well is a disaster."*

The slide then immediately clarifies the *actual* nuance behind that controversy — a genuinely important conceptual point: **downsampling comes from stride, not specifically from pooling — you can achieve the same spatial-size reduction using a strided convolution instead of max pooling.** So pooling is not *required* for downsampling; it's a *choice* with specific trade-offs versus a strided conv:

- **Pro and con simultaneously: pooling has no learnable parameters.** Pro: free, no extra parameters/overfitting risk. Con: it can't adapt or learn — it's a fixed, hand-chosen aggregation rule, the very same "fixed representation" limitation the whole lecture has been arguing *against* throughout (recall Part 1's whole thesis: learned representations beat fixed ones).
- **Pro: invariance to small spatial shifts.** Because max-pooling only cares about the *maximum* value in a region, slightly shifting the input (so the same maximum value lands in a slightly different sub-position within the pooling window) often produces the **exact same output** — giving the network some built-in robustness to small translations/jitter, a property a generic strided conv doesn't automatically have.

---

# Part 6 — Batch Normalization (Slides 48–53)

This is the same Batch Norm material from the previous exam paper, but here it's presented with the **exact original notation and motivation from this specific lecture/course** — let's match it precisely since your prof will grade against this notation.

## Motivation, exactly as the slide frames it (Slide 48)

We know normalizing **input data** to shallow classifiers (e.g. SVMs) — making it live in $[-1,1]$ or have zero-mean/unit-variance (standardization) — is empirically beneficial: it stabilizes training and produces more performant classifiers. The natural approach: compute mean/variance statistics **across the entire training set**, then use them to normalize.

**But here's the subtlety unique to deep networks**, stated precisely in the slide: when the input to a layer (e.g. the final linear classifier) is the representation $\mathbf{h}$ produced by *earlier layers*, **the distribution of $\mathbf{h}$ keeps changing** as $W_1,\mathbf{b}_1$ (the earlier layers' parameters) get updated by SGD at every mini-batch. So:
1. You can't simply compute fixed normalization statistics once over the whole training set up front — they'd go stale immediately as soon as upstream weights update.
2. Even if you tried to compute statistics at some intermediate step, it's **not clear how to prevent optimization from "undoing" the normalization** — i.e., how to make SGD *aware* of the standardization constants so that the act of normalizing doesn't get contradicted/reversed by the next gradient update.

**Batch Norm's solution**: insert an explicit **normalization layer** *inside* the network, computed fresh on **each mini-batch**, with its own **learnable parameters** that participate in backpropagation — so normalization becomes part of the differentiable computation graph itself, rather than an external, disconnected preprocessing step.

## Batch norm at training time — full derivation with this lecture's exact notation (Slides 49–50)

**Input**: mini-batch of activations $\mathbf{a}^{(i)}$, $i=1,\ldots,B$ (batch size $B$), each of dimension $D$.

**Learnable parameters**: $2D$ total — $\gamma_j$ and $\beta_j$ for $j=1,\ldots,D$ (one scale + one shift **per feature dimension**).

**The four differentiable steps:**

**Step 1 — batch mean per feature:**
$$\mu_j = \frac{1}{B}\sum_{i=1}^{B} a_j^{(i)} \qquad \text{shape } 1\times D$$

**Step 2 — batch variance per feature:**
$$v_j = \frac{1}{B}\sum_{i=1}^{B}\left(a_j^{(i)}-\mu_j\right)^2 \qquad \text{shape } 1\times D$$

**Step 3 — normalize:**
$$\hat a_j^{(i)} = \frac{a_j^{(i)}-\mu_j}{\sqrt{v_j+\epsilon}} \qquad \text{shape } B\times D$$

**Step 4 — scale and shift (the learnable reintroduction of flexibility):**
$$s_j^{(i)} = \gamma_j\,\hat a_j^{(i)} + \beta_j \qquad \text{shape } B\times D$$

**Why all four steps being differentiable matters**, stated explicitly in the slide: *"all of them are differentiable and can be backpropagated through: it guarantees that optimization does not 'undo' normalization."* This directly resolves the motivating problem from slide 48 — because the normalization is now wired into the same computation graph that SGD optimizes, gradients correctly flow through $\mu,v,\hat a$ as well, so the network's optimization process is **aware of and consistent with** the normalization, rather than fighting against an external, disconnected preprocessing step.

**A beautiful, exam-quotable consequence**: *"Learning $\gamma_j=\sqrt{v_j}$ and $\beta_j=\mu_j$ may recover the identity function, if it were the optimal thing to do."* In other words, BN doesn't **force** normalization onto the network — it merely **offers** it as an option; the network can always learn to undo it completely if normalization isn't actually helpful at that particular layer/feature.

**Running averages, maintained during training for later use at test time** (momentum $m$, typically $m=0.1$):
$$\mu_j^{(t)} = (1-m)\mu_j^{(t-1)} + m\,\mu_j \qquad v_j^{(t)} = (1-m)v_j^{(t-1)}+m\,v_j$$

## Batch norm at test time (Slide 51)

**Why training-time statistics can't be reused directly at test time**: at test time, *"we do not want to depend stochastically on the other items in the mini-batch — we want the output to depend only on the input, deterministically."*

So mean and variance become **fixed constants** — the **final values** of the running averages accumulated throughout training:

$$\mu_j^{(T)} = \text{final running average from training (constant at test time)}, \quad \text{shape } 1\times D$$
$$v_j^{(T)} = \text{final running average from training (constant at test time)}, \quad \text{shape } 1\times D$$

The test-time formula becomes a **purely deterministic affine transform of the input**, since $\mu^{(T)},v^{(T)},\gamma,\beta$ are all now fixed numbers:

$$s_j^{(i)} = \gamma_j\,\frac{a_j^{(i)}-\mu_j^{(T)}}{\sqrt{v_j^{(T)}+\epsilon}}+\beta_j = \underbrace{\frac{\gamma_j}{\sqrt{v_j^{(T)}+\epsilon}}}_{\text{constant slope}}\,a_j^{(i)} + \underbrace{\left(\beta_j - \frac{\gamma_j\mu_j^{(T)}}{\sqrt{v_j^{(T)}+\epsilon}}\right)}_{\text{constant intercept}} \qquad \text{shape } B\times D$$

**Key practical consequence, explicitly stated**: since this collapses into a fixed linear (affine) transform at test time, **it can be algebraically fused/folded directly into the preceding FC or convolutional layer's weights and biases** — at inference/deployment, you don't need a separate BN computation step at all; you can pre-multiply it into the previous layer's $W,b$, giving **zero extra runtime cost at test time**. This is exactly the "no overhead at test time" pro listed next.

## Pros and cons, exactly as the slide lists them (Slide 52)

**Pros:**
- **Allows the use of higher learning rates.**
- **Careful initialization is less important.**
- **Training is not deterministic, acts as a regularizer** (because batch statistics fluctuate batch to batch, injecting helpful noise).
- **No overhead at test time** — fuses with the previous layer, as derived above.

**Cons:**
- **Not clear why it's so beneficial** — the slide is explicit that, despite being extremely empirically effective, the *theoretical* explanation (originally framed as fixing "internal covariate shift") remains debated/not fully settled, even per the original authors' own framing.
- **Needing to distinguish training vs. test behavior makes implementations more complex** — a real, practical source of many bugs (e.g., forgetting to switch a framework's "model.eval()" mode, accidentally using batch statistics at inference).
- **Does not scale down to "micro-batches"** — i.e., when the batch size is very small (e.g. 1–2 samples), batch statistics become unreliable/noisy estimates, degrading BN's benefit (this connects directly back to the limitation we discussed in your earlier batch-norm question).

## Batch norm for convolutional layers (Slide 53)

| | FC layers | Convolutional layers |
|---|---|---|
| Normalized along | mini-batch dimension only | mini-batch **and spatial** dimensions |
| Activation shape | $a: B\times D$ | $a: B\times C_{out}\times H\times W$ |
| $\mu, v$ shape | $1\times D$ | $1\times C_{out}\times1\times1$ |
| $\gamma,\beta$ shape | $1\times D$ | $1\times C_{out}\times1\times1$ |
| Formula | $s=\gamma\frac{a-\mu}{\sqrt{v+\epsilon}}+\beta$ | $s=\gamma\frac{a-\mu}{\sqrt{v+\epsilon}}+\beta$ (same formula, different broadcast shape) |

Also known as **Spatial Batch Norm** or **BatchNorm2D**. **Why normalize over spatial dimensions too, exactly as the slide explains**: *"the idea is to respect how convolutional layers work: elements of the same feature map [are] processed by the same kernel [and so should be] normalized in the same way."* Since the same kernel/weights produced every spatial position within a given channel (parameter sharing — recall Part 3!), it's consistent to treat all $H\times W$ positions within that channel, across the whole batch, as **samples from the same underlying distribution**, and pool statistics over all of them jointly — exactly matching what we derived in your previous batch-norm exam answer, now traced back to its root justification in convolution's parameter-sharing property.

---

## Quick self-test checklist for this lecture

1. State the "representation learning ≈ deep learning" thesis and explain it using the fixed-vs-learned-representation diagram contrast.
2. Reproduce the algebraic proof that stacking linear layers without activation functions collapses to one linear layer (for both FC and conv).
3. Compare sigmoid vs ReLU vs Leaky ReLU: formulas, gradients, vanishing gradients, dead neurons.
4. Explain, geometrically, why ReLU's "folding" of space can make non-linearly-separable data linearly separable in the hidden representation.
5. Derive, from scratch, why an FC layer is wildly parameter-inefficient for detecting local image features (the $H^2W^2$ vs $HW$ comparison), and state the 3 structural properties of convolution that fix this (local receptive field, parameter sharing, preserved spatial structure).
6. Define cross-correlation vs. true convolution precisely, and know which one neural networks actually use.
7. State convolution's 4 properties as a (structured) linear operator: parameter sharing, sparsity, size-adaptivity, equivariance to translation (and the explicit caveat: NOT equivariant to rotation/scale).
8. Compute, from raw formulas, the output size, #params, and #flops of any given conv layer, with and without padding/stride.
9. Derive and explain why receptive field grows linearly without stride but exponentially with stride — and connect this to why downsampling exists.
10. Explain max pooling: how it differs structurally from convolution (per-channel only, $C_{out}=C_{in}$, no parameters), compute a worked numeric example, and discuss the Hinton-quote pros/cons (shift invariance vs. no learnable parameters; remember pooling ≠ the only way to downsample).
11. Derive batch norm fully: the four training-time steps with exact shapes, why test-time needs fixed running statistics instead, why BN fuses into the previous layer at test time, and the full pros/cons list. Know the conv-layer (spatial) variant and why it normalizes over H,W too.

