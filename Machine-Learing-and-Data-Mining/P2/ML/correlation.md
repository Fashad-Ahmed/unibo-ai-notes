**Correlation in Machine Learning (ML)** measures the **strength and direction of a relationship between variables**. It’s mainly used in **EDA (Exploratory Data Analysis)** and **feature selection**, not as a learning algorithm itself.

---

## 1. What is Correlation?

Correlation tells us:

* **How strongly** two variables move together
* **In which direction** they move

Correlation values range from **–1 to +1**:

| Value | Meaning                      |
| ----- | ---------------------------- |
| +1    | Perfect positive correlation |
| 0     | No linear correlation        |
| –1    | Perfect negative correlation |

---

## 2. Types of Correlation in ML

### 1️⃣ Pearson Correlation

* Measures **linear relationship**
* Assumes **continuous, normally distributed data**

Formula:
[
r = \frac{\text{cov}(X,Y)}{\sigma_X \sigma_Y}
]

**Use when**: linear models, regression analysis

---

### 2️⃣ Spearman Rank Correlation

* Measures **monotonic relationship**
* Uses **ranked values**
* Works well for **ordinal data**

**Use when**: non-linear but monotonic relationships

---

### 3️⃣ Kendall’s Tau

* Measures **rank correlation**
* More robust for small datasets

---

## 3. Correlation vs Causation ⚠️

> Correlation **does not imply causation**

Example:

* Ice cream sales and drowning incidents are correlated
* Hot weather is the real cause

---

## 4. Why Correlation Matters in ML

### 1️⃣ Feature Selection

* Highly correlated features → **multicollinearity**
* Can hurt **linear & logistic regression**

### 2️⃣ Model Stability

* Redundant features add noise
* Makes coefficients unstable

### 3️⃣ Dimensionality Reduction

* Remove one feature from highly correlated pairs

---

## 5. Correlation & Different Models

| Model Type          | Effect of Correlation  |
| ------------------- | ---------------------- |
| Linear Regression   | ❌ Problematic          |
| Logistic Regression | ❌ Problematic          |
| KNN                 | ⚠️ Distance distortion |
| Decision Trees      | ✅ Mostly OK            |
| Random Forest       | ✅ OK                   |
| XGBoost             | ✅ OK                   |

---

## 6. Correlation in Feature Engineering

Common rules:

* |correlation| > **0.8** → consider removing one feature
* Use **domain knowledge**, not just numbers

---

## 7. Visualizing Correlation

* **Heatmap**
* **Scatter plots**
* **Pair plots**

---

## 8. Correlation for Target Variable

* Feature–target correlation helps identify **important predictors**
* Low correlation ≠ useless (non-linear relationships)

---

## 9. Limitations

❌ Only captures **linear** relationships
❌ Sensitive to **outliers**
❌ Doesn’t handle categorical data directly

Below are **practical Python examples** showing how correlation is used in **machine learning workflows**.

---

## 1. Create Sample Data

```python
import pandas as pd
import numpy as np

np.random.seed(0)

data = pd.DataFrame({
    "Hours_Studied": [1, 2, 3, 4, 5],
    "Exam_Score": [50, 55, 65, 70, 75],
    "Sleep_Hours": [8, 7, 6, 6, 5]
})

print(data)
```

---

## 2. Pearson Correlation (Default)

Measures **linear correlation**.

```python
corr_matrix = data.corr()
print(corr_matrix)
```

**Output (approx.)**

```
               Hours_Studied  Exam_Score  Sleep_Hours
Hours_Studied        1.00        0.99        -0.94
Exam_Score           0.99        1.00        -0.96
Sleep_Hours         -0.94       -0.96         1.00
```

---

## 3. Spearman Correlation (Ordinal / Monotonic)

```python
spearman_corr = data.corr(method="spearman")
print(spearman_corr)
```

Use this when:

* Data is **ordinal**
* Relationship is **non-linear but monotonic**

---

## 4. Kendall Correlation

```python
kendall_corr = data.corr(method="kendall")
print(kendall_corr)
```

Best for:

* Small datasets
* Ranking problems

---

## 5. Feature–Target Correlation

```python
feature_target_corr = data.corr()["Exam_Score"].sort_values(ascending=False)
print(feature_target_corr)
```

Helps identify **strong predictors**.

---

## 6. Remove Highly Correlated Features

```python
threshold = 0.9

corr_matrix = data.corr().abs()
upper = corr_matrix.where(
    np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
)

to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
print("Drop columns:", to_drop)
```

---

## 7. Visualize Correlation (Heatmap)

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
plt.show()
```

---

## 8. Correlation with Categorical Target

```python
# Encode target before correlation
data["Passed"] = [0, 0, 1, 1, 1]
print(data.corr()["Passed"])
```

---

## 9. Important ML Tips ⚠️

* High correlation ≠ causation
* Low correlation ≠ unimportant (non-linear models!)
* Tree models handle correlation better than linear models

---

## Summary

| Task                | Method   |
| ------------------- | -------- |
| Linear relationship | Pearson  |
| Ordinal data        | Spearman |
| Small datasets      | Kendall  |
| Feature filtering   | Pearson  |

