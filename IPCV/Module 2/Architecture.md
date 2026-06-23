

This lecture traces the evolution of CNN architectures for image classification, from LeNet5 (1998) to ResNet (2015), using the ImageNet competition (ILSVRC) as the timeline. The narrative arc is important for the exam: **each architecture solves a specific problem with the previous one.** If you understand *why* each architecture was invented (not just *what* it looks like), you'll be able to answer any conceptual exam question.

Let me set up the visual roadmap first, then go layer-by-layer through the math, then architecture-by-architecture through the ideas.Now let me build the visual map of the whole lecture's progression, then walk through every section in depth.Now let's go through every concept in deep, exam-ready detail.

---

## 1. The generic CNN architecture (Slide 2)

A CNN classifier is built from **two functional blocks**:

1. **Feature extractor**: a stack of *N* repeated blocks, each block usually `Conv2D → (ReLU) → MaxPool`. Notice the slide's small parenthetical remark: *"with max-pool, ReLU can be the last operation in a block"* — meaning the order Conv→ReLU→Pool and Conv→Pool→ReLU are functionally similar in many implementations, but the convention shown is Conv→Pool→ReLU per the diagram ordering (2D Conv, Max-Pool, ReLU stacked).
2. **Classifier**: *M* fully connected (FC) layers at the end, after a **flatten** operation that turns the final 3D activation tensor into a 1D vector.

The notation used: $h_3 \to \phi(W_4 h_3 + b_4) \to h_4 \to W_5 h_4 + b_5 \to s$

- $h_i$ = activation (hidden state) after layer $i$
- $W_i, b_i$ = weight matrix and bias of layer $i$
- $\phi$ = nonlinearity (e.g. ReLU)
- $s$ = final score vector (logits) — notice **no nonlinearity** on the very last layer; it outputs raw scores, since softmax/loss is applied outside the network.

**Key exam point:** the last FC layer is called the **classifier** (produces class scores), while everything before flatten is the **feature extractor** (produces a vector representation, an "embedding," of the image).

---

## 2. LeNet5 (Slide 3) — the historical baseline

This is your reference point for "what didn't exist yet" in 1998:

