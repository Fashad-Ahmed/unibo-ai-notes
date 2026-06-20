![alt text](image-6.png)


Welcome to **Lecture 2: Camera Calibration**!

These title and intro slides perfectly set the stage for what we are about to do. They reiterate the exact transition we discussed at the end of the last module:

We are officially leaving the **Forward Model** (where we know the camera and want to find the pixel) and entering the **Inverse Problem**:

* **The Goal:** Estimate the 6 Extrinsic parameters, the 4 Intrinsic parameters, and the lens distortion coefficients.
* **The Method:** We are given $i$ number of pairs of known 3D World points ($M_W$) and their corresponding 2D pixel locations ($m$).

Now that the problem is formally defined, the next slides should dive into the actual algorithms used to mathematically crack this.

![alt text](image-7.png)


Calibration Patterns: How to get Ground Truth Data

To figure out the camera's parameters, we need pairs of 3D world points ($M_W$) and 2D pixels ($m$). To get the 3D world points, we use Calibration Patterns (usually checkerboards, because the corners are incredibly sharp and easy for a computer algorithm to detect).

There are two main mathematical approaches to calibration, based on the physical object you use:

1. The 3D Calibration Object (Top Right Image)

The Method: You build a 3D physical object with at least two orthogonal planes (like the inside corner of a box) and paste checkerboard patterns on them.

The Math: Because the object is truly 3D (it has depth, $X$, $Y$, and $Z$ variance in the real world), you technically only need to take a single photograph of it to mathematically calculate all of your camera parameters!

The Catch: As the slide notes, "it is difficult to build accurate targets containing multiple planes." If the two boards are angled at $89.5^\circ$ instead of exactly $90.0^\circ$, your entire math model will be corrupted. Manufacturing these objects with sub-millimeter precision is incredibly expensive and difficult.

2. The 2D Planar Pattern (Bottom Right Images)

The Method: You print a checkerboard on a single, flat piece of paper and glue it to a stiff, flat board.

The Math: Because the board is completely flat, $Z=0$ for every single point on the board. You don't have enough 3D depth data from a single photo to solve the math. Therefore, you must take several different images (at least 3, but usually 10-20) of the exact same board from different angles and distances.

The Advantage: This is the industry standard (often called Zhang's Method). It is incredibly cheap and easy to print a perfectly flat checkerboard on a piece of rigid glass or metal. Moving the camera around it 10 times is much easier than building a perfectly square 3D box.

Software Implementation

The slide ends with a note of relief: "Implementing a camera calibration software requires a significant effort." Writing the calculus optimization code to solve the non-linear distortion equations from scratch is a nightmare. Fortunately, nobody does it from scratch anymore. The math has been perfectly packaged into single lines of code in standard Computer Vision libraries:

OpenCV (C++ and Python) uses the cv2.calibrateCamera() function.

MATLAB has a dedicated, easy-to-use GUI called the Camera Calibration Toolbox.

![alt text](image-8.png)


![alt text](image-9.png)


Zhang's Method: The Industry Standard for Calibration

Zhang's method (published in 2000) revolutionized computer vision because it proved you don't need an expensive 3D calibration box. You can calibrate a camera using just a flat piece of paper (a planar pattern) shown from a few different angles.

The algorithm works in four major phases, starting with rough mathematical guesses and ending with a massive, highly precise optimization loop.

Phase 1: Data Collection (Blue Box)

Acquire $n$ images: You take several photos (usually 10 to 20) of a flat checkerboard from different angles and distances.

$c$ internal corners: A computer algorithm scans each image and finds the exact $(u, v)$ pixel coordinates of the checkerboard intersections.

Phase 2: Homographies (Top Green & Orange Boxes)

Because the checkerboard is perfectly flat, we can assume its $Z$-coordinate is always $0$. This magically simplifies our $3 \times 4$ Camera Matrix into a $3 \times 3$ matrix called a Homography ($H$).

Compute $H_i$: For every single image ($i$), the computer calculates a rough Homography matrix that maps the flat 3D checkerboard plane to the flat 2D image plane.

Refine $H_i$: It tweaks these matrices to minimize the Reprojection Error.

What is Reprojection Error? It is the distance in pixels between where the algorithm found the corner in the photo, and where the math predicts the corner should be. We want this error to be as close to 0 as possible.

Phase 3: The "Initial Guesses" (Middle Green Boxes)

Now that the computer has a set of highly accurate Homographies ($H_i$), it uses a clever set of linear algebra formulas to rip those Homographies apart into our standard camera parameters:

Guess $A$ (Intrinsics): It mathematically extracts the focal lengths ($f_u, f_v$) and principal point ($u_0, v_0$). Notice there is only one $A$ matrix, because the camera's internal hardware doesn't change between photos.

Guess $R_i$ and $t_i$ (Extrinsics): It calculates where the camera was physically located for each of the $n$ images.

Guess $k$ and $p$ (Distortion): It calculates a rough starting guess for the radial and tangential lens bending.

Phase 4: Global Non-Linear Optimization (Bottom Orange Box)

This is the grand finale. The "initial guesses" from Phase 3 are pretty good, but they were calculated in pieces and rely on linear approximations.

To get perfect, sub-pixel accuracy, Zhang's method takes all the parameters ($A$, all the $R_i$'s and $t_i$'s, and the distortion coefficients $k, p$) and throws them into a giant calculus optimization engine (usually the Levenberg-Marquardt algorithm).

It slightly nudges all the numbers up and down simultaneously, projecting the 3D points through the complete, non-linear image formation pipeline we learned in the last module, until the global reprojection error across all $n$ images is absolutely minimized.