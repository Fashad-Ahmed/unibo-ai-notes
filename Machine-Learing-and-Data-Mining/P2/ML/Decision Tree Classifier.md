
# Decision Tree Classifier

## 1. What is a Decision Tree Classifier?

A **Decision Tree Classifier** is a **supervised learning algorithm** used for **classification tasks**.
It works by **recursively splitting the data** based on feature values to form a tree-like structure that makes decisions.

Think of it as a flowchart:

> *If condition → then decision → else another condition → final class*

---

## 2. Structure of a Decision Tree

### Components

* **Root Node** – first split
* **Internal Nodes** – decision rules
* **Leaf Nodes** – final class labels
* **Branches** – outcomes of decisions

Example:

```
          Age <= 30
         /          \
     Yes              No
   Income <= 50k    Student?
    /      \        /      \
  No       Yes    Yes       No
```

---

## 3. How Decision Trees Work (Step-by-Step)

1. Start with the full dataset
2. Try all possible splits for each feature
3. Choose the split that best **separates the classes**
4. Split the dataset
5. Repeat recursively for each child node
6. Stop when a stopping condition is met

---

## 4. Splitting Criteria (Impurity Measures)

The “best split” is chosen by **reducing impurity**.

---

### 4.1 Gini Impurity (Most common)

[
\text{Gini} = 1 - \sum_{i=1}^{c} p_i^2
]

* (p_i): probability of class (i)
* **0** = pure node

Example:

* 50% Yes, 50% No → Gini = 0.5
* 100% Yes → Gini = 0

---

### 4.2 Entropy (Information Gain)

[
\text{Entropy} = -\sum_{i=1}^{c} p_i \log_2(p_i)
]

Information Gain:
[
IG = Entropy(parent) - \sum w_i \cdot Entropy(child_i)
]

Lower entropy → better split

---

### 4.3 Gini vs Entropy

| Gini               | Entropy          |
| ------------------ | ---------------- |
| Faster             | Slower           |
| Default in sklearn | More theoretical |
| Similar results    | Similar results  |

---

## 5. Handling Different Feature Types

### Numerical Features

* Try thresholds: `Age <= 25`, `Age <= 30`
* Sorted values used to find optimal splits

### Categorical Features

* One-vs-rest splits
* Often one-hot encoded in practice (sklearn)

---

## 6. Stopping Criteria

Tree growth stops when:

* All samples belong to one class
* Max depth reached
* Minimum samples per node reached
* No split improves impurity

---

## 7. Prediction Process

For a new data point:

1. Start at root
2. Follow decision rules
3. Reach leaf node
4. Predict **majority class** in that leaf

---

## 8. Overfitting in Decision Trees ⚠️

### Why it happens

* Trees can memorize training data
* Deep trees = low bias, high variance

### Prevention (Pruning)

#### Pre-pruning (Early stopping)

* `max_depth`
* `min_samples_split`
* `min_samples_leaf`
* `max_features`

#### Post-pruning

* Cost Complexity Pruning (α pruning)

---

## 9. Hyperparameters (sklearn)

| Parameter         | Purpose              |
| ----------------- | -------------------- |
| max_depth         | Limits tree depth    |
| min_samples_split | Min samples to split |
| min_samples_leaf  | Min samples in leaf  |
| criterion         | gini / entropy       |
| max_features      | Features per split   |

---

## 10. Advantages

✅ Easy to understand & visualize
✅ No feature scaling required
✅ Handles non-linear relationships
✅ Works with mixed data types

---

## 11. Disadvantages

❌ Prone to overfitting
❌ Unstable (small data change → big tree)
❌ Lower accuracy than ensembles

---

## 12. Decision Tree vs Other Models

| Model               | Comparison                  |
| ------------------- | --------------------------- |
| Logistic Regression | Trees capture non-linearity |
| KNN                 | Trees faster at prediction  |
| Random Forest       | Forest reduces overfitting  |
| XGBoost             | Boosting improves accuracy  |

---

## 13. Practical Example (sklearn)

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    criterion="gini",
    max_depth=3,
    min_samples_leaf=5
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

---

## 14. When to Use Decision Trees

✔ Need interpretability
✔ Non-linear patterns
✔ Mixed feature types
✔ Baseline model

---

## 15. Key Interview Points

* Gini vs Entropy
* Overfitting & pruning
* Bias–variance tradeoff
* Feature importance
* Why trees don’t need scaling

---

## Final Summary

* Decision Trees split data using impurity reduction
* Simple but powerful
* Overfitting is main challenge
* Foundation for Random Forest & Boosting

