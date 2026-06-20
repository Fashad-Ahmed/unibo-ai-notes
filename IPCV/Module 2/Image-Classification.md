Training Linear Classifiers

We know the formula for our model is $f(x; W, b) = Wx + b$.
But how do we find the perfect weights ($W$) and biases ($b$) so the network stops guessing randomly and actually recognizes objects? This process is called Learning as Optimization.

Part 1: The Intuition of "Template Matching"

Before we train the network, it helps to understand what the matrix $W$ actually is.
If you take a single row of the $W$ matrix (e.g., the row responsible for predicting "Car") and "unflatten" it back into a $32 \times 32$ image, you can literally see what the network is looking for!

The matrix multiplication $Wx$ is mathematically identical to a dot product or correlation.

The network is taking the input image and sliding it over a learned "template" to see how closely the pixels match.

Part 2: The Need for a "Loss Function"

To train the network, we show it a picture of a bird, let it guess, and then penalize it if it gets the answer wrong.

Why can't we just use Accuracy (0-1 Loss)?
Slide 28 shows the "0-1 Loss". This means we just count the number of errors.

The Problem: Accuracy is a staircase. If you slightly tweak a parameter knob ($\theta$), the number of errors might not change at all. The computer has no idea if that slight tweak made the model almost right or completely wrong.

The Solution: We need a smooth, continuous Loss Function (a proxy for accuracy). A smooth curve tells the computer: "You are still wrong, but you are getting warmer! Keep tweaking the knob in that direction!"

Part 3: Softmax and Cross-Entropy Loss

Raw scores (logits) from $Wx+b$ are messy. They can be massive positive numbers ($253$) or negative numbers ($-63$). We need to convert them into clean percentages.

Step 1: The Softmax Function

To turn raw scores into a valid Probability Distribution (where all numbers are between 0 and 1, and they all add up to 100%), we use the Softmax function:


$$p_j = \frac{\exp(s_j)}{\sum \exp(s_k)}$$

We take $e$ to the power of the score. This forces all negative scores to become positive.

We divide by the sum of all exponentiated scores. This perfectly scales them so they add up to exactly $1.0$ (or 100%).

Step 2: Cross-Entropy Loss

Now that we have clean probabilities, we calculate the penalty (the Loss). We want to maximize the probability of the correct Ground Truth class.
In math, maximizing a probability is identical to minimizing the negative log-probability:


$$L_i = -\log(p_{correct})$$

If the network is 90% sure the image is a bird ($0.9$), $-\log(0.9) = \mathbf{0.10}$ (A very tiny penalty!).

If the network is only 9% sure the image is a bird ($0.09$), $-\log(0.09) = \mathbf{2.40}$ (A massive penalty!).

(PyTorch Note: CrossEntropyLoss automatically does both the Softmax and the Negative Log math for you in one step!)

Part 4: Gradient Descent (How the computer learns)

Now that we have a mathematical penalty ($L$), we use calculus to update our parameters ($\theta$). We calculate the Gradient (the derivative of the loss with respect to the weights), which points exactly in the direction of the steepest error. We then take a small step in the opposite direction to reduce the error.

$$\theta_{new} = \theta_{old} - (learning\_rate \times gradient)$$

There are three ways to do this:

Batch Gradient Descent: Calculate the gradient across all 1.3 million images in ImageNet before taking a single step. Result: Way too slow.

Stochastic Gradient Descent (SGD): Calculate the gradient for exactly ONE image, take a step, then do the next image. Result: Too erratic and chaotic.

Mini-Batch SGD (The Industry Standard): Grab a small handful of images (e.g., a batch of 32, 64, or 256). Average their gradients together and take a step. Result: The perfect sweet spot! It smooths out the chaos and perfectly utilizes the massive parallel processing cores of modern GPUs.

Part 5: The Fatal Flaw of Linear Models

Look at Slide 44. This is what happens if you successfully train a Linear Classifier on the CIFAR-10 dataset. Look closely at the learned "templates" for each class.

The "Car" template looks like a blurry red blob over a blue background.

The "Horse" template actually looks like a two-headed horse! (One head facing left, one facing right).

Why does this happen?
A linear classifier is only allowed to learn ONE single template per class. To minimize the loss, it literally has to average every single picture of a horse into one image. If half the dataset has horses looking left, and half looking right, the math forces the template to have two heads!

Because of this limitation, a pure Linear Classifier is capped at around 38% accuracy on CIFAR-10.