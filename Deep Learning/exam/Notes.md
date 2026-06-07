Input: 9 patches of shape (28, 28, 3), scrambled in random order. Stored as tensor (9, 28, 28, 3) per sample.
Output: the original (96, 96, 3) image.
The patches were made by: taking a 96×96 image → splitting into 3×3 grid of 32×32 patches → center-cropping each to 28×28 (so 2px eroded from each side of every patch) → shuffling.
Two coupled subproblems hidden in this:

Permutation: figure out which patch goes where (9! possibilities).
Inpainting: fill in the 4-pixel-wide gaps between patches (the eroded borders).


Metric: MAE between predicted 96×96 image and ground truth.
Baseline to beat: 0.1826 (the "every pixel = mean of its source patch" trick).
Hard constraints: Keras, no pretrained, <6M params, single Colab notebook, weights downloadable via gdown.



Sure. These three questions matter because they determine how you should architect the model. Let me walk through each.

**Q1 — Why is the mean-patch baseline ~0.18 and not, say, 0.4?**

First understand what that baseline actually does. Look at the code: `tf.reduce_mean(patches, axis=1)` reduces over the *9 patches* dimension (not over pixels). So it computes the per-pixel average across the 9 patches, giving one "ghost" 28×28 image, then tiles it 9 times in a 3×3 grid and resizes to 96×96.

The reason MAE ≈ 0.18 (and not much worse) is that **natural images have low pixel variance once you normalize to [0,1]**. The standard deviation of pixel values in STL10 is roughly 0.15–0.25. If you replace every pixel with a single "plausible image color" you'll get an MAE close to that std. For reference:
- All-black prediction → MAE ≈ mean pixel value ≈ 0.45
- Uniform random noise prediction → MAE ≈ 0.33
- Mean-patch (this baseline) → 0.18
- Perfect reconstruction → 0

So 0.18 isn't a strong baseline. It's the "natural-image variance floor" you get for free by exploiting that pixels in a photo cluster around a mean color. Your network has to do meaningfully better than this to be worth anything.

**Q2 — Perfect permutation + no inpainting (black gaps): better or worse than baseline?**

Let me count the gap pixels precisely. Each 32×32 cell has its center 28×28 kept and a 2-pixel border eroded. In the full 96×96 image:
- Rows entirely missing: rows 0–1, 30–33, 62–65, 94–95 → **12 rows of gap**
- Same for columns → 12 columns of gap
- Kept pixels: 84 × 84 = 7056
- Total pixels: 9216
- **Gap fraction ≈ 23.4%**

If kept pixels are perfect (error 0) and gap pixels are filled with black:

```
MAE ≈ 0 × 0.766  +  (mean pixel value) × 0.234
     ≈ 0.45 × 0.234
     ≈ 0.105
```

So even with no inpainting at all, a perfect permutation network already gives you ~0.10 MAE — **beating the baseline by ~40%**. This is a big insight: the permutation problem is where most of the MAE budget lives.

**Q3 — Which subproblem contributes more to MAE?**

Permutation, by a large margin. Reasoning:

- A wrong-position patch contributes its full pixel-difference to MAE across all 784 of its pixels. Get one of 9 patches wrong → ~11% of your image is garbage.
- Inpainting only affects 23% of pixels, and even "dumb" inpainting (interpolate from neighbors) is much better than black — probably down to 0.02–0.03 MAE contribution.

So the priority ladder is:
1. **Get permutation right** → this alone takes you from 0.18 → ~0.10
2. **Decent inpainting** → takes you from ~0.10 → ~0.05
3. **Refinement / smoothing across seams** → final polish

This tells you the architecture: **a pipeline of two networks** (permutation predictor + inpainting/refinement) is the right move, and you should spend most of your engineering effort on the permutation stage. It also tells you that during development, you should monitor MAE *and* permutation accuracy separately so you know which stage is failing.

---

