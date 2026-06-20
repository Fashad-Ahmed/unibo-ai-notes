Noise in computer vision shows up as random variation in pixel values that doesn’t reflect the real scene. It can come from low light, sensor limitations, compression, or transmission errors. The trick is first recognizing what kind of noise you’re dealing with, then choosing a method that reduces it without destroying useful detail.

### Identifying noise

Start by inspecting the image statistically and visually:

* **Visual cues**

  * Grainy texture across the image → often Gaussian noise
  * Isolated white/black pixels → salt-and-pepper noise
  * Color speckles in dark areas → sensor or ISO noise

* **Histogram analysis**
  A noisy image often has a wider, less smooth intensity distribution.

* **Frequency domain**
  Using Fourier Transform, noise typically appears as high-frequency components.

* **Variance estimation**
  Flat regions (like sky or walls) should be smooth—high variance there signals noise.

* **Model-based detection**
  In Computer Vision pipelines, you can estimate noise using residuals from a denoising or reconstruction model.

---

### Common noise types

* **Gaussian noise** – random variation, usually from sensors
* **Salt-and-pepper noise** – dead pixels or transmission errors
* **Poisson noise** – photon-counting issues in low light
* **Speckle noise** – common in radar or medical imaging

---

### Reducing noise

Different techniques work better for different noise types:

#### 1. Spatial filtering

* **Gaussian blur**
  Smooths noise but can blur edges.
* **Median filtering**
  Excellent for salt-and-pepper noise; preserves edges better.
* **Bilateral filtering**
  Smooths while keeping edges sharp.

#### 2. Frequency domain filtering

* Remove high-frequency components after applying a Fourier Transform.
* Low-pass filters reduce noise but risk losing detail.

#### 3. Advanced denoising

* **Non-local means**
  Uses self-similarity across the image.
* **Wavelet denoising**
  Works well for separating signal and noise across scales.

#### 4. Deep learning approaches

* CNN-based denoisers (e.g., DnCNN) learn noise patterns directly.
* Autoencoders and diffusion models can reconstruct clean images.

#### 5. Practical tricks

* Capture multiple frames and average them.
* Use better lighting or lower ISO during acquisition.
* Apply normalization before feeding into models.

---

### Trade-offs to keep in mind

* More aggressive denoising = more detail loss
* Edge preservation is key for downstream tasks (like detection or segmentation)
* Real-time systems need lightweight filters; offline pipelines can use heavier models

---
