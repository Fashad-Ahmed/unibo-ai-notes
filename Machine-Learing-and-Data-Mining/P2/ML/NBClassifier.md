Below is a **clear, exam-ready explanation** of the **Gaussian Naive Bayes (GNB) classifier**, written the way examiners expect it.

---

## 1️⃣ What is Gaussian Naive Bayes?

**Gaussian Naive Bayes** is a **supervised classification algorithm** based on:

* **Bayes’ Theorem**
* **Naive independence assumption**
* **Gaussian (Normal) distribution** for features

It is used when **features are continuous** (real-valued).

---

## 2️⃣ Bayes’ Theorem (Core Formula)

[
P(C \mid X) = \frac{P(X \mid C),P(C)}{P(X)}
]

Where:

* (C) = class
* (X = (x_1, x_2, \dots, x_n)) = feature vector
* (P(C \mid X)) = posterior probability
* (P(C)) = prior probability
* (P(X \mid C)) = likelihood

---

## 3️⃣ Naive Independence Assumption

Gaussian Naive Bayes assumes:

[
P(X \mid C) = \prod_{i=1}^{n} P(x_i \mid C)
]

👉 Features are **conditionally independent** given the class
(This is the “naive” part)

---

## 4️⃣ Why “Gaussian”?

Each feature (x_i) is assumed to follow a **normal distribution** within each class:

[
P(x_i \mid C) = \frac{1}{\sqrt{2\pi\sigma_{C,i}^2}}
\exp\left(-\frac{(x_i - \mu_{C,i})^2}{2\sigma_{C,i}^2}\right)
]

Where:

* (\mu_{C,i}) = mean of feature (i) for class (C)
* (\sigma_{C,i}^2) = variance of feature (i) for class (C)

---

## 5️⃣ How Gaussian Naive Bayes Works (Steps)

### **Training Phase**

For each class (C):

1. Compute **prior probability** (P(C))
2. Compute **mean** (\mu_{C,i}) for each feature
3. Compute **variance** (\sigma_{C,i}^2) for each feature

---

### **Prediction Phase**

For a new data point (X):

1. Compute (P(X \mid C)) using Gaussian formula
2. Compute posterior:
   [
   P(C \mid X) \propto P(C)\prod_i P(x_i \mid C)
   ]
3. Choose class with **maximum posterior probability**

[
\hat{C} = \arg\max_C P(C \mid X)
]

---

## 6️⃣ Simple Example

Suppose:

* Class: **Pass / Fail**
* Feature: **Exam score**

If scores in **Pass** class follow:
[
\mu = 75, \quad \sigma = 5
]

For a student with score **80**, compute:
[
P(80 \mid Pass)
]

Do the same for **Fail**, then choose the class with higher probability.

---

## 7️⃣ Advantages

✅ Very fast and scalable
✅ Works well with small datasets
✅ Handles continuous data easily
✅ Performs surprisingly well even if independence assumption is violated

---

## 8️⃣ Disadvantages

❌ Assumes features are independent
❌ Assumes Gaussian distribution (may not fit all data)
❌ Poor performance if data is highly non-normal

---

## 9️⃣ Where It Is Used

* Text classification (with continuous embeddings)
* Medical diagnosis
* Spam detection
* Real-time classification

---

## 🔟 Exam-Ready One-Line Definition

📝 **Gaussian Naive Bayes is a probabilistic classifier that applies Bayes’ theorem with a naive independence assumption and models continuous features using a Gaussian distribution.**

---

## 🔁 Common Exam Traps

❓ *Does Gaussian Naive Bayes output probabilities or labels?*
✔ Both (probabilities, then label via argmax)

❓ *Is Gaussian Naive Bayes a generative or discriminative model?*
✔ **Generative**




```

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Sample dataset
X = np.array([
    [5.1, 3.5],
    [4.9, 3.0],
    [6.2, 3.4],
    [5.9, 3.0]
])

y = np.array([0, 0, 1, 1])  # class labels

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Model
model = GaussianNB()

# Training
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))


```