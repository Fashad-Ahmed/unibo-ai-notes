![alt text](image-1.png)


This slide kicks off the technical content for Module 2 by recapping the absolute most fundamental concept in 3D computer vision: **The Perspective Projection Model** (often called the Pinhole Camera Model).

Before we can teach a computer to understand 3D space, we have to define exactly how the 3D world gets squashed onto a flat 2D photograph. Here is a breakdown of the geometry and the math shown on the slide:

### 1. The Setup: The Camera Reference Frame (CRF)

Look at the diagram on the right. To do the math, we pin our 3D coordinate system directly to the camera itself.

* **The Origin ($C$):** The center of our 3D universe $(0,0,0)$ is placed exactly at the camera's lens (the optical center).
* **The Z-Axis:** This points straight out from the lens. It is called the **Optical Axis**. The $Z$ value of an object is simply its depth (how far away it is from the camera).
* **The Image Plane ($I$):** This is the camera sensor (or film) where the 2D picture is formed. It is positioned at a specific distance from the lens, known as the **focal length ($f$)**.

### 2. The Math: Similar Triangles (Equation 1)

If you have a physical point in the real world $M = [x, y, z]$, where exactly will it appear on your 2D screen $m = [u, v]$?

The light ray travels from the real-world object $M$, passes through the 2D image plane at $m$, and hits the lens $C$. This creates two perfect right triangles that share the same angle. Using the geometry of "similar triangles," we get the formulas:

* **$u = f \frac{x}{z}$** (for the horizontal pixel position)
* **$v = f \frac{y}{z}$** (for the vertical pixel position)

### 3. What this equation actually means in real life

Look closely at the division by $Z$. This is the mathematical proof of why **objects look smaller as they get further away**.

* If a person ($X$ height) stands 5 meters away ($Z=5$), they take up a certain number of pixels ($u$) on your screen.
* If that same person walks 100 meters away ($Z=100$), you are dividing by a much larger number. Their pixel size ($u$) shrinks drastically.

### 4. The Headache: "Non-Linear Equations"

Notice that the slide explicitly highlights in blue that these are **non-linear equations**.
In linear algebra, computers love multiplying matrices to solve problems (e.g., $A \cdot x = B$). But you *cannot* use standard matrix multiplication if you have a variable ($z$) in the denominator of a fraction!

Because dividing by depth ($z$) ruins standard linear algebra, the very next thing you will likely learn is a clever mathematical trick called **Homogeneous Coordinates**, which allows us to "fake" this division so we can put all of this camera physics into a clean, solvable matrix.


![alt text](image.png)



Why Do We Need an Image Formation Model?

In the previous slide, we looked at the math of how a 3D point is flattened onto a 2D image plane (Perspective Projection). It can seem tedious, but these two slides show you the spectacular things you can build once you understand that math.

If you know the exact mathematical model of how a camera creates an image, you can run that math in reverse.

Slide: 3D Point Cloud Reconstruction

The image on Slide 3 shows a 3D point cloud of a castle. This was likely generated from dozens or hundreds of standard 2D photographs (perhaps taken by a drone flying around it).

This process is called Structure from Motion (SfM) or 3D Reconstruction.

If you take photos of a castle from many different angles, and you find matching SIFT features across those photos...

AND you know the Image Formation Model (the focal length of the camera, and exactly where the camera was in 3D space for every photo)...

You can triangulate the rays of light backwards from the 2D pixels out into virtual 3D space to find exactly where they intersect.

Knowing the camera model allows the computer to "un-flatten" the 2D photos back into a full 3D geometric map!

Slide: NeRF (Neural Radiance Fields)

Slide 4 jumps straight into the cutting edge of modern computer vision. The images shown (the Lego bulldozer, the hotdog, the chair) are from a revolutionary 2020 paper introducing NeRFs.

What is a NeRF?
NeRF stands for Neural Radiance Field. It is an AI model that learns to represent a continuous 3D scene.

You feed the AI a dataset of 2D photos of an object taken from various angles.

The AI learns the density and color of every single microscopic point of light in that 3D space.

Once trained, you can ask the AI to render a brand new, photorealistic 2D image of the object from an angle that the camera never even took a picture from. This is called Novel View Synthesis.

Why is it on this slide?
You might think, "If NeRF uses deep learning AI, why do we care about the old classical camera math?"

Because the AI cannot learn without the camera model. To train a NeRF, every single 2D training photo you feed into the neural network MUST be accompanied by its exact camera pose (its 3D location, rotation, and lens properties). The AI uses the perspective projection math to shoot virtual "rays" through the pixels of the 2D images to figure out how to build the 3D object.

The Takeaway: The "classical" math of how cameras work isn't obsolete—it is the foundational bedrock that allows modern Deep Learning AI to understand 3D space!