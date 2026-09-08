 
### 1. The Generalized Hough Transform (GHT)

**(A) Introduction and Off-line Phase**
The Generalized Hough Transform (GHT) is a computer vision algorithm used to detect arbitrary, non-analytic shapes in an image. Unlike the standard Hough Transform, which is limited to parametric shapes like lines or circles, the GHT uses a template-based approach to find complex objects.

The object model in the GHT is represented by an **R-table**. The off-line phase builds this model from a template image of the target object:

1. **Reference Point:** A reference point (often the centroid), denoted as $(x_c, y_c)$, is chosen inside the object shape.
2. **Boundary Extraction:** Edge detection is applied to the template to extract the boundary pixels.
3. **Vector Calculation:** For every boundary pixel, the gradient angle $\phi$ is calculated. Then, a vector is drawn from the boundary pixel to the reference point. This vector is defined by its length $r$ and its angle $\alpha$ relative to the horizontal axis.
4. **R-table Construction:** The values of $r$ and $\alpha$ are stored in a table, indexed by the gradient angle $\phi$. Because multiple boundary points might share the same gradient angle, each index $\phi$ can contain a list of multiple $(r, \alpha)$ pairs.

*Graphical Representation Idea:* Imagine a 2D shape (e.g., a star) with a center dot $(x_c, y_c)$. A point on the edge has a perpendicular normal vector (angle $\phi$). An arrow points from this edge point to the center dot, labeled with length $r$ and angle $\alpha$.

**(B) On-line Phase**
During the on-line phase, the constructed R-table is used to locate the object in a new target image:

1. **Edge Detection:** Edges and their corresponding gradient angles $\phi$ are computed for the target image.
2. **Accumulator Array:** A 2D accumulator array (representing possible $(x_c, y_c)$ locations) is initialized to zero.
3. **Voting:** For every edge pixel $(x, y)$ in the target image with gradient angle $\phi$, the algorithm looks up $\phi$ in the R-table. For every $(r, \alpha)$ pair stored at that index, it calculates the candidate reference point coordinates using simple trigonometry:
$x_c = x + r \cos(\alpha)$
$y_c = y + r \sin(\alpha)$
The accumulator array bin corresponding to $(x_c, y_c)$ is incremented by 1.
4. **Detection:** The accumulator array is scanned for local maxima. A high peak indicates a strong consensus among edge pixels, revealing the location of the object.

**(C) Rotation and Scale Changes**
The basic GHT is highly sensitive to rotation and scale changes. If the target object is scaled, the lengths ($r$) will no longer match. If it is rotated, both the gradient angles ($\phi$) and the positional angles ($\alpha$) will shift, causing the votes to scatter.

*Possible Solutions:* To account for this, the accumulator array must be expanded into a 4D space (X, Y, Scale, Rotation). For every edge pixel, the algorithm must vote across a range of predefined scale factors and rotation angles. Alternatively, using rotation and scale-invariant local features (such as SIFT) instead of raw edge gradients allows for robust matching without exhaustive 4D voting.

---

### 2. Convolutional Neural Networks

**(A) Receptive Field**
The receptive field of an entry in a generic activation is defined as the specific area of input pixels that affect that particular hidden unit.

* **Number of layers:** The size of the receptive field grows as the number of layers increases.


* **Hyperparameters:** If layers only use a stride of 1, the receptive field grows linearly with depth. However, if strides greater than 1 or pooling layers are introduced, the receptive field grows exponentially with respect to the number of layers. To compute features for a large portion of the input with a limited number of layers, downsampling the activations is required.



**(B) General Equations and VGG Stages**
For a convolutional layer, the general equations are as follows:

* **Parameters:**
$$Parameters = C_{out}(C_{in}H_K W_K + 1)$$



Where $C_{out}$ is the number of output channels, $C_{in}$ is the number of input channels, $H_K$ and $W_K$ are the height and width of the kernel, and the $+ 1$ accounts for the bias term.


* **Output Activation Size:**
$$H_{out} = \lfloor \frac{H_{in} - H_K + 2P}{S} \rfloor + 1$$



Where $H_{in}$ is the input height, $P$ is the padding, and $S$ is the stride. (The formula for width $W_{out}$ is identical).


* **FLOPs:**
$$FLOPs = 2(C_{out}H_{out}W_{out})(C_{in}H_K W_K)$$



This accounts for the multiply-add operations performed across the entire output volume.



**VGG Stages:**
VGG introduced the concept of "stages," which are fixed combinations of layers that process activations at the exact same spatial resolution (e.g., a stack of conv-conv-pool).

* *Pros:* Stacking smaller convolutions (e.g., two 3x3 kernels) yields the exact same receptive field as a single larger convolution (e.g., a 5x5 kernel) but requires fewer parameters and significantly less computation. It also allows for the insertion of more non-linear activation functions.


* *Cons:* This approach increases the overall number of activations in the network, which effectively doubles the memory required to store them during the training process.



**(C) ResNet Block Design and Limitations**
When a standard residual block is the first block of a new stage in a ResNet, it must halve the spatial resolution and double the number of channels. Because the dimensions of the input no longer match the dimensions of the output, the residual skip connection cannot use a simple identity function. Instead, it uses a 1x1 convolution with a stride of 2 and $2C$ output channels to match the new dimensions.

* **Limitation:** The original design uses a 1x1 convolution with a stride of 2. Because of the stride, this 1x1 convolution skips over pixels, effectively ignoring 3/4 of the input activation data.


* **Proposed Modification (ResNet-D):** To overcome this, the architecture was modified to perform a 2x2 average pooling with a stride of 2 *before* applying a 1x1 convolution with a stride of 1. This ensures the entire input activation is factored into the downsampling process.



---

