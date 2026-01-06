

## 🔹 Normalization vs Standardization

Both are **feature scaling techniques**, but they do **different things**.

---

## 📌 1. Normalization (Min–Max Scaling)

### What it does

Scales data to a **fixed range**, usually **0 to 1**.

### Formula

[
X_{new} = \frac{X - X_{min}}{X_{max} - X_{min}}
]

### Python

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_norm = scaler.fit_transform(X)
```

### Example

Original values:

```
Age: 10, 20, 30
```

After normalization:

```
0.0, 0.5, 1.0
```

### When to use Normalization

✅ KNN
✅ Neural Networks
✅ Distance-based algorithms
✅ When data has **known min/max limits**
❌ Sensitive to **outliers**

---

## 📌 2. Standardization (Z-score Scaling)

### What it does

Centers data around **mean = 0** and **std = 1**.

### Formula

[
X_{new} = \frac{X - \mu}{\sigma}
]

### Python

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_std = scaler.fit_transform(X)
```

### Example

Original values:

```
10, 20, 30
```

After standardization:

```
-1.22, 0.0, 1.22
```

### When to use Standardization

✅ SVM
✅ Logistic Regression
✅ Perceptron
✅ PCA
✅ Gradient Descent–based models
✔️ More robust to outliers than normalization

---

## ⚖️ Key Differences (Quick Table)

| Feature               | Normalization  | Standardization        |
| --------------------- | -------------- | ---------------------- |
| Range                 | 0 → 1          | -∞ → +∞                |
| Mean                  | Not fixed      | 0                      |
| Std Dev               | Not fixed      | 1                      |
| Sensitive to outliers | Yes            | Less                   |
| Use case              | Distance-based | Gradient / statistical |

---

## 🧠 How to choose? (Golden Rule)

* **Distance-based models** → Normalization
* **Gradient / statistical models** → Standardization
* **Tree-based models** → No scaling needed

---

## ❗ Important Note

Never fit the scaler on **test data**:

```python
scaler.fit(X_train)
X_test_scaled = scaler.transform(X_test)
```

---

If you want, I can:

* Add **visual intuition**
* Explain **with graphs**
* Tell you **which one to use in exams vs real projects**
