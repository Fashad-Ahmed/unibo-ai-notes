Module 2 Foundations: 3D Vision and Deep Learning

This slide serves as the roadmap for the second half of your course. It visually summarizes the three major topics you are about to study.

1. Camera Models and Calibration (Left Side)

In the first half of the course, you treated an image simply as a 2D grid of pixels. Now, you are going to learn the physics and math of how that 2D grid is created from the 3D real world.

Look at the math pipeline in the top left. It shows the journey of a single point in space:

WRF (World Reference Frame): This is a 3D point in the real world $M_w = [x_w, y_w, z_w]^T$.

Extrinsic Parameters (R, t): The camera is located somewhere in the real world. By applying a Rotation matrix ($R$) and a translation vector ($t$), you convert the world coordinates into the Camera Reference Frame (CRF), $M_c$. This just means calculating where the object is relative to the camera's lens.

Intrinsic Parameters: Finally, the light passes through the lens and hits the sensor. Intrinsic parameters (focal length, optical center) and distortion coefficients calculate exactly which 2D pixel $m = [u, v]^T$ that 3D ray of light will hit.

The Checkerboard: The photo below the math shows a checkerboard. Because a checkerboard has perfectly known geometric squares, computer vision engineers take photos of it from different angles to mathematically reverse-engineer all those Intrinsic and Extrinsic parameters. This is called Camera Calibration.

2. Image Classification - Shallow ML (Top Right)

Look at the grid of blurry images labeled "plane, car, bird, cat..."
This represents traditional, "shallow" Machine Learning.

Before Deep Learning took over, researchers tried to classify images by training algorithms to learn a single, average "template" of an object.

Look at the "car" template: it looks like a blurry blob of a windshield and headlights.

Look at the "horse" template: it's a vague shape of a head facing left or right.

This method struggles in the real world because a car looks completely different from the side versus the front. A single "average" template cannot capture the high variability of real-world categories.

3. Convolutional Neural Networks (Bottom Right)

To solve the high variability problem, the field moved to Deep Learning.
The complex wireframe diagram at the bottom shows the architecture of a Convolutional Neural Network (CNN).

Instead of learning one blurry template, a CNN passes the image through dozens of 3D layers (the rectangular blocks in the diagram).

The early layers learn simple edges.

The middle layers combine edges to learn shapes (like wheels or eyes).

The final layers combine shapes to recognize complex objects (like a scooter or a leopard).

The Dense layers at the very end (on the far right) act as the final voting system, outputting the exact probability that the image belongs to a specific class (e.g., 90% chance it is a leopard, 10% chance it is a cheetah).