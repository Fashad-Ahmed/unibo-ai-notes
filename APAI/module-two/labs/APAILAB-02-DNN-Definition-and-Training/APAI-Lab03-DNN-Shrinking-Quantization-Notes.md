# APAI Lab 03 — DNN Shrinking and Quantization

> **Course:** Architecture of AI / APAI · University of Bologna · 2026–2027  
> **Topics:** CNN shrinking, MACs, linear quantization, clipping, calibration, PTQ, Brevitas, fake quantization, QAT, STE, DeepQuant, ONNX, Netron  
> **Source:** `LAB03_2026_2027.pdf` and `APAI26-LAB3-DNN-Shrinking-and-Quantization.ipynb`  
> **Results:** Measurements from my Lab 03 experiments. Values can change with seeds, training, calibration and framework versions.

## Table of contents

1. [Objectives and workflow](#1-objectives-and-workflow)
2. [CNN architecture and shrinking](#2-cnn-architecture-and-shrinking)
3. [Linear quantization mathematics](#3-linear-quantization-mathematics)
4. [Quantization error and clipping](#4-quantization-error-and-clipping)
5. [PTQ, calibration and Brevitas](#5-ptq-calibration-and-brevitas)
6. [Quantization-aware training and STE](#6-quantization-aware-training-and-ste)
7. [Lab experiments and results](#7-lab-experiments-and-results)
8. [Fake-to-true quantization and DeepQuant](#8-fake-to-true-quantization-and-deepquant)
9. [ONNX and Netron inspection](#9-onnx-and-netron-inspection)
10. [Exam questions and key distinctions](#10-exam-questions-and-key-distinctions)
11. [Quick reference](#11-quick-reference)

---

## 1. Objectives and workflow

The goal is to reduce the compute and storage costs of a CNN without unnecessarily sacrificing classification accuracy. The lab starts from the Fashion-MNIST CNN used in Lab 02 and follows this sequence:

```text
Pretrained float32 CNN
       |
       v
Reduce channels (shrinking) -> retrain reduced CNN
       |
       v
Quantize a weight tensor manually; examine bit width and clipping
       |
       v
Build Brevitas fake-quantized CNN; calibrate activation ranges (PTQ)
       |
       +--> Evaluate low-bit PTQ (8, 6, 4, 3, 2 bits)
       |
       +--> Fine-tune low-bit CNN using QAT + STE
       |
       v
Convert the 8-bit PTQ model using DeepQuant (fake -> true)
       |
       v
Export ONNX graphs and inspect in Netron
```

**Crucial distinction:** *Shrinking* changes the architecture (channels, layers, stride). *Quantization* changes numeric precision. A model can use either or both.

## 2. CNN architecture and shrinking

### 2.1 Original CNN

The model classifies grayscale **28 × 28** Fashion-MNIST images into **10 classes**.

| Stage | Original output shape (channels × height × width) | Main operation |
|---|---:|---|
| Input | `1 × 28 × 28` | Grayscale image |
| Block 1 | `32 × 28 × 28` | `Conv3×3 → BN → ReLU`, stride 1 |
| Block 2 | `64 × 28 × 28` | `Conv3×3 → BN → ReLU`, stride 1 |
| Pool | `64 × 14 × 14` | MaxPool 2×2 |
| Block 3 | `128 × 7 × 7` | `Conv3×3 → BN → ReLU`, stride 2 |
| Flatten | `6272` | `128 × 7 × 7` |
| Classifier | `10` | Dropout, fully connected, class scores |

These shapes assume the convolution padding used by the notebook to produce the dimensions shown in the lecture. ReLU is `max(0,x)`; BN normalizes intermediate activations; pooling reduces spatial resolution; flatten makes a feature vector. Softmax may be used to interpret output scores as probabilities, although cross-entropy training in PyTorch normally expects raw logits.

### 2.2 Three shrinking techniques

1. **Reduce output channels** (lab task): `32 → 16`, `64 → 32`, `128 → 64`. Fewer feature maps mean less work and fewer learned weights.
2. **Remove layers/blocks** (lecture example): fewer operations, but reduced model capacity and possible need to reconnect layers.
3. **Increase stride** (lecture example): stride 2 may reduce a `28×28` feature map to `14×14`, making subsequent operations cheaper, but discarding spatial detail. Especially risky for already-small inputs.

The reduced architecture is:

```text
Input: 1×28×28
Conv(1→16, 3×3, stride 1) → BN → ReLU     : 16×28×28
Conv(16→32, 3×3, stride 1) → BN → ReLU    : 32×28×28
MaxPool(2×2)                             : 32×14×14
Conv(32→64, 3×3, stride 2) → BN → ReLU    : 64×7×7
Flatten                                  : 64·7·7 = 3136
Linear(3136→10)                          : 10 scores
```

The next convolution's **input channel count must match the previous convolution's output**.

### 2.3 Parameters versus MACs

For a standard convolution without bias:

$$P = C_{\mathrm{out}} C_{\mathrm{in}} K_h K_w$$

Approximate multiply-accumulate count:

$$\mathrm{MACs} = H_{\mathrm{out}}W_{\mathrm{out}}C_{\mathrm{out}}C_{\mathrm{in}}K_hK_w$$

For a dense layer, MACs are roughly `in_features × out_features`.

Example, second convolution:

- Original: `64×32×3×3 = 18,432` convolutional weights.
- Reduced: `32×16×3×3 = 4,608` convolutional weights.
- **75% fewer Conv2 weights**, because *both* the input and output channels are halved.

**Lab measurement:** original CNN ~**18.3M MACs**; reduced CNN ~**4.66M MACs**, meeting the **< 5M MAC** target. MACs measure arithmetic workload, not model file size or measured runtime.

### 2.4 Why retrain?

The original weights were learned for a specific arrangement of feature maps. Shrinking changes the topology and input activation distributions of downstream layers. The smaller model needs training or fine-tuning to recover useful representations. Retaining compatible pretrained weights can make fine-tuning faster, but merely changing channel counts is not automatically a valid pretrained-weight transfer.

---

## 3. Linear quantization mathematics

A float32 weight can hold many fractional values. Low-bit quantization approximates them by a finite set of integer codes.

The lecture's **symmetric, per-tensor, uniform quantizer** uses:

$$q_{\max} = 2^{N-1}-1$$

$$s = \frac{x_{\max}}{q_{\max}}$$

$$q = \operatorname{clamp}\left(\operatorname{round}\left(\frac{x}{s}\right),-q_{\max},q_{\max}\right)$$

$$\hat{x} = s q$$

Here `N` is bit width, `x_max` is a symmetric clipping bound, `s` is the quantization **scale**, `q` the integer code, and `x_hat` the reconstructed approximation. All values in a *per-tensor* quantizer share the same scale.

| N | `q_max` | Symmetric levels supported by this formula |
|---:|---:|---:|
| 8 | 127 | 255 (`-127...127`) |
| 6 | 31 | 63 |
| 4 | 7 | 15 |
| 3 | 3 | 7 |
| 2 | 1 | 3 (`-1,0,+1`) |

**Worked example:** `N=4`, `x_max=0.7`, `x=0.26`:

1. `q_max = 7`.
2. `s = 0.7 / 7 = 0.1`.
3. `q = round(0.26 / 0.1) = 3`.
4. `x_hat = 3 × 0.1 = 0.3`.
5. Absolute error `|0.26 - 0.3| = 0.04`.

Equivalent PyTorch implementation for the lecture's quantizer:

```python
import torch

def quantize_symmetric(x: torch.Tensor, bit_width: int, x_max=None):
    q_max = 2 ** (bit_width - 1) - 1
    if x_max is None:
        x_max = x.abs().max()
    scale = x_max / q_max
    q = torch.clamp(torch.round(x / scale), -q_max, q_max)
    return q, scale

# Reconstruction: x_hat = q * scale
```

This example assumes a nonzero scale. Production quantizers must also handle all-zero tensors and any zero-point conventions.

### 3.1 Why use fewer bits?

- Float32 weights: **32 bits = 4 bytes** per value.
- Int8: **8 bits = 1 byte** per value (4× smaller raw weight storage).
- Packed 4-bit values use 0.5 byte/value on average; packed 2-bit values 0.25 byte/value, excluding padding/scales/metadata.

These storage savings only apply when the deployed representation actually packs/stores low-bit integers; **fake quantization can still use float32 storage and arithmetic**. Speedups require matching hardware/kernel support and are not automatic.

### 3.2 Symmetric and affine quantization

For symmetric quantization, zero typically maps to integer 0. A more general affine convention uses a zero-point `z`:

$$x \approx s(q-z)$$

The lab's Netron output includes signed `-128...127` clip ranges for weights and `0...255` for some activation stages. These full 8-bit ranges need not use exactly the same endpoint convention as the teaching formula above.

---

## 4. Quantization error and clipping

### 4.1 Error types

**Rounding error:** a value inside the quantizer's range maps to the nearest representable level. For uniform nearest-neighbor rounding:

$$|x-\hat{x}| \leq s/2 \quad \text{(provided }|x|\leq x_{\max}\text{)}$$

**Clipping error:** an outlier outside the supported range is saturated at the boundary. It can exceed `s/2`.

Metrics:

$$\mathrm{MAE}=\frac1n\sum_i |x_i-\hat x_i|$$

$$\mathrm{MSE}=\frac1n\sum_i (x_i-\hat x_i)^2$$

$$E_{\max}=\max_i |x_i-\hat x_i|$$

### 4.2 Lab: bit-width vs weight reconstruction error

| Precision | Scale | Distinct levels used | Mean absolute error | Maximum absolute error |
|---|---:|---:|---:|---:|
| 8-bit | 0.00080 | 234 | 0.00020 | 0.00040 |
| 4-bit | 0.01447 | 15 | 0.00359 | 0.00723 |
| 2-bit | 0.10127 | 3 | 0.02698 | 0.05063 |

**Interpretation:** fewer bits increase level spacing and weight reconstruction error. The measured maxima were approximately `scale/2`, consistent with rounding inside the quantization range.

### 4.3 Histograms and staircase plot

- A **weight histogram** shows where float32 weights are concentrated.
- Red vertical markers indicate allowable reconstructed values.
- On a plot of original `x` against quantized `x_hat`, the float identity is a diagonal line and quantization is a **staircase**: intervals of inputs map to the same output.
- The vertical distance between staircase and diagonal represents quantization error.

### 4.4 Percentile clipping

The lab selects the bound with:

```python
x_max = torch.quantile(w.abs(), percentile / 100)
```

Clipping the largest absolute values decreases `x_max` and therefore `s`, improving precision for typical in-range values. But too much clipping saturates many outliers and increases their errors.

**Measured 4-bit MSE:**

| Percentile | `x_max` | MSE |
|---:|---:|---:|
| 100% | 0.1013 | 1.72e-5 |
| 99.9% | 0.0882 | 1.33e-5 |
| **99%** | **0.0740** | **9.92e-6 (best)** |
| 95% | 0.0622 | 1.10e-5 |

**Measured 8-bit MSE:**

| Percentile | `x_max` | MSE |
|---:|---:|---:|
| **100%** | **0.1013** | **5.31e-8 (best)** |
| 99.9% | 0.0882 | 8.26e-8 |
| 99% | 0.0740 | 7.33e-7 |
| 95% | 0.0622 | 4.81e-6 |

**Conclusion:** moderate clipping helped at 4 bits because lower rounding error outweighed saturation of a few weights. It hurt at 8 bits because rounding was already fine-grained, so clipping error dominated. These are *weight reconstruction MSE* results, **not CNN classification accuracy**.

---

## 5. PTQ, calibration and Brevitas

### 5.1 Post-Training Quantization (PTQ)

PTQ changes the quantization representation **after** conventional float32 training, without gradient-based retraining of model weights. It uses observed or known ranges to choose scales. It is relatively inexpensive, but extremely low precision can cause significant accuracy loss.

### 5.2 Calibration

Weights are available directly, but activation distributions depend on the input images. **Calibration** runs a representative subset through the network to estimate suitable activation ranges/scales. In this lab, activation ranges are determined using the **99.999th percentile**. Calibration is *not* backpropagation; it measures statistics and establishes quantizer parameters.

### 5.3 Fake quantization (FQ)

Fake quantization applies rounding/clipping in the forward path but still relies on floating-point values/operations. It simulates the numerical effect of a low-bit model and supports training. A fake-quantized PyTorch graph should **not** automatically be described as an integer-only deployable model.

### 5.4 Brevitas workflow from the lecture

1. **Deep-copy** `net_reduced` to keep a clean float32 baseline.
2. **Equalize** with SmoothQuant-style weight/activation redistribution to reduce activation outlier difficulty while approximately preserving outputs.
3. **Preprocess** using `torch.fx`; merge compatible BatchNorm into Conv.
4. **Quantize modules** through compute/activation/identity maps, e.g., PyTorch Conv → Brevitas `QuantConv2d`.
5. **Calibrate** activation ranges on a representative training subset.

The lab's intended settings include signed 8-bit weight and activation quantizers, per-tensor weight scales, and int32 bias/accumulation behavior. Its named Brevitas quantizers include `Int8WeightPerTensorFloat`, `Int8ActPerTensorFloat`, `Uint8ActPerTensorFloat`, and `Int32Bias`.

### 5.5 Why fuse BatchNorm into Conv?

At evaluation time BN is an affine transform using fixed running statistics. For `y = Wx+b` and BN parameters `gamma, beta, mu, variance`:

$$W' = \frac{\gamma}{\sqrt{\sigma^2+\epsilon}}W$$

$$b' = \frac{\gamma(b-\mu)}{\sqrt{\sigma^2+\epsilon}}+\beta$$

Folding BN into a convolution simplifies inference while preserving its evaluation-time function up to numerical effects.

---

## 6. Quantization-aware training and STE

**QAT** trains/fine-tunes the model with quantization simulated during forward passes, so the weights adapt to low precision. It is especially useful at low bit widths where PTQ introduces large distortions.

```text
Float32 master weights
      -> fake quantize (round + clamp) -> forward -> loss
      <- surrogate gradients through quantizers (STE) <- backprop
      -> update float32 weights and trainable quantizer parameters
```

### 6.1 Why use the Straight-Through Estimator (STE)?

`round(x)` has derivative zero almost everywhere, which would obstruct ordinary backpropagation. STE substitutes a usable surrogate gradient, often treating rounding like the identity inside the quantizer's valid range and assigning zero gradient beyond clipping bounds. It is **not** the exact mathematical derivative.

### 6.2 Why retain float32 master weights?

Small optimizer updates would disappear if weights were stored and rounded to integers after every update. Keeping trainable float32 weights allows small changes to accumulate, while forward passes simulate quantized inference.

### 6.3 Why not recalibrate after QAT in this lab?

The lab trains activation scales with model weights. Another calibration pass could overwrite the learned scales. This reflects the lab's particular quantizer setup, rather than a universal prohibition on recalibration.

---

## 7. Lab experiments and results

> **Accuracy values are validation accuracies.** `pp` means **percentage points**, not percentage change. Float32 baselines and sweeps were evaluated separately, so some rounded figures vary slightly among runs.

### 7.1 Standalone comparison: 8-bit PTQ and 3-bit QAT

| Setup | Validation loss | Accuracy |
|---|---:|---:|
| Reduced CNN, 8-bit PTQ | 0.2994 | 89.36% |
| Reduced CNN, 3-bit PTQ | 2.1908 | 50.34% |
| Reduced CNN, 3-bit after 1 epoch QAT | 0.4841 | 81.47% |

**3-bit QAT recovered 81.47 − 50.34 = 31.13 pp** in this particular run. QAT greatly mitigated PTQ damage, though accuracy remained below the float32 baseline.

### 7.2 Systematic reduced-CNN sweep

The notebook compares **PTQ without equalization**, **PTQ with equalization**, and **PTQ + one epoch of QAT**. QAT in the systematic sweep uses a subset of 10,000 training images.

| Weight/activation bits | Reduced PTQ (with equalization) | Reduced PTQ + QAT |
|---:|---:|---:|
| 8 | ~89.4% | 89.77% |
| 6 | ~89.4% | 89.60% |
| 4 | ~86.9% | 87.29% |
| 3 | 50.34% | 80.11% |
| 2 | ~9.7% | 12.31% |

- **8 and 6 bits:** PTQ was close to float32 accuracy; QAT added little.
- **4 bits:** modest accuracy degradation began.
- **3 bits:** severe PTQ degradation, with substantial QAT recovery.
- **2 bits:** both PTQ and one-epoch QAT were poor, near chance for 10 balanced classes.
- **Equalization:** PTQ curves with and without equalization nearly overlapped in this experiment; the benefit was small.

### 7.3 Original vs. reduced CNN: which is more robust?

To compare architectures fairly, measure each one's drop from **its own** float32 baseline:

$$\Delta A_{\mathrm{pp}} = 100\,(A_{\mathrm{float}}-A_{\mathrm{quantized}})$$

Float32 baselines:

- Original CNN: **90.19%**.
- Reduced CNN: **89.41%**.

**PTQ accuracy drops** (positive = worse than own float32 baseline):

| Bits | Original CNN drop | Reduced CNN drop |
|---:|---:|---:|
| 8 | 0.05 pp | 0.06 pp |
| 6 | -0.05 pp | 0.06 pp |
| 4 | 1.82 pp | 2.48 pp |
| **3** | **14.89 pp** | **39.07 pp** |
| 2 | 77.68 pp | 79.74 pp |
| **Mean across these five bit widths** | **18.88 pp** | **24.28 pp** |

**Observed conclusion:** the **original CNN was more robust to PTQ** across this sweep, especially at **3 bits**. It retained ~75.3% PTQ accuracy versus ~50.3% for the reduced CNN. A plausible explanation is that the original CNN's larger channel counts (`32, 64, 128` versus `16, 32, 64`) give greater representational capacity/redundancy; this is an interpretation, not a universal guarantee that bigger CNNs quantize better.

QAT also helped the original at low precision:

| Model at 3 bits | PTQ accuracy | QAT accuracy |
|---|---:|---:|
| Original CNN | ~75.3% | 84.39% |
| Reduced CNN | ~50.3% | 80.11% |

At **2 bits**, both architectures performed poorly even with one epoch of QAT. At **8 bits**, QAT may exceed float32 accuracy marginally because it provides **an extra epoch of optimization**; attributing any improvement solely to quantization would require a matched float32 fine-tuning control.

---

## 8. Fake-to-true quantization and DeepQuant

**Fake quantization:** simulated low-precision rounding, generally with float operations and stored float weights.  
**True quantization:** a deployable integer-oriented representation with frozen quantization parameters and integer math for the relevant operations.

The lecture's real-inference pattern is:

```text
Int8 activations × Int8 weights
       -> Int32 convolution accumulation
       -> rescale + round + clamp (requantization)
       -> Int8 activations for next layer
```

Why int32? The sum of many 8-bit products can exceed an int8 range.

A simplified zero-centered requantization formula is:

$$q_y = \operatorname{clamp}\left(\operatorname{round}\left(\frac{s_xs_w}{s_y}a_{32}\right),q_{\min},q_{\max}\right)$$

where `a32` is an integer accumulated value and `s_x`, `s_w`, `s_y` are input, weight and output scales. Exact implementation may include bias and zero-points.

**Lab detail:** the conversion uses **`qnet` (8-bit PTQ)**, *not* the separately fine-tuned 3-bit `qnet_3b`:

```python
sampleInput = torch.randn(1, 1, 28, 28)
tqnet = brevitasToTrueQuant(
    qnet, sampleInput, exportPath="./DeepQuantTest", debug=True
)
```

DeepQuant is described in the slides as a PULP-platform tool. The lab advises checking consistency between converted and original predictions and validating accuracy. The conversion can report an inconsistency error; the notebook suggests rerunning that cell.

---

## 9. ONNX and Netron inspection

**ONNX** (*Open Neural Network Exchange*) is a portable representation of a model's computational graph, parameters and operator attributes. **Netron** is a visualization tool for inspecting such graphs: <https://netron.app>.

### 9.1 Non-quantized reduced CNN

The float32 graph is compact:

```text
Input -> Conv -> ReLU -> Conv -> ReLU -> MaxPool
      -> Conv -> ReLU -> Flatten -> MatMul -> Output
```

**Observed in Netron:**

- Convolution weight type: **float32**.
- At least some weights have nonzero fractional parts.
- Example **actual first-convolution weight:** `1.7188761234283447` (Netron's maximum weight statistic).
- First three Conv weight shapes: `(16,1,3,3)`, `(32,16,3,3)`, `(64,32,3,3)`.
- Thus **all three convolution kernels are 3×3**.

### 9.2 Quantized CNN

**Observed in Netron:**

- Input tensor: `1 × 1 × 28 × 28` (batch 1, grayscale channel 1, height/width 28).
- Conv kernel shapes still **3×3**.
- Weight-side branches include **`Round -> Clip`** before Conv, eliminating fractional parts of the *quantized values*.
- Signed weight clip range: **`-128` to `127`** (256 integer codes = **8-bit signed numerical range**).
- Some activation clip ranges: `0...255` (unsigned 8-bit) or `-128...127` (signed 8-bit), depending on stage.
- Bias branches show an int32-like clip range (approximately ±2.147 billion).
- Extra nodes (`Div`, `Add`, `Round`, `Clip`, `Sub`, `Mul`) reflect scaling and quantization/requantization operations.

**Careful dtype distinction:** A `Round -> Clip(-128,127)` graph proves that its *values* are constrained to signed 8-bit integer levels; it does **not on its own prove that ONNX stores every intermediate tensor as the `int8` dtype**. Check the tensors' `type` and any `Cast` operations to assert the actual storage datatype. This is especially important when interpreting a lowered or simulated quantized graph.

### 9.3 What to look for in Netron

| Operator | Role |
|---|---|
| `Conv` | Convolution |
| `MatMul` / `Gemm` | Fully connected calculation |
| `MaxPool` | Downsampling |
| `Flatten` | Tensor reshape into a feature vector |
| `Div`, `Mul` | Apply quantization scales / rescale |
| `Add`, `Sub` | Apply or remove offsets |
| `Round` | Map to integer-valued levels |
| `Clip` | Saturate to allowed range |

---

## 10. Exam questions and key distinctions

**Q: Does smaller model size imply faster inference?**  
A: Not always. Actual speed depends on hardware, memory bandwidth, available kernels and operator overhead. MACs are an approximate arithmetic cost metric.

**Q: Difference between parameters and MACs?**  
A: Parameters measure the number of learned values, whereas MACs count multiply-accumulate work for a given input shape.

**Q: Why retrain after shrinking?**  
A: The changed channel/layer arrangement changes the features and distributions; training adapts weights to the new architecture.

**Q: Difference between PTQ and QAT?**  
A: PTQ quantizes a pretrained model without training its weights; QAT fine-tunes it while simulating quantization, using gradients.

**Q: Is fake quantization the same as integer-only inference?**  
A: No. Fake quantization simulates low-bit effects, often in float operations; true quantization implements an integer-oriented graph.

**Q: Why is low-bit PTQ harder?**  
A: Fewer levels lead to larger rounding/clipping errors that the pretrained network was not optimized to tolerate.

**Q: Why does STE exist?**  
A: Rounding has zero derivative almost everywhere; STE substitutes a surrogate gradient for QAT backpropagation.

**Q: Why int32 accumulation for int8 arithmetic?**  
A: Accumulating many int8 products requires a larger numerical range.

**Q: Why can 8-bit QAT slightly outperform an earlier float32 checkpoint?**  
A: An extra fine-tuning epoch can improve optimization. Compare against a float32 control trained for the same extra steps before crediting quantization.

**Q: Does activation equalization always improve PTQ?**  
A: No. In this lab, with- and without-equalization PTQ curves nearly overlapped.

**Q: Is a more accurate model necessarily more robust to quantization?**  
A: No. Compare **accuracy drop relative to each model's own baseline**. This experiment found the original CNN was more robust, particularly at 3 bits.

---

## 11. Quick reference

| Concept | Definition |
|---|---|
| Channel shrinking | Reduce number of Conv output feature maps |
| Stride shrinking | Increase spatial step to reduce output feature map size |
| PTQ | Quantize a model after conventional training |
| Scale `s` | Distance between adjacent reconstructed levels |
| `q_max` | Largest positive quantization index in symmetric convention |
| Clipping | Saturate values outside quantizer's supported range |
| Calibration | Estimate activation ranges using representative inputs |
| Fake quantization | Simulate low precision while retaining trainability |
| QAT | Fine-tune using fake quantization in forward passes |
| STE | Surrogate gradient through discrete rounding |
| Equalization | Redistribute weight/activation scales to aid quantization |
| Requantization | Convert higher-precision accumulators to the next low-bit range |
| DeepQuant | Tool used to convert Brevitas FQ to integer-oriented inference graph |
| ONNX | Portable computational graph/model representation |
| Netron | Graph and tensor inspector for model files |

### Final takeaways

1. **Shrinking** reduced this CNN from ~18.3M to ~4.66M MACs.
2. **8-bit PTQ** retained roughly float32-level validation accuracy (~89%).
3. **3-bit PTQ** suffered a large accuracy drop; **QAT** recovered over 30 pp in the standalone reduced-model run.
4. **2-bit** was too aggressive for these settings: one-epoch QAT remained poor.
5. **Original CNN** was more robust to PTQ than the reduced CNN, especially at 3 bits.
6. **Netron** revealed the 3×3 convolution kernels and quantization operations/ranges in the exported graph.

---

## References

- Course lecture: `LAB03_2026_2027.pdf` (APAI Lab 03: DNN Shrinking and Quantization).
- Course practical: `APAI26-LAB3-DNN-Shrinking-and-Quantization.ipynb`.
- [Brevitas documentation](https://xilinx.github.io/brevitas/)
- [ONNX](https://onnx.ai/)
- [Netron](https://netron.app/)

> These are lecture-and-lab study notes. The numerical tables are from the lab runs described above; qualitative explanations (e.g., redundancy contributing to robustness) are interpretations, not separately established causal proofs.
