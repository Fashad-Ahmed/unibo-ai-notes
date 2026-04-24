Sigmoid is not a different function; it is literally just Softmax applied to a 2-class problem.

### **1. The Setup: Probabilities (Sigmoid & Softmax)**
Before we can calculate a loss, the network's output must speak the language of probability.
As we discussed, your `mynet2` model outputs 10 raw numbers (logits). We apply **Softmax** (or **Sigmoid** for binary cases) to squish these logits into a predicted probability distribution, which we will call **$Q$**. 

Meanwhile, the dataset provides the ground truth label. If the image is a "7", the true probability distribution is $100\%$ for class 7 and $0\%$ for all others. We will call this true distribution **$P$**.

The goal of training is to make the predicted distribution $Q$ match the true distribution $P$ as closely as possible.

### **2. Entropy: Measuring Uncertainty**
In information theory, **Entropy** ($H$) measures the amount of chaos, uncertainty, or "surprise" inherent in a single probability distribution. 

For a true distribution $P(x)$, the Entropy is calculated as:
$$H(P) = - \sum_{x} P(x) \log P(x)$$

* **High Entropy:** The probabilities are spread out (e.g., a coin flip where $P(\text{heads}) = 0.5$ and $P(\text{tails}) = 0.5$). The outcome is highly uncertain.
* **Low Entropy:** The probabilities are concentrated. In deep learning classification tasks, your true labels are usually "one-hot" encoded (e.g., $[0, 0, 1, 0]$). The probability of the correct class is $1.0$. Because $\log(1) = 0$, the Entropy of a standard deep learning dataset is exactly **$0$**. There is no uncertainty in the ground truth.

### **3. Cross-Entropy: The Deep Learning Loss Function**
**Cross-Entropy** ($H(P, Q)$) is the standard loss function used for classification in modern neural networks. It measures how many "bits" of information are needed to represent an event from distribution $P$ if you incorrectly assume the distribution is $Q$.

Mathematically, it replaces the $\log$ term in the standard entropy formula with the $\log$ of our network's predictions:
$$H(P, Q) = - \sum_{x} P(x) \log Q(x)$$

**Why it works for Deep Learning:**
Because $P(x)$ is $0$ for all incorrect classes, the sum collapses. The only term that matters is the one where the true class $P(x) = 1$. The formula effectively simplifies to:
$$\text{Loss} = - \log(Q(\text{correct\_class}))$$

If your network predicts a $99\%$ probability ($0.99$) for the correct class, $-\log(0.99)$ approaches $0$ (low loss). If it confidently predicts a $1\%$ probability ($0.01$) for the correct class, $-\log(0.01)$ explodes to a massive number, heavily penalizing the network for being confident and wrong.

### **4. Kullback-Leibler (KL) Divergence: The Mathematical Bridge**
**KL Divergence** ($D_{KL}$) is a strict measure of how one probability distribution diverges from a reference distribution. It calculates the exact difference between Cross-Entropy and standard Entropy.

$$D_{KL}(P || Q) = \sum_{x} P(x) \log \left( \frac{P(x)}{Q(x)} \right)$$

This is arguably the most important relationship in deep learning optimization:
$$H(P, Q) = H(P) + D_{KL}(P || Q)$$
**(Cross-Entropy = Entropy + KL Divergence)**

**The "Aha!" Moment for Training:**
We want our network to minimize the difference between its predictions ($Q$) and the truth ($P$). Logically, we should ask the optimizer to minimize the KL Divergence. 

However, look at the equation above. The Entropy of our true labels $H(P)$ is a fixed constant (usually $0$, as the dataset doesn't change during training). Therefore, taking the derivative (the gradient) of Cross-Entropy is mathematically identical to taking the derivative of KL Divergence. 

We use **Cross-Entropy Loss** in practice because it is computationally simpler to calculate, but optimizing it achieves the exact theoretical goal of minimizing the KL Divergence between what the network believes and reality.