- **Channels increase, spatial size decreases with depth** — this trend holds in *every* CNN you'll study. It's the fundamental geometric design of CNNs: trade spatial resolution for semantic channels.
- **Average pooling**, not max pooling (max pooling becomes standard later).
- **5×5 kernels, no padding** → this means every conv layer *shrinks* the spatial size (since there's no zero-padding to compensate).
- **Sigmoid/tanh nonlinearities** — pre-ReLU era. These saturate (gradients vanish at extremes), which is part of why training very deep nets with these was hard.
- **RBF (Radial Basis Function) classifier** at the very end instead of a plain softmax — an old-fashioned touch.
- **No residual connections, no (batch) normalization** — both didn't exist yet (BatchNorm: 2015, ResNet: 2015/2016).

This slide is essentially a checklist of "missing ingredients" that later architectures will each introduce one by one.

---

## 3. ILSVRC error evolution (Slide 4)

This chart is the **spine of the whole lecture**. ImageNet Top-5 error rate over years:

| Year | Model | Top-5 error |
|---|---|---|
| 2010 | — | 28.1% |
| 2011 | — | 25.8% |
| 2012 | AlexNet | 16.4% |
| 2013 | ZFNet | 11.7% |
| 2014 | VGG | 7.4% |
| 2014 | Inception-v1 | 6.7% |
| 2015 | ResNet | 3.6% |
| 2016 | ResNeXt | 3.03% |
| 2017 | SENet | 2.3% |

**Important caveat the slide makes**: these numbers are *"based on ensembles and, sometimes, heavy test-time augmentation"* — meaning the headline numbers you see in papers are usually **not** a single model's single-pass error. They often combine multiple trained models (ensembling) and multiple crops/transformations of the test image averaged together. If an exam question asks "is AlexNet's reported error the error of one single network on one image crop," the answer is generally **no** — be ready to mention this caveat.

**Top-5 error**, by the way, means: the true label is *not* among the model's top 5 predicted classes. It's a more forgiving metric than top-1 error, often used because ImageNet has many semantically similar/overlapping classes.

---

## 4. AlexNet (Slides 5–6) — the architecture that started it all

### Structure
- **5 convolutional layers** (conv + ReLU), some optionally followed by max-pooling.
- **3 FC layers** at the end.
- **Group convolutions**: AlexNet was trained on **two GTX580 GPUs**, and to split the computational load, certain conv layers were split into two parallel groups of half the channels each, computed on separate GPUs, that only periodically communicate. This is a *practical engineering hack*, not a fundamental architectural principle — but it's the origin of "grouped convolutions" later reused in other architectures (e.g., ResNeXt).

### Key historical/practical facts (exam-likely trivia)
- Won **ILSVRC 2012**.
- Trained on two GTX580 GPUs, took **5–6 days**.
- Used **Local Response Normalization (LRN)** — a now-abandoned normalization scheme (predates BatchNorm), used in some layers; **not used in later architectures**.
- Famous quote: results would improve simply with faster GPUs/bigger datasets — foreshadows the entire decade of scaling.
- ReLU was a major contributor to its success (faster training than sigmoid/tanh, mitigates vanishing gradients in the *positive* regime).

---

## 5. The Architecture Breakdown Table — THE most important methodological section

This is the part of the lecture an exam will almost certainly test numerically. You need to be able to **compute, from scratch, for any conv/pool/FC layer**: output spatial size, number of activations, number of parameters, FLOPs, and memory. Let's build every formula with full derivation and worked example, exactly as the slides do, but explained more carefully.

### 5.1 Setup notation
- $W_{in}, H_{in}$: input width/height (spatial size)
- $C_{in}$: input channels
- $W_K, H_K$: kernel width/height
- $S$: stride
- $P$: padding (per side)
- $C_{out}$: number of output channels = number of kernels (filters)

### 5.2 Output spatial size formula

$$\text{Activation H/W} = \left\lfloor \frac{W_{in} - W_K + 2P}{S} \right\rfloor + 1$$

This is the **single most important formula in CNN architecture math**. Memorize it cold. Intuition: you slide a $W_K \times W_K$ window across the (padded) input of size $W_{in} + 2P$, moving $S$ pixels at a time; the "+1" accounts for the starting position.

**Worked example (AlexNet conv1):** input 227×227, kernel 11×11, stride 4, padding 0 (note: the original paper says 224 but the standard breakdown actually uses 227 to make the math come out as an integer — this is a well-known subtlety/quirk of AlexNet you might get asked about):

$$\frac{227 - 11 + 0}{4} + 1 = \frac{216}{4} + 1 = 54 + 1 = 55$$

✓ matches the table (55×55).

**Worked example (pool1):** input 55, kernel 3, stride 2, padding 0:
$$\frac{55-3+0}{2}+1 = \frac{52}{2}+1 = 26+1=27$$ ✓

### 5.3 Number of activations
$$\#\text{Activations} = H_{out} \times W_{out} \times C_{out}$$
(per single image; the table multiplies by mini-batch size later when computing memory)

For input layer: $227 \times 227 \times 3 = 154{,}587$.
For conv1: $55 \times 55 \times 96 = 290{,}400$ ✓.

### 5.4 Number of parameters (conv layer)

$$\#\text{params} = (W_K \times H_K \times C_{in} + 1) \times C_{out}$$

Intuition: each output channel/filter has its own set of weights connecting to **all** input channels over the $W_K \times H_K$ spatial window, **plus one bias** per output channel. You multiply by $C_{out}$ because there are that many independent filters.

**Worked example (conv1):** $(11 \times 11 \times 3 + 1) \times 96 = (363+1) \times 96 = 364 \times 96 = 34{,}944 \approx 35K$ ✓ (table shows 35, in thousands).

This is exactly why **pooling layers have zero parameters** — they don't have learnable weights, just a fixed operation (max or average).

### 5.5 FLOPs (floating point operations) for a conv layer

$$\text{flops} = \text{minibatch-size} \times \#\text{activations} \times (W_K \times H_K \times C_{in}) \times 2$$

Intuition breakdown:
- For **each output activation** (each spatial position × each output channel), you compute a dot product over $W_K \times H_K \times C_{in}$ input values with the corresponding weights.
- A dot product of length $n$ takes $n$ multiplications + $n$ additions = $2n$ FLOPs (this is the standard convention: 1 MAC = 2 FLOPs).
- Multiply by the number of output activations (since you do this dot product once per output element) and by mini-batch size (you do this for every image in the batch).

**Worked example (conv1):** $290{,}400 \times (11 \times 11 \times 3) \times 2 = 290{,}400 \times 363 \times 2 \approx 211$ million flops per image... but the table reports **per mini-batch** of 128: $290{,}400 \times 363 \times 2 = 210{,}710{,}400$ — wait, let's check against the slide's own number: the slide says $= 290{,}400 \times (11 \times 11 \times 3) \times 2 = 27$ Gflops. That 290,400 already represents the *per-image* activation count, so:

$$\text{flops (per image)} = 290{,}400 \times 363 \times 2 = 210.9M$$

Then for the full mini-batch of 128: $210.9M \times 128 \approx 27{,}000M = 27$ Gflops ✓. **So the formula already bakes in mini-batch size as a multiplier on top of the per-image activation count** — the slide's flops column reports the **mini-batch total**, not per-image.

### 5.6 FLOPs for pooling layers

$$\text{flops} = \#\text{activations} \times W_K \times H_K$$

No factor of 2 here (no multiply-accumulate, just comparisons for max-pool, or sums for avg-pool — and notably this formula as written doesn't even multiply by mini-batch size in the slide's pool1 example, since pooling is so cheap it's often treated as negligible/just illustrating the per-image base count before scaling).

**Worked example (pool1):** $\#\text{activations}=69{,}984$ (this is per-image: $27\times27\times96$), $W_K \times H_K = 3\times 3=9$:
$$69{,}984 \times 9 = 629{,}856 \approx 0.63M\text{ flops (per image)}$$
Scaled by mini-batch 128: $\approx 80.6M$ ✓ matches table.

### 5.7 Memory for activations

$$\text{Activation memory (MB)} = 2 \times \text{minibatch-size} \times \#\text{activations(per image)} \times \frac{4\text{ bytes}}{1024^2}$$

Two key facts buried here:
- **Factor of 4 bytes**: activations are stored as 32-bit floats.
- **Factor of 2**: at **training time** you must store both the activation **and** its gradient (same-sized tensor) for backprop. This is explicitly explained on slide 10: *"We need to store all intermediate activations to compute the gradient... another tensor of the same size."*

**Worked example (conv1):** $2 \times 128 \times 290{,}400 \times 4 / 1024^2 = 283.6$ MB ✓.

**Worked example (input):** Note the input layer does *not* get the factor of 2 — the slide computes it as $128 \times 154{,}587 \times 4/1024^2 = 75.5$ MB. Why no ×2? Because **you don't backpropagate a gradient with respect to the input image itself** in standard classification training (the input has no learnable parameters before it, so there's nothing upstream to update) — so only one copy of input activations needs to be stored, not an activation+gradient pair. This is a subtle but testable distinction.

### 5.8 Memory for parameters

$$\text{Params memory (MB)} = 3 \times \#\text{params} \times \frac{4\text{ bytes}}{1024^2}$$

Why **×3** and not ×2 like activations? Per slide 10's explanation: for every parameter you need:
1. Its value
2. Its gradient
3. **An optimizer state term** (e.g. momentum velocity, or for Adam, first/second moments — which would actually need ×4, but the slide uses ×3 as the simplified standard estimate, e.g., covering value + gradient + one momentum term)

**Worked example (conv1):** $3 \times 34{,}944 \times 4 / 1024^2 \approx 0.4$ MB ✓.

The slide is explicit that **this is a lower bound**, an approximation: *"Hard to have a precise estimate... we can get approximate values by considering twice the activation size and 3-4 times the #params."*

### 5.9 The flatten layer — special case

Flatten has:
- **0 parameters** (no learnable weights)
- **0 additional memory** — it's literally a *view* / reinterpretation of the same memory buffer, reshaping a $C \times H \times W$ tensor into a $(C \times H \times W) \times 1$ vector, **no copy needed**.
- This is conceptually important: flatten doesn't transform data, it just **reinterprets the indexing**.

### 5.10 FC layers — formulas

**Parameters:**
$$\#\text{params} = C_{out} \times C_{in} + C_{out}$$
(weight matrix $C_{out} \times C_{in}$, plus one bias per output unit). Note: this is the **same formula as a conv layer with $W_K = H_K = 1$** — and that's exactly the conceptual link the lecture is building toward (an FC layer = special case of 1×1 conv with no spatial extent).

**Worked example (fc6):** input is the flattened $9216$-d vector, output 4096:
$$4096 \times 9216 + 4096 = 37{,}752{,}832 + ... $$
wait let's recompute precisely: $4096 \times 9216 = 37{,}748{,}736$, plus $4096$ bias terms $= 37{,}752{,}832 \approx 37{,}758K$ (table rounds slightly, but matches ✓).

**FLOPs:**
$$\text{flops} = \#\text{minibatch} \times 2 \times C_{in} \times \#\text{activations(out, per image)}$$

**Worked example (fc6):** $128 \times 2 \times 9216 \times 4096 \approx 9.66$ Gflops ✓ matches table.

### 5.11 The grand totals and the trends (Slide 19–20) — **memorize these conclusions**

For AlexNet (mini-batch 128):
- **62.4 million parameters**
- **~290 Gflops** total for the mini-batch → **2.2 Gflops/image**
- **1.4 GB** activation memory, **714 MB** parameter memory

**The five "trends to note" — these are exam gold, likely to be asked verbatim:**

1. **Stem layer** at the beginning of the network — a layer that aggressively reduces spatial size early (large kernel/stride) to control cost and grow receptive field fast.
2. **Nearly all parameters live in the FC layers** (37.7M + 16.8M + 4.1M ≈ 58.6M out of 62.4M total — i.e. ~94%!). Convolutions are comparatively parameter-light per layer, since weights are *shared* across spatial positions, while FC layers have one full weight per (input,output) pair with no sharing.
3. **Activation memory is dominated by the first conv layers** — because spatial resolution is still large there (55×55, 27×27), even though channel count is modest.
4. **FLOPs are dominated by conv layers** — because FLOPs scale with $H \times W \times C_{in} \times C_{out} \times K^2$, and even though conv layers have fewer parameters, they reuse those parameters at every spatial location, multiplying the compute enormously.
5. **Activations and parameters have similar memory footprint at training time** in AlexNet specifically (~1.4GB vs ~0.7GB — same order of magnitude, not negligible relative to each other).

This parameters-vs-flops dichotomy (**FC layers: many params, few flops; conv layers: few params, many flops**) is one of the most important conceptual takeaways of the entire lecture, and a classic exam question.

---

## 6. ZFNet / Clarifai (Slide 21)

- Same overall AlexNet-like structure, but its main *contribution* is methodological, not just architectural: they built **visualization tools (Deconvnets)** to actually look at what each layer's filters/activations represent — moving network design away from pure trial-and-error.
- Their key empirical finding via these visualizations + ablations: **AlexNet's first layer (11×11, stride 4) is too aggressive** → causes "dead filters" (filters that never activate meaningfully), missing frequency information, and **aliasing artifacts** in the second layer.
- **Fix**: smaller, gentler stem — use **7×7 conv with stride 2** in layer 1 (instead of 11×11 stride 4), and also use **stride 2** in the second 5×5 conv layer (spreading the spatial downsampling more gradually instead of doing it all at once in layer 1).
- This is the conceptual seed of the **"stem layer" design lesson**, later explicitly reused and refined by GoogLeNet and ResNet: *don't crush spatial resolution too violently in one shot — downsample gradually with more, smaller-stride layers.*

---

## 7. VGG (Slides 22–24)

### Philosophy
VGG's whole point is an **ablation/regularity argument**: instead of hand-designing different kernel sizes per layer (like AlexNet/ZFNet), restrict the entire network to only two primitive choices:
- **3×3 convolutions**, stride 1, padding 1 (preserves spatial size)
- **2×2 max-pooling**, stride 2, padding 0 (exactly halves spatial size)
- **Double the number of channels after every pooling step**

This simplicity makes the architecture "regular" and easy to reason about, and it was a deliberate experiment to show that **depth + simple uniform components** can outperform hand-crafted heterogeneous kernels.

### Other facts
- Got **2nd place** in ILSVRC 2014 (Inception v1 got 1st), 7.5% top-5 error.
- **Dropped LRN**.
- **No batch norm yet** (BN wasn't invented until 2015) — so VGG had a serious training problem: very deep configs (16, 19 layers) couldn't be trained from random initialization directly. Solution at the time: **pre-train a shallower network first, then initialize the deeper network's early layers with those weights** ("layer-wise" warm starting) — this trick became unnecessary once smart initialization schemes (e.g. Xavier/He init) and later BatchNorm arrived.
- VGG-16 and VGG-19 differ in the number of conv layers per stage (the **D** and **E** columns in the table on slide 22) — VGG-19 has more 3×3 convs added to certain stages compared to VGG-16.

### The concept of "Stages" (Slide 23) — important abstraction

A **stage** = a group of layers operating at the **same spatial resolution**, ending in a pooling layer that halves resolution. VGG stages are one of: conv-conv-pool, conv-conv-conv-pool, or conv-conv-conv-conv-pool.

**Why stack multiple small convs instead of one big one?** Slide 23's table compares:

| Option | Params | Flops | #ReLUs | #Activations stored |
|---|---|---|---|---|
| One $C\times C \times 5\times5$ conv | $25C^2+C$ | $50C^2 W H$ | 1 | $C \times W \times H$ |
| Two stacked $C\times C\times3\times3$ convs | $18C^2+2C$ | $36C^2WH$ | 2 | $2 \times C\times W\times H$ |

**Key insight (very testable):** two stacked 3×3 convs have the **same receptive field** as one 5×5 conv (because a 3×3 conv followed by another 3×3 conv "sees" a 5×5 region of the original input — receptive fields compose additively: $RF = k_1 + k_2 - 1 = 3+3-1=5$). But the two-3×3 version:
- Uses **fewer parameters**: $18C^2$ vs $25C^2$ (for large $C$).
- Uses **fewer flops**: $36C^2WH$ vs $50C^2WH$.
- Has **more nonlinearities** (2 ReLUs instead of 1) → more expressive power, since you interleave nonlinear transformations rather than doing one big linear-ish operation.
- **"No free lunch"**: it **doubles the activation memory** you need to store at training time (you have an extra intermediate tensor of full size $C\times W\times H$ to keep for backprop) — this is the cost of the efficiency gain. This trade-off (fewer params/flops, but more memory) is a recurring theme and definitely worth remembering as a general principle: **decomposing one large operation into several smaller ones often saves params/flops at the cost of extra memory and more sequential computation.**

### VGG-16 summary numbers (Slide 24)
- **138M params** (≈2.3× AlexNet), again **mostly in FC layers**.
- **~4 Tflops** (~14× AlexNet), **31 Gflops/image**, dominated by convolutions.
- **~16.5 GB memory** (~12× AlexNet) — dominated by activations, specifically because of the **early conv layers without a stem layer** — VGG keeps full 224×224, then 224×224 again before the first pool, so those first activations are huge (3136 MB each for conv1/conv2!) compared to AlexNet's stem-shrunk first layer.
- Trained on **4 GPUs, data parallelism, 2–3 weeks**.

---

## 8. Inception v1 / GoogLeNet (Slides 25–32)

### The big idea
Quote from the paper, worth memorizing: *"The main hallmark of this architecture is the improved utilization of the computing resources inside the network... allows for increasing the depth and width of the network while keeping the computational budget constant."*

Architecture = **Stem layers** (similar idea to ZFNet's gentle downsampling) → **stack of Inception modules** → **Global Average Pool + classifier**.

- 22 "trainable layers" counted along the main path, but **~100 layers overall** if you count every branch inside every Inception module separately.

### Stem layers (Slide 26)
- Downsamples aggressively but **gently and gradually**: 224 → 28 in only 5 layers, using **only stride-2 operations** and a **largest kernel of 7×7** (learning directly from the ZFNet lesson — no giant 11×11 stride-4 jump).
- Cost: ~130 Gflops, 124K params, ~2GB memory for the *whole stem*.
- Comparison: VGG needs **10 layers** to reach the same 28×28 resolution, and that costs **2.4 Tflops, 1.7M params, 13GB memory** — i.e., the stem-based gradual downsampling is **dramatically cheaper** than VGG's uniform full-resolution stacking. This comparison is a strong illustration of *why stems matter*.

### Naïve Inception module (Slide 27) — the problem

The core idea of "Inception" is: instead of choosing one kernel size per layer (3×3 *or* 5×5 *or* 1×1), run **several different operations in parallel on the same input** and **concatenate** their outputs along the channel dimension. This lets the network learn which receptive field sizes matter at each stage, instead of the architect guessing.

Naïve module branches (all applied to the same $28\times28\times192$ input):
- 1×1 conv → 64 channels
- 3×3 conv (pad 1) → 128 channels
- 5×5 conv (pad 2) → 32 channels
- 3×3 max-pool (pad 1, stride 1) → preserves 192 channels (pooling doesn't change channel count!)

Concatenated output: $64+128+32+192 = 416$ channels.

**Two problems identified:**
1. **Channel explosion**: because the max-pool branch passes through the *full* 192 input channels untouched, every time you stack inception modules, channel count snowballs upward very fast (since concatenation only adds channels, never reduces them via the pooling branch).
2. **Computational cost**: large convolutions (3×3, 5×5) applied directly on a high channel-count input (192) are expensive: the slide computes $5\times5$ conv cost $\approx 240$ Mflops and $3\times3$ conv cost $\approx 350$ Mflops for *just one module* — and this compounds catastrophically if you stack many such modules.

### The fix: 1×1 convolutions (Slide 28) — bottleneck trick

**What is a 1×1 convolution, conceptually?** It has *no spatial extent at all* — its kernel only looks at a single pixel location, but across *all* input channels. So at each spatial location, it's literally just **a linear (fully-connected) transformation applied independently to the channel vector at that pixel**: take the $C_{in}$-length vector at one pixel, multiply by a $C_{out}\times C_{in}$ weight matrix + bias, get a $C_{out}$-length vector. If you stack several 1×1 convs (with nonlinearities between), you're literally running an **MLP applied identically at every spatial location** (this is the "Network in Network" idea, cited as Lin et al. ICLR 2014).

**Why it's useful here:** a 1×1 conv lets you **cheaply change channel depth** (compress or expand $C$) **without touching spatial size**. This gives architects a "dial" to control computational cost independent of spatial resolution.

### Inception module with dimension reduction (Slide 29)

Now each expensive branch gets a 1×1 conv **bottleneck** first, to *shrink* the channel count before the expensive spatial conv:
- 1×1 conv → 64 (this branch, by itself, *is* one of the parallel outputs)
- 1×1 (→96) then 3×3 conv → 128
- 1×1 (→16) then 5×5 conv → 32
- 3×3 max-pool, then 1×1 conv (→32) to *control* the pooling branch's channel count too (this also fixes problem #1 — channel explosion — since now even the pooling path is compressed)

Result: output is $64+128+32+32=256$ channels — much more controlled.

**Recomputed cost with bottleneck**, exactly as the slide shows:
- 5×5 branch: $28\times28\times16\times192\times2$ (the 1×1 reduction) $+ 28\times28\times32\times16\times5\times5\times2$ (the 5×5 conv on the *reduced* 16 channels) $\approx 5M + 10M = 15M$ flops — vs. **240M** before. That's a **~16× reduction**.
- 3×3 branch: similarly drops from 350M to ~202M flops.

This is the central lesson of Inception modules: **use 1×1 convs as cheap "bottlenecks" to control channel dimensionality before expensive operations** — a pattern reused everywhere afterward (including ResNet's bottleneck block, covered later).

### Global Average Pooling vs FC classifier (Slides 30–31)

This addresses the "nearly all parameters are in the FC layers" problem we saw in AlexNet/VGG.

**Idea (from Network-in-Network):** instead of flattening the final feature map and feeding it to a big FC layer (which needs $C\times H\times W \times \text{num\_classes}$ parameters), just **average each channel's spatial map down to a single number** — Global Average Pooling (GAP) — producing a $C$-length vector, then apply **one small FC layer** ($C \times \text{num\_classes}$ params) directly on that.

**Quantitative comparison (Slide 31):**
- GoogLeNet's GAP + 1 FC layer: **~1 million parameters total**, negligible flops.
- VGG's three FC layers: **124 million parameters**, requiring **31 Gflops**.

This single change explains why GoogLeNet, despite being "deeper," ends up with **far fewer total parameters** than VGG (7M vs 138M) — confirming the lecture's broader point that **FC layers, not depth, are usually where parameter count balloons.**

**Practical PyTorch note** the slide makes: using `AdaptiveAvgPool2d` (which computes the pooling kernel size automatically based on input size) instead of a fixed-size `AvgPool2d` makes the network **size-agnostic** — it can process input images of *any* spatial resolution, not just the one used at training time. This is a genuinely useful practical fact for an exam.

### GoogLeNet summary (Slide 32)
- **~7 million parameters**, **390 Gflops** (3 Gflops/image), **~3.3 GB** memory.
- **10.07% top-5 error** with a single model + single crop; **7.89%** with one model + aggressive multi-crop test-time augmentation (144 crops) — this nicely illustrates the "ensembles/augmentation" caveat from slide 4: test-time tricks meaningfully move the needle.

Comparing all three so far is a great mental table for the exam:

| Model | Params | Flops/img | Memory | Where most params live |
|---|---|---|---|---|
| AlexNet | 62M | 2.2 Gflops | 1.4GB act + 0.7GB params | FC layers (~94%) |
| VGG-16 | 138M | 31 Gflops | ~16.5GB | FC layers |
| GoogLeNet | 7M | 3 Gflops | ~3.3GB | Spread across conv/inception (GAP kills FC cost) |

---

## 9. Inception v3 (Slide 33) — brief mention

Key idea: **factorize convolutions** further to reduce params/flops while keeping the same receptive field, similar in spirit to the VGG "stages" 3×3-stacking trick but pushed further:
- **Factorization A** (used at fine spatial scale, 35×35): splits a larger conv into parallel smaller-kernel branches.
- **Factorization B** (mid-scale, 17×17): uses **asymmetric** convolutions — $n\times1$ followed by $1\times n$ — to factorize a $n\times n$ conv into two cheaper 1D convolutions (this is the same logic as the 5×5 → two 3×3 trick, generalized: an $n\times n$ conv can be replaced by a $1\times n$ conv followed by an $n\times 1$ conv, drastically reducing params from $O(n^2)$ to $O(n)$, per channel).
- **Factorization C** (coarse scale, 8×8): even more aggressive parallel asymmetric splitting.

Result: **4.48% top-5 error** with 12-crop testing. The slide's overarching message: **smaller/fewer parameters → easier optimization ("more disentangled," easier to train) and better efficiency**, not just a side effect.

---

## 10. Residual Networks / ResNet (Slides 34–47) — the deepest conceptual section

### 10.1 The problem ResNet solves (Slide 34)

**Empirical observation from VGG:** depth helps... up to a point. But naively stacking more layers **does not monotonically improve performance** — and crucially, **training error also increases** with depth (not just test/validation error). This rules out "overfitting" as the sole explanation, since overfitting would show *low* training error but *high* test error — here **both go up**. So there's a genuine **optimization problem**: SGD struggles to train very deep "plain" networks well, even with Batch Norm already in place.

**The constructive existence proof:** if a 20-layer network achieves performance $X$, you can in principle build a 56-layer network that's *at least as good*, simply by setting the extra 36 layers to compute the **identity function** (pass input through unchanged). So a deep network should never be worse, in principle. But **SGD fails to find this trivial identity solution** using the standard parameterization of layers (a plain stack of weight layers learning $H(x)$ directly does not easily converge to $H(x) = x$).

### 10.2 The residual block solution (Slide 35)

**Fix: reparameterize what each block learns.** Instead of forcing a block to learn the *full* mapping $H(x)$, let it learn the **residual** (the difference): $F(x) = H(x) - x$, and explicitly **add back $x$** via a skip connection:

$$\text{output} = F(x) + x$$

Structure of one residual block: `Conv2D → BN → ReLU → Conv2D → BN`, then **add the original input $x$**, *then* apply the final ReLU.

**Why this fixes the optimization problem:**
- Weights are typically initialized near zero (biases exactly zero), so initially $F(x) \approx 0$, meaning the block starts out **already computing the identity function** $x \to x$ almost automatically — there's no longer a hard optimization problem of *discovering* identity from scratch; it's the network's *default starting point*.
- The network now just needs to learn a small **"perturbation"** on top of identity, which is generally an easier optimization target than learning the whole transformation from scratch.
- Heavy use of **batch normalization** throughout, which by 2015 had become standard.

### 10.3 Overall ResNet design (Slide 36)

Inspired by VGG's "stages" philosophy:
- Network = stack of **stages**, each stage = stack of residual blocks.
- Each residual block = two stacked 3×3 convs + BN (as above).
- **First block of each new stage**: halves spatial resolution (via stride-2 conv) **and** doubles channel count — exactly matching VGG's "channels double after each pool" rule, but achieved through a stride-2 conv rather than a separate pooling layer.
- Uses a **stem layer** + **global average pooling** at the end, both borrowed directly from GoogLeNet.
- **Naming convention** (also borrowed from VGG): "ResNet-X" where X = number of layers with learnable weights (e.g. ResNet-18, ResNet-50).

### 10.4 Stem layer specifics (Slide 37)
- Just **one conv + one pool** layer (simpler than GoogLeNet's 5-layer stem), reducing only down to 56×56 (less aggressive than GoogLeNet's 28×28) — the slide's hypothesis: because **residual blocks themselves are lightweight** (compared to GoogLeNet's heavier multi-branch Inception modules), ResNet doesn't need as drastic an early reduction to keep total cost manageable.
- Ends with the same GAP + single linear-layer classifier pattern.

### 10.5 The dimension-matching problem (Slide 38) — important detail

The simple "add $x$ to $F(x)$" trick **only works when $x$ and $F(x)$ have the same shape**. But at the start of a new stage, the spatial size halves and channels double — so the skip connection's $x$ no longer matches the main branch's output shape. **Two solutions the authors tried:**

1. **Zero-padding + stride**: apply a stride-2 "identity-like" sampling to $x$ to match spatial size, and zero-pad the channel dimension to match the new (doubled) channel count. **No extra parameters.**
2. **1×1 conv with stride 2** and $2C$ output channels on the skip path — this *does* add a few parameters but lets the network *learn* the best projection rather than being forced into a fixed zero-padding scheme.

**Empirical finding: option 2 (learned projection) performs slightly better.** This is the "solid arrow" path in ResNet diagrams (versus a plain "dashed arrow" identity skip used within a stage where shapes already match).

### 10.6 Results (Slide 39)

- With residual connections, deeper networks (56-layer) now **outperform** shallower ones (20-layer) on both training and test error — confirming that residual blocks indeed solve the optimization issue, not just an overfitting issue.
- Won **all five main tracks** of the 2015 ILSVRC & COCO competitions by large margins (ImageNet classification with a 152-layer net described by Yann LeCun as *"ultra-deep"*; large improvements in detection/localization/segmentation too).
- Still **the standard baseline/backbone** referenced in this lecture as of writing (and broadly still true in practice as a default choice even today).

### 10.7 Bottleneck residual block (Slide 40) — efficiency variant

For *very* deep ResNets, the plain "two 3×3 convs" block becomes expensive at high channel counts. The **bottleneck block** structure:

`1×1 conv (C→C/4 reduction, i.e., here written as going from 4C down to C) → 3×3 conv (C→C) → 1×1 conv (C→4C expansion)`

Cost comparison (per the slide's formulas, in terms of base channel width $C$):
- **Basic block** (two 3×3 convs at width $C$): $36C^2HW$ flops, $18C^2$ params.
- **Bottleneck block** (1×1 reduce + 3×3 + 1×1 expand, where the "outer" width is $4C$): $34C^2HW$ flops, $17C^2$ params.

**Punchline: roughly the same total cost, but it lets you increase depth (more layers) without increasing the computational budget** — exactly the GoogLeNet philosophy of using 1×1 convs as a cheap dial to control cost while adding more representational depth. Bottleneck blocks are used in the *deeper* ResNet variants (ResNet-50/101/152).

### 10.8 Visualizing why residual learning helps (Slide 41)

A loss-landscape visualization (Li et al. 2018) shows: **without skip connections**, the loss surface of a 56-layer network is **jagged, chaotic, full of sharp local structure** — hard for gradient descent to navigate. **With skip connections**, the same network's loss surface is **smooth and convex-like** near the minimum — much easier for SGD to optimize. This is a nice intuitive/visual confirmation of "why" residual connections help beyond the identity-function argument.

### 10.9 ResNets as ensembles of shallow networks (Slide 42)

A follow-up theoretical analysis (Veit et al. 2016): if you "unravel" a residual network with $n$ blocks, you can view it as an implicit **sum over $2^n$ different possible paths** through the network (each block can either be "used" — contribute $f_i(x)$ — or "skipped" via the identity path). This reframes a ResNet as effectively an **ensemble of many different-depth sub-networks** sharing weights.

**Empirical support for this view (the plots on the slide):**
- **Deleting individual layers** causes only a gradual, smooth degradation in error (not catastrophic failure) — consistent with "ensemble" behavior, since other paths can still carry useful signal.
- **Path length distribution** is concentrated around a particular length (not all paths are equally likely; most effective paths are of moderate length).
- **Gradient magnitude decreases sharply with path length** — meaning **longer paths contribute disproportionately less to gradient signal** during training, supporting the idea that the *effective* depth of the network (in terms of what actually gets trained well) is **shorter than the network's nominal depth** — most of the useful learning signal flows through comparatively short paths, with the rest behaving like a (weakly-trained) ensemble contribution.

This is a great "why does ResNet generalize/train so well" theoretical talking point for an exam.

### 10.10 ResNet v2 tweaks ("Bag of Tricks" paper, Slide 43)

Three small but meaningful engineering refinements:

- **ResNet-B**: in the original bottleneck-block downsampling path, the 1×1 stride-2 conv at the *start* of the block **skips 3 out of every 4 input pixels** (since stride-2 on a 1×1 kernel just subsamples, ignoring the other 3 nearby pixels entirely — wasteful!). Fix: move the stride-2 operation into the **3×3 conv** instead (which, having a real spatial receptive field, can actually "see" all the input pixels even while subsampling), so no information is silently discarded.
- **ResNet-C**: replace the single big **7×7 stride-2** stem conv with **three stacked 3×3 convs** (first one stride 2) — directly the VGG-style "decompose a big kernel into smaller stacked ones" trick, applied to the stem.
- **ResNet-D**: the 1×1-stride-2 conv used on the **skip-connection** path (to match dimensions between stages) has the *same* "ignores ¾ of input" problem as ResNet-B. Fix: insert a **2×2 stride-2 average pool** *before* the 1×1 conv on the skip path, so all four pixels in each 2×2 block get averaged together before the channel-projection, instead of silently dropping 3 of them.

**Common thread across all three fixes**: avoid using a strided 1×1 conv (or strided 7×7-without-care) in a way that silently discards spatial information — always make sure pooling/striding genuinely aggregates information from all relevant input pixels rather than just sampling one and ignoring the rest.

### 10.11 Common ResNet variants (Slides 44–45) — memorize this table

| Model | Block type | Blocks per stage | Approx params | Approx flops/img | Top-5 error |
|---|---|---|---|---|---|
| ResNet-18 | Basic (2×3×3) | 2,2,2,2 | ~22M (per slide: ~7.3 Gflops/img? — see below) | ~1.8 Gflops/img (slide says ~7.3 actually for 34 — let me restate per slide directly) | 7.46% |
| ResNet-34 | Basic (2×3×3) | 3,4,6,3 | ~25M | ~7.7 Gflops/img | 6.71% |
| ResNet-50 | Bottleneck (4× expansion) | 3,4,6,3 | ~44M | ~15.1 Gflops/img | 6.05% |
| ResNet-101 | Bottleneck | 3,4,23,3 | ~62M | ~23.4 Gflops/img | 5.71% |
| ResNet-152 | Bottleneck | 3,8,36,3 | (not separately listed on slide 45, but follows same bottleneck pattern with even more blocks) | — | — |

To read the slide exactly as given (matching params/flops/error to network sizes, top to bottom: ResNet-18 → 7.3Gflops/22M/7.46%; ResNet-34 → 7.7Gflops/25M/6.71%; ResNet-50 → 15.1Gflops/44M/6.05%; ResNet-101 → 23.4Gflops/62M/5.71%). Note **errors reported are on the validation set with 10-crop testing** — again the "augmentation caveat" from slide 4 applies.

**Key structural distinction (definitely testable):**
- **ResNet-18 / ResNet-34** use the **basic block** (two stacked 3×3 convs, no channel expansion).
- **ResNet-50 / ResNet-101 / ResNet-152** use the **bottleneck block** (1×1 reduce → 3×3 → 1×1 expand by 4×) — this is *why* their "channel" labels in the stage diagram look 4× bigger (256, 512, 1024, 2048) compared to ResNet-18/34's (64,128,256,512): the bottleneck's *expanded* output channel count is reported, but internally it's computed at 1/4 that width.

**Slide highlights ResNet-50 as the "good default choice"** — worth remembering as the practical recommendation given on the slide.

---

## 11. Transfer Learning (Slides 46–47)

### Core idea
Most practitioners never train these huge networks from scratch on a new task — instead they **reuse a network pretrained on a large dataset** (typically ImageNet-1k or ImageNet-21k) and adapt it to a smaller/new dataset. This works because learned visual features (edges → textures → parts → objects) tend to be broadly transferable across visual tasks.

### Two main strategies (Slide 46 diagram)
1. **Frozen feature extractor**: keep all pretrained CNN weights fixed (frozen), only train a *new* classifier head on top, using the frozen network purely as a feature extractor for the new dataset.
2. **Fine-tuning**: initialize the *whole* network (including the convolutional backbone) with pretrained weights, then continue training (updating) all or most of the weights on the new dataset.

### Practical fine-tuning recipe (Slide 47) — important practical exam content
1. **Start with a frozen feature extractor** first (train just the new head) — this gives a reasonable starting point and avoids destroying useful pretrained features early when the new head's weights are still random/noisy (large early gradients from a randomly-initialized head could otherwise back-propagate into and damage the pretrained backbone).
2. **Use a smaller learning rate** than what was used to originally train the architecture from scratch — pretrained weights are already in a good region of the loss landscape; large updates would move them too aggressively and destroy that.
3. **Progressive/differential learning rates**: use even smaller learning rates for earlier (more generic, lower-level) layers, and possibly **freeze the very lowest layers entirely** — the intuition being that early layers learn very generic features (edges, colors, simple textures) that transfer almost universally, while later layers learn more task/dataset-specific features that benefit more from adaptation.

---

## Quick self-test checklist (use this to study)

To make sure you're exam-ready, you should be able to, without looking anything up:

1. Derive the output-size formula and apply it to any conv/pool layer given $W_{in}, K, S, P$.
2. Compute #params, #activations, flops, and memory for any conv, pool, or FC layer from scratch.
3. Explain *why* activation memory needs ×2 (training-time gradient storage) and parameter memory needs ×3-4 (value + gradient + optimizer state), and why the *input* layer doesn't get the ×2.
4. Explain why FC layers dominate parameter count while conv layers dominate FLOPs — and connect this to why GoogLeNet (GAP) has so few parameters compared to AlexNet/VGG.
5. State the chronological lesson chain: AlexNet (big stem) → ZFNet (stem too aggressive, soften it) → VGG (uniform 3×3 stages, no stem) → GoogLeNet (multi-branch + 1×1 bottlenecks + gentle multi-layer stem + GAP) → ResNet (skip connections solve the *training*, not just capacity, problem of depth).
5b. Explain the "two 3×3 = one 5×5 receptive field, fewer params/flops, more memory" trade-off and why it generalizes (it's the same logic behind Inception v3's factorizations and ResNet-C's stem redesign).
6. Explain 1×1 convolutions precisely: they act as a per-pixel linear layer across channels, changing depth without touching spatial size — and why this is the key tool for controlling Inception module cost.
7. Explain the residual block: what problem it solves (degradation with depth = an *optimization* problem, not just overfitting), how it's structured, why near-zero initialization helps it start near the identity function, and how dimension mismatches at stage transitions are handled (zero-pad+stride vs. 1×1 stride-2 conv).
8. Distinguish basic vs. bottleneck residual blocks, and which ResNet variants use which.
9. Describe the three "Bag of Tricks" ResNet-v2 fixes (B, C, D) and the unifying theme (don't silently discard spatial info under stride).
10. Explain transfer learning: frozen vs fine-tune, and the three-part practical recipe (freeze first → smaller LR → progressive LR/freezing by depth).

Would you like me to turn this into a structured study guide document (e.g. a Word doc or markdown) you can print, or generate practice exam questions (with worked solutions) based on these numerical formulas?I'll go through this lecture deck slide by slide, building up every concept from scratch with full intuition and the math behind it. This is a long, dense lecture — let's take it seriously and thoroughly.

# The Big Picture

This lecture traces the evolution of CNN architectures for image classification, from LeNet5 (1998) to ResNet (2015), using the ImageNet competition (ILSVRC) as the timeline. The narrative arc is important for the exam: **each architecture solves a specific problem with the previous one.** If you understand *why* each architecture was invented (not just *what* it looks like), you'll be able to answer any conceptual exam question.

Let me set up the visual roadmap first, then go layer-by-layer through the math, then architecture-by-architecture through the ideas.Now let me build the visual map of the whole lecture's progression, then walk through every section in depth.Now let's go through every concept in deep, exam-ready detail.

---

## 1. The generic CNN architecture (Slide 2)

A CNN classifier is built from **two functional blocks**:

1. **Feature extractor**: a stack of *N* repeated blocks, each block usually `Conv2D → (ReLU) → MaxPool`. Notice the slide's small parenthetical remark: *"with max-pool, ReLU can be the last operation in a block"* — meaning the order Conv→ReLU→Pool and Conv→Pool→ReLU are functionally similar in many implementations, but the convention shown is Conv→Pool→ReLU per the diagram ordering (2D Conv, Max-Pool, ReLU stacked).
2. **Classifier**: *M* fully connected (FC) layers at the end, after a **flatten** operation that turns the final 3D activation tensor into a 1D vector.

The notation used: $h_3 \to \phi(W_4 h_3 + b_4) \to h_4 \to W_5 h_4 + b_5 \to s$

- $h_i$ = activation (hidden state) after layer $i$
- $W_i, b_i$ = weight matrix and bias of layer $i$
- $\phi$ = nonlinearity (e.g. ReLU)
- $s$ = final score vector (logits) — notice **no nonlinearity** on the very last layer; it outputs raw scores, since softmax/loss is applied outside the network.

**Key exam point:** the last FC layer is called the **classifier** (produces class scores), while everything before flatten is the **feature extractor** (produces a vector representation, an "embedding," of the image).

---

## 2. LeNet5 (Slide 3) — the historical baseline

This is your reference point for "what didn't exist yet" in 1998:

- **Channels increase, spatial size decreases with depth** — this trend holds in *every* CNN you'll study. It's the fundamental geometric design of CNNs: trade spatial resolution for semantic channels.
- **Average pooling**, not max pooling (max pooling becomes standard later).
- **5×5 kernels, no padding** → this means every conv layer *shrinks* the spatial size (since there's no zero-padding to compensate).
- **Sigmoid/tanh nonlinearities** — pre-ReLU era. These saturate (gradients vanish at extremes), which is part of why training very deep nets with these was hard.
- **RBF (Radial Basis Function) classifier** at the very end instead of a plain softmax — an old-fashioned touch.
- **No residual connections, no (batch) normalization** — both didn't exist yet (BatchNorm: 2015, ResNet: 2015/2016).

This slide is essentially a checklist of "missing ingredients" that later architectures will each introduce one by one.

---

## 3. ILSVRC error evolution (Slide 4)

This chart is the **spine of the whole lecture**. ImageNet Top-5 error rate over years:

| Year | Model | Top-5 error |
|---|---|---|
| 2010 | — | 28.1% |
| 2011 | — | 25.8% |
| 2012 | AlexNet | 16.4% |
| 2013 | ZFNet | 11.7% |
| 2014 | VGG | 7.4% |
| 2014 | Inception-v1 | 6.7% |
| 2015 | ResNet | 3.6% |
| 2016 | ResNeXt | 3.03% |
| 2017 | SENet | 2.3% |

**Important caveat the slide makes**: these numbers are *"based on ensembles and, sometimes, heavy test-time augmentation"* — meaning the headline numbers you see in papers are usually **not** a single model's single-pass error. They often combine multiple trained models (ensembling) and multiple crops/transformations of the test image averaged together. If an exam question asks "is AlexNet's reported error the error of one single network on one image crop," the answer is generally **no** — be ready to mention this caveat.

**Top-5 error**, by the way, means: the true label is *not* among the model's top 5 predicted classes. It's a more forgiving metric than top-1 error, often used because ImageNet has many semantically similar/overlapping classes.

---

## 4. AlexNet (Slides 5–6) — the architecture that started it all

### Structure
- **5 convolutional layers** (conv + ReLU), some optionally followed by max-pooling.
- **3 FC layers** at the end.
- **Group convolutions**: AlexNet was trained on **two GTX580 GPUs**, and to split the computational load, certain conv layers were split into two parallel groups of half the channels each, computed on separate GPUs, that only periodically communicate. This is a *practical engineering hack*, not a fundamental architectural principle — but it's the origin of "grouped convolutions" later reused in other architectures (e.g., ResNeXt).

### Key historical/practical facts (exam-likely trivia)
- Won **ILSVRC 2012**.
- Trained on two GTX580 GPUs, took **5–6 days**.
- Used **Local Response Normalization (LRN)** — a now-abandoned normalization scheme (predates BatchNorm), used in some layers; **not used in later architectures**.
- Famous quote: results would improve simply with faster GPUs/bigger datasets — foreshadows the entire decade of scaling.
- ReLU was a major contributor to its success (faster training than sigmoid/tanh, mitigates vanishing gradients in the *positive* regime).

---

## 5. The Architecture Breakdown Table — THE most important methodological section

This is the part of the lecture an exam will almost certainly test numerically. You need to be able to **compute, from scratch, for any conv/pool/FC layer**: output spatial size, number of activations, number of parameters, FLOPs, and memory. Let's build every formula with full derivation and worked example, exactly as the slides do, but explained more carefully.

### 5.1 Setup notation
- $W_{in}, H_{in}$: input width/height (spatial size)
- $C_{in}$: input channels
- $W_K, H_K$: kernel width/height
- $S$: stride
- $P$: padding (per side)
- $C_{out}$: number of output channels = number of kernels (filters)

### 5.2 Output spatial size formula

$$\text{Activation H/W} = \left\lfloor \frac{W_{in} - W_K + 2P}{S} \right\rfloor + 1$$

This is the **single most important formula in CNN architecture math**. Memorize it cold. Intuition: you slide a $W_K \times W_K$ window across the (padded) input of size $W_{in} + 2P$, moving $S$ pixels at a time; the "+1" accounts for the starting position.

**Worked example (AlexNet conv1):** input 227×227, kernel 11×11, stride 4, padding 0 (note: the original paper says 224 but the standard breakdown actually uses 227 to make the math come out as an integer — this is a well-known subtlety/quirk of AlexNet you might get asked about):

$$\frac{227 - 11 + 0}{4} + 1 = \frac{216}{4} + 1 = 54 + 1 = 55$$

✓ matches the table (55×55).

**Worked example (pool1):** input 55, kernel 3, stride 2, padding 0:
$$\frac{55-3+0}{2}+1 = \frac{52}{2}+1 = 26+1=27$$ ✓

### 5.3 Number of activations
$$\#\text{Activations} = H_{out} \times W_{out} \times C_{out}$$
(per single image; the table multiplies by mini-batch size later when computing memory)

For input layer: $227 \times 227 \times 3 = 154{,}587$.
For conv1: $55 \times 55 \times 96 = 290{,}400$ ✓.

### 5.4 Number of parameters (conv layer)

$$\#\text{params} = (W_K \times H_K \times C_{in} + 1) \times C_{out}$$

Intuition: each output channel/filter has its own set of weights connecting to **all** input channels over the $W_K \times H_K$ spatial window, **plus one bias** per output channel. You multiply by $C_{out}$ because there are that many independent filters.

**Worked example (conv1):** $(11 \times 11 \times 3 + 1) \times 96 = (363+1) \times 96 = 364 \times 96 = 34{,}944 \approx 35K$ ✓ (table shows 35, in thousands).

This is exactly why **pooling layers have zero parameters** — they don't have learnable weights, just a fixed operation (max or average).

### 5.5 FLOPs (floating point operations) for a conv layer

$$\text{flops} = \text{minibatch-size} \times \#\text{activations} \times (W_K \times H_K \times C_{in}) \times 2$$

Intuition breakdown:
- For **each output activation** (each spatial position × each output channel), you compute a dot product over $W_K \times H_K \times C_{in}$ input values with the corresponding weights.
- A dot product of length $n$ takes $n$ multiplications + $n$ additions = $2n$ FLOPs (this is the standard convention: 1 MAC = 2 FLOPs).
- Multiply by the number of output activations (since you do this dot product once per output element) and by mini-batch size (you do this for every image in the batch).

**Worked example (conv1):** $290{,}400 \times (11 \times 11 \times 3) \times 2 = 290{,}400 \times 363 \times 2 \approx 211$ million flops per image... but the table reports **per mini-batch** of 128: $290{,}400 \times 363 \times 2 = 210{,}710{,}400$ — wait, let's check against the slide's own number: the slide says $= 290{,}400 \times (11 \times 11 \times 3) \times 2 = 27$ Gflops. That 290,400 already represents the *per-image* activation count, so:

$$\text{flops (per image)} = 290{,}400 \times 363 \times 2 = 210.9M$$

Then for the full mini-batch of 128: $210.9M \times 128 \approx 27{,}000M = 27$ Gflops ✓. **So the formula already bakes in mini-batch size as a multiplier on top of the per-image activation count** — the slide's flops column reports the **mini-batch total**, not per-image.

### 5.6 FLOPs for pooling layers

$$\text{flops} = \#\text{activations} \times W_K \times H_K$$

No factor of 2 here (no multiply-accumulate, just comparisons for max-pool, or sums for avg-pool — and notably this formula as written doesn't even multiply by mini-batch size in the slide's pool1 example, since pooling is so cheap it's often treated as negligible/just illustrating the per-image base count before scaling).

**Worked example (pool1):** $\#\text{activations}=69{,}984$ (this is per-image: $27\times27\times96$), $W_K \times H_K = 3\times 3=9$:
$$69{,}984 \times 9 = 629{,}856 \approx 0.63M\text{ flops (per image)}$$
Scaled by mini-batch 128: $\approx 80.6M$ ✓ matches table.

### 5.7 Memory for activations

$$\text{Activation memory (MB)} = 2 \times \text{minibatch-size} \times \#\text{activations(per image)} \times \frac{4\text{ bytes}}{1024^2}$$

Two key facts buried here:
- **Factor of 4 bytes**: activations are stored as 32-bit floats.
- **Factor of 2**: at **training time** you must store both the activation **and** its gradient (same-sized tensor) for backprop. This is explicitly explained on slide 10: *"We need to store all intermediate activations to compute the gradient... another tensor of the same size."*

**Worked example (conv1):** $2 \times 128 \times 290{,}400 \times 4 / 1024^2 = 283.6$ MB ✓.

**Worked example (input):** Note the input layer does *not* get the factor of 2 — the slide computes it as $128 \times 154{,}587 \times 4/1024^2 = 75.5$ MB. Why no ×2? Because **you don't backpropagate a gradient with respect to the input image itself** in standard classification training (the input has no learnable parameters before it, so there's nothing upstream to update) — so only one copy of input activations needs to be stored, not an activation+gradient pair. This is a subtle but testable distinction.

### 5.8 Memory for parameters

$$\text{Params memory (MB)} = 3 \times \#\text{params} \times \frac{4\text{ bytes}}{1024^2}$$

Why **×3** and not ×2 like activations? Per slide 10's explanation: for every parameter you need:
1. Its value
2. Its gradient
3. **An optimizer state term** (e.g. momentum velocity, or for Adam, first/second moments — which would actually need ×4, but the slide uses ×3 as the simplified standard estimate, e.g., covering value + gradient + one momentum term)

**Worked example (conv1):** $3 \times 34{,}944 \times 4 / 1024^2 \approx 0.4$ MB ✓.

The slide is explicit that **this is a lower bound**, an approximation: *"Hard to have a precise estimate... we can get approximate values by considering twice the activation size and 3-4 times the #params."*

### 5.9 The flatten layer — special case

Flatten has:
- **0 parameters** (no learnable weights)
- **0 additional memory** — it's literally a *view* / reinterpretation of the same memory buffer, reshaping a $C \times H \times W$ tensor into a $(C \times H \times W) \times 1$ vector, **no copy needed**.
- This is conceptually important: flatten doesn't transform data, it just **reinterprets the indexing**.

### 5.10 FC layers — formulas

**Parameters:**
$$\#\text{params} = C_{out} \times C_{in} + C_{out}$$
(weight matrix $C_{out} \times C_{in}$, plus one bias per output unit). Note: this is the **same formula as a conv layer with $W_K = H_K = 1$** — and that's exactly the conceptual link the lecture is building toward (an FC layer = special case of 1×1 conv with no spatial extent).

**Worked example (fc6):** input is the flattened $9216$-d vector, output 4096:
$$4096 \times 9216 + 4096 = 37{,}752{,}832 + ... $$
wait let's recompute precisely: $4096 \times 9216 = 37{,}748{,}736$, plus $4096$ bias terms $= 37{,}752{,}832 \approx 37{,}758K$ (table rounds slightly, but matches ✓).

**FLOPs:**
$$\text{flops} = \#\text{minibatch} \times 2 \times C_{in} \times \#\text{activations(out, per image)}$$

**Worked example (fc6):** $128 \times 2 \times 9216 \times 4096 \approx 9.66$ Gflops ✓ matches table.

### 5.11 The grand totals and the trends (Slide 19–20) — **memorize these conclusions**

For AlexNet (mini-batch 128):
- **62.4 million parameters**
- **~290 Gflops** total for the mini-batch → **2.2 Gflops/image**
- **1.4 GB** activation memory, **714 MB** parameter memory

**The five "trends to note" — these are exam gold, likely to be asked verbatim:**

1. **Stem layer** at the beginning of the network — a layer that aggressively reduces spatial size early (large kernel/stride) to control cost and grow receptive field fast.
2. **Nearly all parameters live in the FC layers** (37.7M + 16.8M + 4.1M ≈ 58.6M out of 62.4M total — i.e. ~94%!). Convolutions are comparatively parameter-light per layer, since weights are *shared* across spatial positions, while FC layers have one full weight per (input,output) pair with no sharing.
3. **Activation memory is dominated by the first conv layers** — because spatial resolution is still large there (55×55, 27×27), even though channel count is modest.
4. **FLOPs are dominated by conv layers** — because FLOPs scale with $H \times W \times C_{in} \times C_{out} \times K^2$, and even though conv layers have fewer parameters, they reuse those parameters at every spatial location, multiplying the compute enormously.
5. **Activations and parameters have similar memory footprint at training time** in AlexNet specifically (~1.4GB vs ~0.7GB — same order of magnitude, not negligible relative to each other).

This parameters-vs-flops dichotomy (**FC layers: many params, few flops; conv layers: few params, many flops**) is one of the most important conceptual takeaways of the entire lecture, and a classic exam question.

---

## 6. ZFNet / Clarifai (Slide 21)

- Same overall AlexNet-like structure, but its main *contribution* is methodological, not just architectural: they built **visualization tools (Deconvnets)** to actually look at what each layer's filters/activations represent — moving network design away from pure trial-and-error.
- Their key empirical finding via these visualizations + ablations: **AlexNet's first layer (11×11, stride 4) is too aggressive** → causes "dead filters" (filters that never activate meaningfully), missing frequency information, and **aliasing artifacts** in the second layer.
- **Fix**: smaller, gentler stem — use **7×7 conv with stride 2** in layer 1 (instead of 11×11 stride 4), and also use **stride 2** in the second 5×5 conv layer (spreading the spatial downsampling more gradually instead of doing it all at once in layer 1).
- This is the conceptual seed of the **"stem layer" design lesson**, later explicitly reused and refined by GoogLeNet and ResNet: *don't crush spatial resolution too violently in one shot — downsample gradually with more, smaller-stride layers.*

---

## 7. VGG (Slides 22–24)

### Philosophy
VGG's whole point is an **ablation/regularity argument**: instead of hand-designing different kernel sizes per layer (like AlexNet/ZFNet), restrict the entire network to only two primitive choices:
- **3×3 convolutions**, stride 1, padding 1 (preserves spatial size)
- **2×2 max-pooling**, stride 2, padding 0 (exactly halves spatial size)
- **Double the number of channels after every pooling step**

This simplicity makes the architecture "regular" and easy to reason about, and it was a deliberate experiment to show that **depth + simple uniform components** can outperform hand-crafted heterogeneous kernels.

### Other facts
- Got **2nd place** in ILSVRC 2014 (Inception v1 got 1st), 7.5% top-5 error.
- **Dropped LRN**.
- **No batch norm yet** (BN wasn't invented until 2015) — so VGG had a serious training problem: very deep configs (16, 19 layers) couldn't be trained from random initialization directly. Solution at the time: **pre-train a shallower network first, then initialize the deeper network's early layers with those weights** ("layer-wise" warm starting) — this trick became unnecessary once smart initialization schemes (e.g. Xavier/He init) and later BatchNorm arrived.
- VGG-16 and VGG-19 differ in the number of conv layers per stage (the **D** and **E** columns in the table on slide 22) — VGG-19 has more 3×3 convs added to certain stages compared to VGG-16.

### The concept of "Stages" (Slide 23) — important abstraction

A **stage** = a group of layers operating at the **same spatial resolution**, ending in a pooling layer that halves resolution. VGG stages are one of: conv-conv-pool, conv-conv-conv-pool, or conv-conv-conv-conv-pool.

**Why stack multiple small convs instead of one big one?** Slide 23's table compares:

| Option | Params | Flops | #ReLUs | #Activations stored |
|---|---|---|---|---|
| One $C\times C \times 5\times5$ conv | $25C^2+C$ | $50C^2 W H$ | 1 | $C \times W \times H$ |
| Two stacked $C\times C\times3\times3$ convs | $18C^2+2C$ | $36C^2WH$ | 2 | $2 \times C\times W\times H$ |

**Key insight (very testable):** two stacked 3×3 convs have the **same receptive field** as one 5×5 conv (because a 3×3 conv followed by another 3×3 conv "sees" a 5×5 region of the original input — receptive fields compose additively: $RF = k_1 + k_2 - 1 = 3+3-1=5$). But the two-3×3 version:
- Uses **fewer parameters**: $18C^2$ vs $25C^2$ (for large $C$).
- Uses **fewer flops**: $36C^2WH$ vs $50C^2WH$.
- Has **more nonlinearities** (2 ReLUs instead of 1) → more expressive power, since you interleave nonlinear transformations rather than doing one big linear-ish operation.
- **"No free lunch"**: it **doubles the activation memory** you need to store at training time (you have an extra intermediate tensor of full size $C\times W\times H$ to keep for backprop) — this is the cost of the efficiency gain. This trade-off (fewer params/flops, but more memory) is a recurring theme and definitely worth remembering as a general principle: **decomposing one large operation into several smaller ones often saves params/flops at the cost of extra memory and more sequential computation.**

### VGG-16 summary numbers (Slide 24)
- **138M params** (≈2.3× AlexNet), again **mostly in FC layers**.
- **~4 Tflops** (~14× AlexNet), **31 Gflops/image**, dominated by convolutions.
- **~16.5 GB memory** (~12× AlexNet) — dominated by activations, specifically because of the **early conv layers without a stem layer** — VGG keeps full 224×224, then 224×224 again before the first pool, so those first activations are huge (3136 MB each for conv1/conv2!) compared to AlexNet's stem-shrunk first layer.
- Trained on **4 GPUs, data parallelism, 2–3 weeks**.

---

## 8. Inception v1 / GoogLeNet (Slides 25–32)

### The big idea
Quote from the paper, worth memorizing: *"The main hallmark of this architecture is the improved utilization of the computing resources inside the network... allows for increasing the depth and width of the network while keeping the computational budget constant."*

Architecture = **Stem layers** (similar idea to ZFNet's gentle downsampling) → **stack of Inception modules** → **Global Average Pool + classifier**.

- 22 "trainable layers" counted along the main path, but **~100 layers overall** if you count every branch inside every Inception module separately.

### Stem layers (Slide 26)
- Downsamples aggressively but **gently and gradually**: 224 → 28 in only 5 layers, using **only stride-2 operations** and a **largest kernel of 7×7** (learning directly from the ZFNet lesson — no giant 11×11 stride-4 jump).
- Cost: ~130 Gflops, 124K params, ~2GB memory for the *whole stem*.
- Comparison: VGG needs **10 layers** to reach the same 28×28 resolution, and that costs **2.4 Tflops, 1.7M params, 13GB memory** — i.e., the stem-based gradual downsampling is **dramatically cheaper** than VGG's uniform full-resolution stacking. This comparison is a strong illustration of *why stems matter*.

### Naïve Inception module (Slide 27) — the problem

The core idea of "Inception" is: instead of choosing one kernel size per layer (3×3 *or* 5×5 *or* 1×1), run **several different operations in parallel on the same input** and **concatenate** their outputs along the channel dimension. This lets the network learn which receptive field sizes matter at each stage, instead of the architect guessing.

Naïve module branches (all applied to the same $28\times28\times192$ input):
- 1×1 conv → 64 channels
- 3×3 conv (pad 1) → 128 channels
- 5×5 conv (pad 2) → 32 channels
- 3×3 max-pool (pad 1, stride 1) → preserves 192 channels (pooling doesn't change channel count!)

Concatenated output: $64+128+32+192 = 416$ channels.

**Two problems identified:**
1. **Channel explosion**: because the max-pool branch passes through the *full* 192 input channels untouched, every time you stack inception modules, channel count snowballs upward very fast (since concatenation only adds channels, never reduces them via the pooling branch).
2. **Computational cost**: large convolutions (3×3, 5×5) applied directly on a high channel-count input (192) are expensive: the slide computes $5\times5$ conv cost $\approx 240$ Mflops and $3\times3$ conv cost $\approx 350$ Mflops for *just one module* — and this compounds catastrophically if you stack many such modules.

### The fix: 1×1 convolutions (Slide 28) — bottleneck trick

**What is a 1×1 convolution, conceptually?** It has *no spatial extent at all* — its kernel only looks at a single pixel location, but across *all* input channels. So at each spatial location, it's literally just **a linear (fully-connected) transformation applied independently to the channel vector at that pixel**: take the $C_{in}$-length vector at one pixel, multiply by a $C_{out}\times C_{in}$ weight matrix + bias, get a $C_{out}$-length vector. If you stack several 1×1 convs (with nonlinearities between), you're literally running an **MLP applied identically at every spatial location** (this is the "Network in Network" idea, cited as Lin et al. ICLR 2014).

**Why it's useful here:** a 1×1 conv lets you **cheaply change channel depth** (compress or expand $C$) **without touching spatial size**. This gives architects a "dial" to control computational cost independent of spatial resolution.

### Inception module with dimension reduction (Slide 29)

Now each expensive branch gets a 1×1 conv **bottleneck** first, to *shrink* the channel count before the expensive spatial conv:
- 1×1 conv → 64 (this branch, by itself, *is* one of the parallel outputs)
- 1×1 (→96) then 3×3 conv → 128
- 1×1 (→16) then 5×5 conv → 32
- 3×3 max-pool, then 1×1 conv (→32) to *control* the pooling branch's channel count too (this also fixes problem #1 — channel explosion — since now even the pooling path is compressed)

Result: output is $64+128+32+32=256$ channels — much more controlled.

**Recomputed cost with bottleneck**, exactly as the slide shows:
- 5×5 branch: $28\times28\times16\times192\times2$ (the 1×1 reduction) $+ 28\times28\times32\times16\times5\times5\times2$ (the 5×5 conv on the *reduced* 16 channels) $\approx 5M + 10M = 15M$ flops — vs. **240M** before. That's a **~16× reduction**.
- 3×3 branch: similarly drops from 350M to ~202M flops.

This is the central lesson of Inception modules: **use 1×1 convs as cheap "bottlenecks" to control channel dimensionality before expensive operations** — a pattern reused everywhere afterward (including ResNet's bottleneck block, covered later).

### Global Average Pooling vs FC classifier (Slides 30–31)

This addresses the "nearly all parameters are in the FC layers" problem we saw in AlexNet/VGG.

**Idea (from Network-in-Network):** instead of flattening the final feature map and feeding it to a big FC layer (which needs $C\times H\times W \times \text{num\_classes}$ parameters), just **average each channel's spatial map down to a single number** — Global Average Pooling (GAP) — producing a $C$-length vector, then apply **one small FC layer** ($C \times \text{num\_classes}$ params) directly on that.

**Quantitative comparison (Slide 31):**
- GoogLeNet's GAP + 1 FC layer: **~1 million parameters total**, negligible flops.
- VGG's three FC layers: **124 million parameters**, requiring **31 Gflops**.

This single change explains why GoogLeNet, despite being "deeper," ends up with **far fewer total parameters** than VGG (7M vs 138M) — confirming the lecture's broader point that **FC layers, not depth, are usually where parameter count balloons.**

**Practical PyTorch note** the slide makes: using `AdaptiveAvgPool2d` (which computes the pooling kernel size automatically based on input size) instead of a fixed-size `AvgPool2d` makes the network **size-agnostic** — it can process input images of *any* spatial resolution, not just the one used at training time. This is a genuinely useful practical fact for an exam.

### GoogLeNet summary (Slide 32)
- **~7 million parameters**, **390 Gflops** (3 Gflops/image), **~3.3 GB** memory.
- **10.07% top-5 error** with a single model + single crop; **7.89%** with one model + aggressive multi-crop test-time augmentation (144 crops) — this nicely illustrates the "ensembles/augmentation" caveat from slide 4: test-time tricks meaningfully move the needle.

Comparing all three so far is a great mental table for the exam:

| Model | Params | Flops/img | Memory | Where most params live |
|---|---|---|---|---|
| AlexNet | 62M | 2.2 Gflops | 1.4GB act + 0.7GB params | FC layers (~94%) |
| VGG-16 | 138M | 31 Gflops | ~16.5GB | FC layers |
| GoogLeNet | 7M | 3 Gflops | ~3.3GB | Spread across conv/inception (GAP kills FC cost) |

---

## 9. Inception v3 (Slide 33) — brief mention

Key idea: **factorize convolutions** further to reduce params/flops while keeping the same receptive field, similar in spirit to the VGG "stages" 3×3-stacking trick but pushed further:
- **Factorization A** (used at fine spatial scale, 35×35): splits a larger conv into parallel smaller-kernel branches.
- **Factorization B** (mid-scale, 17×17): uses **asymmetric** convolutions — $n\times1$ followed by $1\times n$ — to factorize a $n\times n$ conv into two cheaper 1D convolutions (this is the same logic as the 5×5 → two 3×3 trick, generalized: an $n\times n$ conv can be replaced by a $1\times n$ conv followed by an $n\times 1$ conv, drastically reducing params from $O(n^2)$ to $O(n)$, per channel).
- **Factorization C** (coarse scale, 8×8): even more aggressive parallel asymmetric splitting.

Result: **4.48% top-5 error** with 12-crop testing. The slide's overarching message: **smaller/fewer parameters → easier optimization ("more disentangled," easier to train) and better efficiency**, not just a side effect.

---

## 10. Residual Networks / ResNet (Slides 34–47) — the deepest conceptual section

### 10.1 The problem ResNet solves (Slide 34)

**Empirical observation from VGG:** depth helps... up to a point. But naively stacking more layers **does not monotonically improve performance** — and crucially, **training error also increases** with depth (not just test/validation error). This rules out "overfitting" as the sole explanation, since overfitting would show *low* training error but *high* test error — here **both go up**. So there's a genuine **optimization problem**: SGD struggles to train very deep "plain" networks well, even with Batch Norm already in place.

**The constructive existence proof:** if a 20-layer network achieves performance $X$, you can in principle build a 56-layer network that's *at least as good*, simply by setting the extra 36 layers to compute the **identity function** (pass input through unchanged). So a deep network should never be worse, in principle. But **SGD fails to find this trivial identity solution** using the standard parameterization of layers (a plain stack of weight layers learning $H(x)$ directly does not easily converge to $H(x) = x$).

### 10.2 The residual block solution (Slide 35)

**Fix: reparameterize what each block learns.** Instead of forcing a block to learn the *full* mapping $H(x)$, let it learn the **residual** (the difference): $F(x) = H(x) - x$, and explicitly **add back $x$** via a skip connection:

$$\text{output} = F(x) + x$$

Structure of one residual block: `Conv2D → BN → ReLU → Conv2D → BN`, then **add the original input $x$**, *then* apply the final ReLU.

**Why this fixes the optimization problem:**
- Weights are typically initialized near zero (biases exactly zero), so initially $F(x) \approx 0$, meaning the block starts out **already computing the identity function** $x \to x$ almost automatically — there's no longer a hard optimization problem of *discovering* identity from scratch; it's the network's *default starting point*.
- The network now just needs to learn a small **"perturbation"** on top of identity, which is generally an easier optimization target than learning the whole transformation from scratch.
- Heavy use of **batch normalization** throughout, which by 2015 had become standard.

### 10.3 Overall ResNet design (Slide 36)

Inspired by VGG's "stages" philosophy:
- Network = stack of **stages**, each stage = stack of residual blocks.
- Each residual block = two stacked 3×3 convs + BN (as above).
- **First block of each new stage**: halves spatial resolution (via stride-2 conv) **and** doubles channel count — exactly matching VGG's "channels double after each pool" rule, but achieved through a stride-2 conv rather than a separate pooling layer.
- Uses a **stem layer** + **global average pooling** at the end, both borrowed directly from GoogLeNet.
- **Naming convention** (also borrowed from VGG): "ResNet-X" where X = number of layers with learnable weights (e.g. ResNet-18, ResNet-50).

### 10.4 Stem layer specifics (Slide 37)
- Just **one conv + one pool** layer (simpler than GoogLeNet's 5-layer stem), reducing only down to 56×56 (less aggressive than GoogLeNet's 28×28) — the slide's hypothesis: because **residual blocks themselves are lightweight** (compared to GoogLeNet's heavier multi-branch Inception modules), ResNet doesn't need as drastic an early reduction to keep total cost manageable.
- Ends with the same GAP + single linear-layer classifier pattern.

### 10.5 The dimension-matching problem (Slide 38) — important detail

The simple "add $x$ to $F(x)$" trick **only works when $x$ and $F(x)$ have the same shape**. But at the start of a new stage, the spatial size halves and channels double — so the skip connection's $x$ no longer matches the main branch's output shape. **Two solutions the authors tried:**

1. **Zero-padding + stride**: apply a stride-2 "identity-like" sampling to $x$ to match spatial size, and zero-pad the channel dimension to match the new (doubled) channel count. **No extra parameters.**
2. **1×1 conv with stride 2** and $2C$ output channels on the skip path — this *does* add a few parameters but lets the network *learn* the best projection rather than being forced into a fixed zero-padding scheme.

**Empirical finding: option 2 (learned projection) performs slightly better.** This is the "solid arrow" path in ResNet diagrams (versus a plain "dashed arrow" identity skip used within a stage where shapes already match).

### 10.6 Results (Slide 39)

- With residual connections, deeper networks (56-layer) now **outperform** shallower ones (20-layer) on both training and test error — confirming that residual blocks indeed solve the optimization issue, not just an overfitting issue.
- Won **all five main tracks** of the 2015 ILSVRC & COCO competitions by large margins (ImageNet classification with a 152-layer net described by Yann LeCun as *"ultra-deep"*; large improvements in detection/localization/segmentation too).
- Still **the standard baseline/backbone** referenced in this lecture as of writing (and broadly still true in practice as a default choice even today).

### 10.7 Bottleneck residual block (Slide 40) — efficiency variant

For *very* deep ResNets, the plain "two 3×3 convs" block becomes expensive at high channel counts. The **bottleneck block** structure:

`1×1 conv (C→C/4 reduction, i.e., here written as going from 4C down to C) → 3×3 conv (C→C) → 1×1 conv (C→4C expansion)`

Cost comparison (per the slide's formulas, in terms of base channel width $C$):
- **Basic block** (two 3×3 convs at width $C$): $36C^2HW$ flops, $18C^2$ params.
- **Bottleneck block** (1×1 reduce + 3×3 + 1×1 expand, where the "outer" width is $4C$): $34C^2HW$ flops, $17C^2$ params.

**Punchline: roughly the same total cost, but it lets you increase depth (more layers) without increasing the computational budget** — exactly the GoogLeNet philosophy of using 1×1 convs as a cheap dial to control cost while adding more representational depth. Bottleneck blocks are used in the *deeper* ResNet variants (ResNet-50/101/152).

### 10.8 Visualizing why residual learning helps (Slide 41)

A loss-landscape visualization (Li et al. 2018) shows: **without skip connections**, the loss surface of a 56-layer network is **jagged, chaotic, full of sharp local structure** — hard for gradient descent to navigate. **With skip connections**, the same network's loss surface is **smooth and convex-like** near the minimum — much easier for SGD to optimize. This is a nice intuitive/visual confirmation of "why" residual connections help beyond the identity-function argument.

### 10.9 ResNets as ensembles of shallow networks (Slide 42)

A follow-up theoretical analysis (Veit et al. 2016): if you "unravel" a residual network with $n$ blocks, you can view it as an implicit **sum over $2^n$ different possible paths** through the network (each block can either be "used" — contribute $f_i(x)$ — or "skipped" via the identity path). This reframes a ResNet as effectively an **ensemble of many different-depth sub-networks** sharing weights.

**Empirical support for this view (the plots on the slide):**
- **Deleting individual layers** causes only a gradual, smooth degradation in error (not catastrophic failure) — consistent with "ensemble" behavior, since other paths can still carry useful signal.
- **Path length distribution** is concentrated around a particular length (not all paths are equally likely; most effective paths are of moderate length).
- **Gradient magnitude decreases sharply with path length** — meaning **longer paths contribute disproportionately less to gradient signal** during training, supporting the idea that the *effective* depth of the network (in terms of what actually gets trained well) is **shorter than the network's nominal depth** — most of the useful learning signal flows through comparatively short paths, with the rest behaving like a (weakly-trained) ensemble contribution.

This is a great "why does ResNet generalize/train so well" theoretical talking point for an exam.

### 10.10 ResNet v2 tweaks ("Bag of Tricks" paper, Slide 43)

Three small but meaningful engineering refinements:

- **ResNet-B**: in the original bottleneck-block downsampling path, the 1×1 stride-2 conv at the *start* of the block **skips 3 out of every 4 input pixels** (since stride-2 on a 1×1 kernel just subsamples, ignoring the other 3 nearby pixels entirely — wasteful!). Fix: move the stride-2 operation into the **3×3 conv** instead (which, having a real spatial receptive field, can actually "see" all the input pixels even while subsampling), so no information is silently discarded.
- **ResNet-C**: replace the single big **7×7 stride-2** stem conv with **three stacked 3×3 convs** (first one stride 2) — directly the VGG-style "decompose a big kernel into smaller stacked ones" trick, applied to the stem.
- **ResNet-D**: the 1×1-stride-2 conv used on the **skip-connection** path (to match dimensions between stages) has the *same* "ignores ¾ of input" problem as ResNet-B. Fix: insert a **2×2 stride-2 average pool** *before* the 1×1 conv on the skip path, so all four pixels in each 2×2 block get averaged together before the channel-projection, instead of silently dropping 3 of them.

**Common thread across all three fixes**: avoid using a strided 1×1 conv (or strided 7×7-without-care) in a way that silently discards spatial information — always make sure pooling/striding genuinely aggregates information from all relevant input pixels rather than just sampling one and ignoring the rest.

### 10.11 Common ResNet variants (Slides 44–45) — memorize this table

| Model | Block type | Blocks per stage | Approx params | Approx flops/img | Top-5 error |
|---|---|---|---|---|---|
| ResNet-18 | Basic (2×3×3) | 2,2,2,2 | ~22M (per slide: ~7.3 Gflops/img? — see below) | ~1.8 Gflops/img (slide says ~7.3 actually for 34 — let me restate per slide directly) | 7.46% |
| ResNet-34 | Basic (2×3×3) | 3,4,6,3 | ~25M | ~7.7 Gflops/img | 6.71% |
| ResNet-50 | Bottleneck (4× expansion) | 3,4,6,3 | ~44M | ~15.1 Gflops/img | 6.05% |
| ResNet-101 | Bottleneck | 3,4,23,3 | ~62M | ~23.4 Gflops/img | 5.71% |
| ResNet-152 | Bottleneck | 3,8,36,3 | (not separately listed on slide 45, but follows same bottleneck pattern with even more blocks) | — | — |

To read the slide exactly as given (matching params/flops/error to network sizes, top to bottom: ResNet-18 → 7.3Gflops/22M/7.46%; ResNet-34 → 7.7Gflops/25M/6.71%; ResNet-50 → 15.1Gflops/44M/6.05%; ResNet-101 → 23.4Gflops/62M/5.71%). Note **errors reported are on the validation set with 10-crop testing** — again the "augmentation caveat" from slide 4 applies.

**Key structural distinction (definitely testable):**
- **ResNet-18 / ResNet-34** use the **basic block** (two stacked 3×3 convs, no channel expansion).
- **ResNet-50 / ResNet-101 / ResNet-152** use the **bottleneck block** (1×1 reduce → 3×3 → 1×1 expand by 4×) — this is *why* their "channel" labels in the stage diagram look 4× bigger (256, 512, 1024, 2048) compared to ResNet-18/34's (64,128,256,512): the bottleneck's *expanded* output channel count is reported, but internally it's computed at 1/4 that width.

**Slide highlights ResNet-50 as the "good default choice"** — worth remembering as the practical recommendation given on the slide.

---

## 11. Transfer Learning (Slides 46–47)

### Core idea
Most practitioners never train these huge networks from scratch on a new task — instead they **reuse a network pretrained on a large dataset** (typically ImageNet-1k or ImageNet-21k) and adapt it to a smaller/new dataset. This works because learned visual features (edges → textures → parts → objects) tend to be broadly transferable across visual tasks.

### Two main strategies (Slide 46 diagram)
1. **Frozen feature extractor**: keep all pretrained CNN weights fixed (frozen), only train a *new* classifier head on top, using the frozen network purely as a feature extractor for the new dataset.
2. **Fine-tuning**: initialize the *whole* network (including the convolutional backbone) with pretrained weights, then continue training (updating) all or most of the weights on the new dataset.

### Practical fine-tuning recipe (Slide 47) — important practical exam content
1. **Start with a frozen feature extractor** first (train just the new head) — this gives a reasonable starting point and avoids destroying useful pretrained features early when the new head's weights are still random/noisy (large early gradients from a randomly-initialized head could otherwise back-propagate into and damage the pretrained backbone).
2. **Use a smaller learning rate** than what was used to originally train the architecture from scratch — pretrained weights are already in a good region of the loss landscape; large updates would move them too aggressively and destroy that.
3. **Progressive/differential learning rates**: use even smaller learning rates for earlier (more generic, lower-level) layers, and possibly **freeze the very lowest layers entirely** — the intuition being that early layers learn very generic features (edges, colors, simple textures) that transfer almost universally, while later layers learn more task/dataset-specific features that benefit more from adaptation.

---

## Quick self-test checklist (use this to study)

To make sure you're exam-ready, you should be able to, without looking anything up:

1. Derive the output-size formula and apply it to any conv/pool layer given $W_{in}, K, S, P$.
2. Compute #params, #activations, flops, and memory for any conv, pool, or FC layer from scratch.
3. Explain *why* activation memory needs ×2 (training-time gradient storage) and parameter memory needs ×3-4 (value + gradient + optimizer state), and why the *input* layer doesn't get the ×2.
4. Explain why FC layers dominate parameter count while conv layers dominate FLOPs — and connect this to why GoogLeNet (GAP) has so few parameters compared to AlexNet/VGG.
5. State the chronological lesson chain: AlexNet (big stem) → ZFNet (stem too aggressive, soften it) → VGG (uniform 3×3 stages, no stem) → GoogLeNet (multi-branch + 1×1 bottlenecks + gentle multi-layer stem + GAP) → ResNet (skip connections solve the *training*, not just capacity, problem of depth).
5b. Explain the "two 3×3 = one 5×5 receptive field, fewer params/flops, more memory" trade-off and why it generalizes (it's the same logic behind Inception v3's factorizations and ResNet-C's stem redesign).
6. Explain 1×1 convolutions precisely: they act as a per-pixel linear layer across channels, changing depth without touching spatial size — and why this is the key tool for controlling Inception module cost.
7. Explain the residual block: what problem it solves (degradation with depth = an *optimization* problem, not just overfitting), how it's structured, why near-zero initialization helps it start near the identity function, and how dimension mismatches at stage transitions are handled (zero-pad+stride vs. 1×1 stride-2 conv).
8. Distinguish basic vs. bottleneck residual blocks, and which ResNet variants use which.
9. Describe the three "Bag of Tricks" ResNet-v2 fixes (B, C, D) and the unifying theme (don't silently discard spatial info under stride).
10. Explain transfer learning: frozen vs fine-tune, and the three-part practical recipe (freeze first → smaller LR → progressive LR/freezing by depth).

Would you like me to turn this into a structured study guide document (e.g. a Word doc or markdown) you can print, or generate practice exam questions (with worked solutions) based on these numerical formulas?
