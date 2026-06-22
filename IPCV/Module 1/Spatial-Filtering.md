

# The big picture of this lecture

This lecture answers one question across many angles: **how do you remove noise from an image without destroying real image content?** It builds up a family of filters in increasing sophistication: mean → Gaussian → median → bilateral → non-local means — each one fixing a specific weakness of the previous one. Let's trace that chain carefully, because that's exactly how exam questions on this material are structured.Now let's go through every section in full depth.

---

# Part 1 — What is noise, and why does averaging remove it? (Slides 4–7)

## The noise model

$$I_t(p) = \tilde I(p) + n_t(p), \qquad n_t(p) \sim N(0,\sigma) \text{ i.i.d.}$$

This is the foundational assumption of almost the entire lecture: a noisy observation $I_t(p)$ at pixel $p$ and time $t$ equals the **true, noiseless image value** $\tilde I(p)$ plus a **random noise term** $n_t(p)$ that is:
- **Zero-mean** ($N(0,\sigma)$ — centered at 0, so noise doesn't systematically push values up or down, only scatters them).
- **i.i.d.** (independent and identically distributed) — each pixel's noise draw is statistically independent of every other pixel's, and they all come from the same distribution.

## Denoising by averaging across time (Slide 5)

If you had $T$ repeated noisy captures of the *same static* scene (e.g. $T=100$ photos of a still subject), average them pixel-by-pixel:

$$O(p) = \frac{1}{T}\sum_{t=1}^{T} I_t(p) = \frac{1}{T}\sum_{t=1}^{T}\big(\tilde I(p)+n_t(p)\big) = \tilde I(p) + \frac{1}{T}\sum_{t=1}^{T}n_t(p) \approx \tilde I(p)$$

**Why this works, precisely**: the true signal $\tilde I(p)$ is identical across all $t$ (static scene), so it survives averaging unchanged. The noise terms, being zero-mean and independent, **partially cancel each other out** when averaged — by the law of large numbers, the average of $T$ i.i.d. zero-mean random variables shrinks toward zero as $T$ grows (specifically, the variance of the average shrinks as $\sigma^2/T$). **The mean image is far less noisy** because you've essentially divided the noise's standard deviation by $\sqrt T$, while leaving the true signal completely untouched.

## The problem: what if you only have ONE image? (Slides 6–7)

You don't have $T$ repeated captures — you have a single noisy photo. **The trick: trade the temporal average for a spatial average.** Instead of averaging the *same pixel* across *time*, average *nearby pixels* within the *same image*, assuming they likely share similar true underlying values (a reasonable assumption in smooth image regions).

**The key design question this immediately raises**: *how large should the neighborhood (support) $S$ be?* The slide states explicitly: **it's a trade-off** — bigger neighborhoods average over more noise samples (better denoising, lower residual noise), but also risk averaging together pixels whose *true* values are actually different (e.g. straddling an edge), which causes **blurring**. This single trade-off is the thread that the entire rest of the lecture pulls on.

## The spatial denoising filter formula (Slide 7)

$$O(p) = \frac{1}{|S|}\sum_{q\in S} I(q) = \frac{1}{|S|}\sum_{q\in S}\big(\tilde I(q)+n(q)\big) = \frac{1}{|S|}\sum_{q\in S}\tilde I(q) + \frac{1}{|S|}\sum_{q\in S}n(q) \approx \tilde I(q)$$

where $S$ is the **support** (the neighborhood of $p$ you average over), and $|S|$ is the number of pixels in it. This is algebraically the **exact same derivation** as the temporal-averaging case, just with the sum running over neighboring *pixels* instead of repeated *time samples* — same math, different averaging axis.

## Image filters, defined generally (Slide 7, bottom)

$$o(p) = f(S(p))$$

**Image filters** are operators that compute a pixel's new intensity based on the intensities of pixels in a **neighborhood (support)** of $p$. They serve many purposes (denoising, sharpening/edge enhancement, etc.), and **Linear and Translation-Equivariant (LTE) operators** form a particularly important sub-class. This is the bridge into the signal-processing formalism next.

---

# Part 2 — LTE operators and convolution (Slides 10–18)

## Defining the two properties precisely (Slides 10–11)

Given a 2D operator $T$: $o(x,y) = T\{i(x,y)\}$:

**Linearity:**
$$T\{\alpha i_1(x,y)+\beta i_2(x,y)\} = \alpha\,o_1(x,y)+\beta\,o_2(x,y), \quad \text{where } o_1=T\{i_1\},\ o_2=T\{i_2\}$$

The operator's response to a weighted sum of inputs equals the same weighted sum of the individual responses — **superposition holds**.

**Translation-equivariance:**
$$T\{i(x-x_0,y-y_0)\} = o(x-x_0,y-y_0)$$

Shifting the input by $(x_0,y_0)$ shifts the output by exactly the same amount — the operator behaves identically no matter *where* in the image it's applied.

## The fundamental theorem: LTE ⟺ convolution (Slide 11)

**If an operator is both linear and translation-equivariant, its output is *necessarily* given by convolving the input with the operator's impulse response** $h(x,y) = T\{\delta(x,y)\}$ (its response to a unit impulse, the Dirac delta):

$$o(x,y) = T\{i(x,y)\} = \int_{-\infty}^{\infty}\int_{-\infty}^{\infty} i(\alpha,\beta)\,h(x-\alpha,y-\beta)\,d\alpha\,d\beta$$

**Why this matters conceptually**: this is the theoretical justification for *why* convolution is the right mathematical tool for so much of classical image processing — it's not an arbitrary choice, it's the **unique consequence** of demanding the two natural properties (linearity + shift-equivariance) from your filter. Anything you'd want a "well-behaved, position-independent linear filter" to do is *automatically* a convolution, by this theorem.

## Graphical view (Slide 13) — what the two operations inside the integral mean

The formula contains exactly two geometric operations on $h$:
- **Reflection about the origin**: $h(x-\alpha,y-\beta)$, as a function of $(\alpha,\beta)$, is $h$ **flipped** (since the argument's sign on $\alpha,\beta$ is negative).
- **Translation**: the flipped $h$ is then **shifted** so its origin sits at $(x,y)$.

You multiply this flipped-and-shifted $h$ against $i$, and integrate (sum up the product) — that integral value becomes the single output pixel at $(x,y)$. Then you repeat for every $(x,y)$.

## Properties of convolution (Slide 14) — memorize all four

$$o(x,y) = i(x,y)*h(x,y)$$

1. **Associative**: $f*(g*h) = (f*g)*h$
2. **Commutative**: $f*g = g*f$
3. **Distributive over sum**: $f*(g+h) = f*g+f*h$
4. **Commutes with differentiation**: $(f*g)' = f'*g = f*g'$

(Property 4 is a genuinely useful practical fact, e.g. it's exactly why you can compute an image's derivative by convolving with a derivative-of-Gaussian kernel in one step, instead of first smoothing then separately differentiating.)

## Correlation (Slide 15) — same idea, no flip

$$i(x,y)\circ h(x,y) = \int_{-\infty}^{\infty}\int_{-\infty}^{\infty} i(\alpha,\beta)\,h(x+\alpha,y+\beta)\,d\alpha\,d\beta$$

Note the **sign**: $h(x+\alpha,y+\beta)$ — a **plus**, not a minus like in convolution. This is the formal definition behind the change-of-variables argument that follows. The slide also explicitly derives the order-reversed version, correlation of $h$ wrt $i$:

$$h(x,y)\circ i(x,y) = \int\int h(\alpha,\beta)\,i(x+\alpha,y+\beta)\,d\alpha\,d\beta$$

using the substitution $\xi = x+\alpha \Rightarrow \alpha=\xi-x$, $\eta=y+\beta\Rightarrow\beta=\eta-y$.

**Crucial, explicitly stated fact**: *unlike convolution, correlation is NOT commutative*: $i\circ h \neq h\circ i$ in general.

## Convolution vs correlation, fully reconciled (Slide 17) — the exact relationship to memorize

$$\text{Convolution is commutative:} \quad i*h = h*i$$
$$\text{Correlation is NOT commutative:} \quad i\circ h \neq h\circ i$$
$$\text{If } h \text{ is an even function } (h(x,y)=h(-x,-y)): \quad i*h = h*i = h\circ i$$

**Read this last line very carefully — it's the single most commonly mis-stated fact on exams.** When $h$ is **even** (symmetric about the origin), convolution and correlation *coincide* — but **only in this specific direction**: $i*h$ equals **$h\circ i$** (correlation of $h$ with respect to $i$), not $i\circ h$. And even in this special case, **correlation itself still never becomes commutative** — $i\circ h\neq h\circ i$ remains true regardless of whether $h$ is even. The evenness of $h$ only creates a bridge *between* convolution and one specific ordering of correlation; it does not make correlation symmetric in its own right.

This explains a fact you already learned in the previous lecture: most CNN kernels are *learned*, generic (non-even) functions, so cross-correlation and true convolution genuinely differ for them — but for classic **hand-designed symmetric kernels** (like a symmetric Gaussian or mean filter, which are even functions), the practical distinction disappears and the two operations give identical results.

---

# Part 3 — Discrete convolution and practical implementation (Slides 18–20)

## Discrete convolution formula (Slide 18)

$$O(i,j) = T\{I(i,j)\} = \sum_{m=-\infty}^{\infty}\sum_{n=-\infty}^{\infty} I(m,n)\,H(i-m,j-n)$$

where $H(i,j)=T\{\delta(i,j)\}$ is the **kernel** — the response to the **Kronecker delta** (the discrete analogue of the Dirac delta: 1 at the origin, 0 everywhere else). All four convolution properties from the continuous case carry over unchanged to the discrete case.

## The practical, finite-kernel version (Slides 19–20)

Since real kernels are finite (size $(2k+1)\times(2k+1)$, centered on the pixel), the infinite sum collapses to a finite one:

$$O(i,j) = \sum_{m=-k}^{k}\sum_{n=-k}^{k} K(m,n)\,I(i-m,j-n)$$

**Mechanically**: slide the kernel across every pixel position of the input image; at each position, compute the weighted sum of the corresponding $(2k+1)\times(2k+1)$ neighborhood, weighted by the (flipped, per true convolution) kernel values; write that single number into the **output** image at that position. **Critical practical warning explicitly stated**: *do not overwrite the input matrix while computing* — you need the original, unmodified input values for every subsequent kernel position, so the output must be written to a separate buffer.

## The border problem (Slide 20) — what happens at the edges

When the kernel is centered near the image boundary, part of its footprint falls **outside** the image — there's no data there. **Two main solution families:**

1. **CROP**: simply don't compute output values for border pixels where the kernel would extend past the edge — the output image ends up **smaller** than the input. Common in classical image processing.
2. **PAD**: artificially extend the input with extra border pixels before convolving, so the kernel always has valid data to read, and the output stays the **same size** as the input. **Preferred in CNNs** (this directly connects back to the "same" padding concept from the previous lecture).

**Padding strategies, all explicitly listed (memorize the names and exact behavior)**:
- **Zero-padding**: pad with constant value 0.
- **Replicate**: repeat the edge pixel value outward, e.g. `aaa|Iabcd|ddd` (the slide's shorthand `aaaIa....dIddd` means: the leftmost real pixel `a` gets copied leftward, the rightmost real pixel `d` gets copied rightward).
- **Reflect**: mirror the image content across the border without repeating the edge pixel itself, e.g. `cba|abcd...dfg|gfd`.
- **Reflect_101**: mirror across the border, but this time the edge pixel itself participates only once / pattern includes it differently, e.g. `dcb|abcd...efgh|gfe` (a slightly different mirroring convention than plain reflect — the "101" naming, from OpenCV's convention, indicates the boundary pixel is *not* duplicated, unlike plain `reflect`).

---

# Part 4 — Mean filter (Slide 21) — the simplest linear filter

The **mean filter** replaces each pixel with the **average intensity** over a chosen neighborhood. It's an LTE operator, so it's expressible as convolution, with kernel:

$$K_{3\times3} = \frac{1}{9}\begin{bmatrix}1&1&1\\1&1&1\\1&1&1\end{bmatrix} \qquad K_{5\times5}=\frac{1}{25}\begin{bmatrix}1&1&1&1&1\\1&1&1&1&1\\1&1&1&1&1\\1&1&1&1&1\\1&1&1&1&1\end{bmatrix}$$

**Key signal-processing classification**: the mean filter performs **low-pass filtering** — in image-processing language, this is called **smoothing**. Low frequencies (smooth, gradual intensity changes) pass through; high frequencies (sharp transitions — edges, fine texture) get attenuated. **Purpose**: usually denoising, though sometimes simply to suppress unwanted fine-scale detail that would interfere with a downstream analysis task.

**A nice practical/efficiency fact, explicitly stated**: mean filtering is **inherently fast because multiplications aren't needed** — since every kernel weight is the same constant ($1/9$ or $1/25$), you can simply **sum** the neighborhood and divide once at the end, rather than multiplying each pixel by its (identical) weight individually. (This is also exactly why the **separable, running-sum/box-filter implementation** — computing a row-sum first, then a column-sum — is so cheap; more on separability below.)

## Mean filter in action — and its fundamental weakness (Slides 24–25)

Given Gaussian noise ($\mu=0,\sigma=8$), comparing $3\times3$ vs $5\times5$ mean smoothing: **larger kernels denoise more strongly but blur more**, exactly the trade-off predicted in Part 1.

**The critical limitation, demonstrated by the slide's pointed question** ("the ideal noiseless value of these pixels is the same? What happens here?"): a uniform, *unweighted* average is blind to **where an edge sits** within the neighborhood. If the support straddles a real edge (low intensities on one side, high intensities on the other), the mean filter **mixes them together regardless**, producing an output value that doesn't correctly represent *either* side — this **blurs edges**, smearing sharp transitions into smooth ramps. **Linear filtering reduces noise, but always at the cost of blurring the image** — this is the single biggest weakness that every subsequent, more sophisticated filter in the lecture exists to fix.

---

# Part 5 — Gaussian filter (Slides 27–31)

## Definition (Slide 27)

The **Gaussian filter** is an LTE operator whose impulse response is a **2D Gaussian function** with zero mean and a constant, diagonal covariance matrix (i.e., circularly symmetric — equal spread in every direction, no correlation between $x$ and $y$). Why is this an improvement over the plain mean filter? Because instead of weighting **every** neighbor **equally**, it weights neighbors by **distance from the center**: nearby pixels get high weight, farther pixels get progressively lower weight, following the smooth bell-curve falloff of the Gaussian. This produces smoother, more natural-looking blur (less "blocky" than a flat box average) — but **note**: it still doesn't know anything about *intensity* differences, only spatial distance — so it **still blurs across edges**, just somewhat more gently than the mean filter (this is exactly why bilateral filtering, later, is needed).

## Choosing the kernel size given σ (Slide 28)

Since the true Gaussian has **infinite extent**, you must truncate it to a finite kernel. The trade-offs:
- **Larger size** → more accurate approximation of the true continuous Gaussian, but **higher computational cost**.
- **The Gaussian shrinks rapidly away from the origin** — so beyond a few standard deviations, contributions become negligible and can safely be dropped.

**Rule of thumb, exactly as given**: the interval $[-3\sigma,+3\sigma]$ captures **99% of the area (energy)** of the Gaussian, so a typical choice is a $(2k+1)\times(2k+1)$ kernel with $k=3\sigma$. (The slide gives the 1D values at $x=-3,-2,-1,0,1,2,3$ as $0.0044, 0.054, 0.242, 0.3989, 0.242, 0.054, 0.0044$ — note these visibly sum to nearly 1, and the tails at $\pm3$ are already tiny, confirming the rule of thumb numerically.)

## Separability — the major efficiency trick (Slide 30)

**Key mathematical fact**: a 2D Gaussian is the **product of two independent 1D Gaussians**:

$$G(x,y) = G(x)\cdot G(y)$$

This means the 2D convolution can be **factored into two sequential 1D convolutions** — convolve along $x$ first, then convolve the result along $y$ (or vice versa — order doesn't matter, by commutativity).

**Cost comparison, exactly as derived in the slide:**

$$\text{2D filter cost: } N_{op} = 2(2k+1)^2 \qquad \text{1D×2 filter cost: } N_{op} = 2\cdot2(2k+1)$$

(the factor "2" inside accounts for multiply+add per tap; applying it twice for the separable version accounts for doing it once per pass, along each of the two axes.)

**Speed-up factor:**

$$S = \frac{2(2k+1)^2}{2\cdot2(2k+1)} = \frac{2k+1}{2} = k+\frac{1}{2}$$

**The takeaway, stated very directly**: the bigger your kernel (larger $k$), the **bigger the speed-up** from exploiting separability — for large kernels, this isn't a minor optimization, it's the difference between $O(k^2)$ and $O(k)$ work per pixel, an asymptotic improvement, not just a constant-factor one.

## The role of σ as a "scale" parameter (Slide 31)

**Higher $\sigma$ → stronger smoothing.** Mechanistic reason given directly: as $\sigma$ increases, the Gaussian curve flattens out, so **the weight given to nearby points decreases while the weight given to farther points increases** — the filter effectively "reaches further" for its averaging, at the cost of local precision.

**Conceptual reframing, worth quoting exactly**: *"filtering with a chosen $\sigma$ can be thought of as setting the 'scale' of interest to analyze image content."* As $\sigma$ grows, **fine details vanish and only larger-scale structures remain visible** — this is the seed idea behind multi-scale image analysis (e.g. image pyramids, scale-space theory): $\sigma$ isn't just a "blur knob," it's a literal **dial selecting which spatial scale of structure you want to look at**.

---

# Part 6 — Impulse noise and the Median filter (Slides 32–34)

## The failure mode that motivates the median filter (Slide 32)

**Impulse noise** (aka **salt-and-pepper noise**) is fundamentally different from Gaussian noise: instead of every pixel getting a small random perturbation, a **small fraction of pixels get replaced entirely** by extreme values (very bright "salt" or very dark "pepper"), while the rest of the pixels remain completely clean.

**Why mean/Gaussian filtering fails here, explicitly stated**: *"Linear filtering is ineffective toward impulse noise (and blurs the image)."* The reasoning: a linear average is **extremely sensitive to outliers** — a single wildly-extreme corrupted pixel inside an averaging window **drags the entire average toward that extreme value**, contaminating the *whole* neighborhood's output, not just the corrupted pixel itself. Worse, you still get blurring on top of that, since it's still a linear blend.

## Median filter (Slide 33)

**Definition**: a **non-linear** filter — each pixel's intensity is replaced by the **median** value within its neighborhood (the value that falls exactly in the middle when all neighborhood intensities are sorted).

**Why this fixes impulse noise specifically, mechanistically**: outliers (corrupted pixels) tend to land at the **extreme top or bottom** of the sorted intensity list within a window — but the median, by definition, **ignores extreme values entirely** and only reports the middle-ranked value. So as long as corrupted pixels are a **minority** within the window, the median is computed entirely from the *clean* majority and is essentially unaffected by however extreme the corrupted minority's values are.

**Bonus property, explicitly stated**: median filtering tends to **preserve sharper edges** than linear filters like mean/Gaussian — because it picks an *actual observed value* from the neighborhood (rather than computing a blended average of dissimilar values across an edge), it doesn't create the smooth, blended "ramp" artifact that linear averaging introduces at edges.

## Practical demonstration and an important limitation (Slide 34)

Given impulse noise (+100 intensity offset, 5% of pixels randomly affected), a $3\times3$ median filter denoises effectively; applying it **twice** cleans up further.

**Crucial limitation, explicitly stated**: *"Gaussian-like noise, such as sensor noise, cannot be dealt with by the Median, as this would require computing new noiseless intensities."* The median can only ever **output a value that was already present** in the neighborhood — it never computes a genuinely new, blended value. This is perfect for impulse noise (where the *true* signal is unaffected at most pixels, you just need to reject the rare corrupted outlier) but **useless for Gaussian noise** (where *every* pixel's true value has been perturbed somewhat, so what you actually need is averaging/blending to estimate a new value that was never directly observed). **Suggested combination**: apply median first (to remove outliers), then follow with linear filtering (to denoise the remaining Gaussian-like component) — using each tool for the noise type it's actually suited to.

---

# Part 7 — Bilateral Filter (Slides 35–37) — finally, edge-aware denoising

## Motivation

We now have: mean/Gaussian filters denoise Gaussian noise well but blur edges; median filters preserve edges but only handle impulse noise. **The bilateral filter is designed to denoise Gaussian-like noise *without* blurring edges** — it's explicitly labeled **"edge preserving smoothing."**

## The formula, term by term (Slide 35)

$$O(p) = \sum_{q\in S} H(p,q)\cdot I_q$$

$$H(p,q) = \frac{1}{W(p)}\,G_{\sigma_d}\big(d_s(p,q)\big)\cdot G_{\sigma_r}\big(d_o(I_p,I_q)\big)$$

with:

- **Spatial distance**: $d_s(p,q) = \|p-q\| = \sqrt{(u_p-u_q)^2+(v_p-v_q)^2}$ — ordinary Euclidean distance between pixel *locations*.
- **Range (intensity) distance**: $d_o(I_p,I_q) = |I_p-I_q|$ — the difference between the two pixels' *intensity values*.
- **Normalization factor (unity gain)**: $W(p) = \sum_{q\in S} G_{\sigma_d}(d_s(p,q))\,G_{\sigma_r}(d_o(p,q))$ — ensures the weights $H(p,q)$ sum to 1 over the neighborhood, so the filter is a proper weighted average (preserves overall brightness, doesn't arbitrarily amplify or dim the image).

**The key structural idea**: the weight $H(p,q)$ is the **product of two separate Gaussian terms** — one based purely on *how far away* $q$ is spatially, the other based purely on *how different* $q$'s intensity is from $p$'s. **A neighbor only gets a high overall weight if it is BOTH close in space AND similar in intensity** — multiplying two Gaussians means either factor alone being small (far away, OR very different intensity) is enough to suppress the combined weight.

## Why this preserves edges (Slide 37)

*"Neighbouring pixels take a larger weight as they are both closer and more similar to the central pixel. At a pixel nearby an edge, the neighbours falling on the other side of the edge look quite different and thus cannot contribute significantly to the output value due to their weights being small."*

This is the entire mechanism in one sentence: at an edge, pixels on the **other side** have very different intensity from the center pixel $p$ — so even though they may be spatially close, the **range term** $G_{\sigma_r}(d_o)$ crushes their weight toward zero. The filter effectively **only averages within the same "side" of the edge**, never blending across it — hence "edge preserving."

The slide's worked example: a step-edge 100 gray-levels wide, with $\sigma_d=5,\sigma_r=50$, shows the weight map $H(p,q)$ at a pixel just across the edge in the brighter region — visually, you'd see weight concentrated almost entirely on the bright side, near-zero on the dark side, even though both sides are spatially close.

This is exactly the limitation/contrast the NLM exam answer we built earlier referenced: bilateral *is* a non-linear, edge-aware filter — but it's still fundamentally **local** (the support $S$ is a small neighborhood around $p$). **Non-local means is the next, final step**: take this exact idea — weight by similarity, not just distance — but stop restricting the search to a small local window, and instead compare entire **patches** (not single-pixel intensities) across the **whole image**.

---

# Part 8 — Non-Local Means (Slides 39–40)

This connects directly to what we covered in detail in your earlier exam answer, but now let's tie it precisely to *this* lecture's own notation and framing, since that's what your professor will expect verbatim.

## The key idea, exactly as stated

*"The key idea is that the similarity among patches spread over the image can be deployed to achieve denoising."* Just like the bilateral filter weighted by *intensity similarity*, NLM weights by similarity too — but the similarity is now measured **between entire local patches**, $N_p$ and $N_q$, not single pixel intensities, and $q$ is searched for across a **much larger region** $S$ (potentially the whole image), not just a small local neighborhood.

## Worked numerical example given directly in the slide (Slide 40)

- Noise level: Gaussian, $\sigma=20$.
- **Patch size** $N = 7\times7$.
- **Search window size** $S = 21\times21$.
- **Filtering parameter** $h = 10\cdot\sigma$.

This is a genuinely useful, concrete, memorizable example of realistic hyperparameter values — if your exam asks "give typical values for NLM's hyperparameters," these numbers (patch $7\times7$, search window $21\times21$, $h\approx10\sigma$) are a perfect, textbook-sourced answer.

The comparative result shown: against the same Gaussian-noise-corrupted image, a plain **Gaussian filter** denoises but blurs detail; **NLM** denoises while **preserving fine texture and detail far better**, precisely because it can borrow statistical strength from many genuinely-similar patches scattered across the whole image, rather than being limited to a small local Gaussian-weighted average.

---

## How this lecture connects to everything else you've already studied

This is genuinely the **foundation layer** beneath two things you've already worked through:
- It's the **direct prerequisite** to the NLM exam question from your second uploaded paper — now you have the full derivation chain: LTE theorem → convolution → mean filter → Gaussian filter → bilateral filter → NLM, where each step is explicitly motivated by a concrete failure of the one before.
- The **convolution formalism** here (continuous integral form, then discretized) is the signal-processing-theory version of the exact same convolution operation the architectures/representations lecture builds CNN layers from — same mathematical object, introduced first from classical image-processing motivations (denoising) here, then reused as a *learnable* feature extractor there.

## Quick self-test checklist for this lecture

1. Derive why averaging over time/space reduces noise without touching the true signal (the algebraic cancellation argument), and state the trade-off in choosing support size $|S|$.
2. State the two defining properties of LTE operators (linearity, translation-equivariance) and the theorem connecting them to convolution.
3. Write the convolution integral and identify the "reflect + translate" geometric interpretation of $h$.
4. State convolution's four properties (associative, commutative, distributive, commutes with differentiation).
5. Define correlation, and state precisely when/how it relates to convolution (only when $h$ is even, and only as $i*h=h*i=h\circ i$ — never $i\circ h=h\circ i$).
6. Write discrete convolution and explain the two border-handling strategies (crop vs pad) and the four padding types (zero, replicate, reflect, reflect_101).
7. Explain why the mean filter needs no multiplications, classify it as low-pass/smoothing, and explain precisely why uniform averaging blurs edges.
8. Derive the Gaussian filter's $3\sigma$ kernel-size rule, the separability speed-up factor $S=k+\tfrac12$, and explain σ as a "scale" parameter.
9. Explain why linear filters fail on impulse noise and why the median filter fixes it (and why median, in turn, fails on Gaussian noise).
10. Write out the bilateral filter formula term by term (spatial weight, range weight, normalizer) and explain exactly why multiplying the two Gaussians achieves edge preservation.
11. State NLM's key idea (patch similarity, global search) and recall the example hyperparameters (7×7 patch, 21×21 search window, h=10σ).

Want me to merge this with the NLM material from your earlier exam paper into one consolidated, non-redundant study document covering Prof. Lisanti's filtering side of the course end-to-end?
