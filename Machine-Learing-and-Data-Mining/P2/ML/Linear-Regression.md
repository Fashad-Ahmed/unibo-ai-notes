## Univariate Regression

**Univariate regression** is a regression model with **one independent (predictor) variable** and **one dependent (response) variable**.
The most common form is **univariate linear regression**.

---

## 1. Model definition

Let:

* ( x ) = independent variable
* ( y ) = dependent variable

### Linear univariate regression model:

[
y = \beta_0 + \beta_1 x + \varepsilon
]

Where:

* ( \beta_0 ) = intercept
* ( \beta_1 ) = slope (effect of (x) on (y))
* ( \varepsilon ) = random error term

---

## 2. Interpretation of parameters

* **Intercept ((\beta_0))**
  Value of (y) when (x = 0)

* **Slope ((\beta_1))**
  Expected change in (y) for a **one-unit increase in (x)**

Example:

> If ( \beta_1 = 2.5 ), then increasing (x) by 1 increases (y) by 2.5 (on average).

---

## 3. Estimation (Ordinary Least Squares)

The parameters are estimated by minimizing the **sum of squared errors**:

[
\min_{\beta_0, \beta_1} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
]

### Closed-form solutions:

[
\beta_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}
]

[
\beta_0 = \bar{y} - \beta_1 \bar{x}
]

---

## 4. Assumptions

1. Linearity: relationship between (x) and (y) is linear
2. Independence of errors
3. Homoscedasticity (constant variance)
4. Normality of errors (for inference)

---

## 5. Statistical significance

### Hypothesis test for slope:

[
H_0: \beta_1 = 0 \quad \text{vs} \quad H_1: \beta_1 \neq 0
]

* If **p-value < 0.05**, (x) has a statistically significant effect on (y)

---

## 6. Goodness of fit

### Coefficient of determination:

[
R^2 = 1 - \frac{SS_{res}}{SS_{tot}}
]

* Measures proportion of variance in (y) explained by (x)
* (0 \le R^2 \le 1)

---

## 7. Example (numerical)

Suppose:
[
\hat{y} = 3 + 2x
]

If ( x = 4 ):
[
\hat{y} = 3 + 2(4) = 11
]

---

## 8. Python example

```python
import numpy as np
from sklearn.linear_model import LinearRegression

# Data
X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
y = np.array([2, 4, 5, 4, 6])

# Model
model = LinearRegression()
model.fit(X, y)

print("Intercept:", model.intercept_)
print("Slope:", model.coef_[0])
print("R^2:", model.score(X, y))
```

---

## 9. Univariate vs multivariate regression

| Type                               | Predictors |
| ---------------------------------- | ---------- |
| Univariate                         | 1          |
| Multivariate (multiple regression) | ≥ 2        |

---

## 10. One-line exam definition

> **Univariate regression models the relationship between one independent variable and one dependent variable using a linear equation.**

---

Below is a **conceptual explanation tied directly to the graphs you see**, followed by **confidence intervals**, and then a **clear comparison of univariate vs polynomial regression**.

---

# 1. Graphical Interpretation of Univariate Regression

### What the first graph shows (Univariate Linear Regression)

* **Dots** → observed data points ((x_i, y_i))
* **Straight line** → fitted regression line
  [
  \hat{y} = \beta_0 + \beta_1 x
  ]

### How to interpret it visually:

* The **slope** shows the *direction and strength* of the relationship
* The **distance of points from the line** represents the error (residuals)
* A good fit → points cluster closely around the line
* A poor fit → points are widely scattered

📌 Each vertical distance:
[
\text{Residual}_i = y_i - \hat{y}_i
]

---

# 2. Confidence Intervals in Univariate Regression

A **confidence interval (CI)** gives a range of plausible values for a parameter or prediction.

---

## 2.1 Confidence interval for the slope ( \beta_1 )

[
\beta_1 \pm t_{\alpha/2,, n-2} \cdot SE(\beta_1)
]

### Interpretation:

> We are 95% confident that the true slope lies within this interval.

Example:
[
\beta_1 = 2.1 \quad \text{CI: } [1.4,; 2.8]
]

✅ Since 0 is **not** in the interval → slope is statistically significant

---

## 2.2 Confidence interval for the mean response

At a given (x_0):

[
\hat{y}(x_0) \pm t \cdot SE_{\text{mean}}(x_0)
]

* Narrower than prediction intervals
* Tells uncertainty in the **estimated mean**

---

## 2.3 Prediction interval (important distinction)

[
\hat{y}(x_0) \pm t \cdot SE_{\text{prediction}}(x_0)
]

* Wider than confidence intervals
* Accounts for **noise + model uncertainty**
* Used to predict **individual outcomes**

---

### CI vs PI (visual intuition)

| Interval            | What it means                    |
| ------------------- | -------------------------------- |
| Confidence Interval | Uncertainty in the mean          |
| Prediction Interval | Uncertainty in a new observation |

---

# 3. Polynomial Regression (Graphical Interpretation)

### What the second graph shows

Polynomial regression extends univariate regression by adding powers of (x):

[
y = \beta_0 + \beta_1 x + \beta_2 x^2 + \beta_3 x^3 + \varepsilon
]

### Visual meaning:

* The curve can **bend**
* Captures **non-linear patterns**
* Still univariate (only one predictor)

📌 Polynomial regression is **linear in parameters**, not in shape.

---

# 4. Univariate vs Polynomial Regression (Comparison)

| Aspect               | Univariate Linear       | Polynomial                                    |
| -------------------- | ----------------------- | --------------------------------------------- |
| Number of predictors | 1                       | 1                                             |
| Relationship         | Linear                  | Non-linear                                    |
| Equation             | ( \beta_0 + \beta_1 x ) | ( \beta_0 + \beta_1 x + \beta_2 x^2 + \dots ) |
| Interpretability     | Very high               | Lower                                         |
| Risk of overfitting  | Low                     | Higher (degree ↑)                             |
| Extrapolation        | Stable                  | Dangerous                                     |
| Use case             | Simple trends           | Curved patterns                               |

---

## Key insight (exam favorite)

> **Polynomial regression is still univariate regression because it uses only one independent variable.**

---

# 5. When to use which?

### Use univariate linear regression when:

* Relationship is approximately linear
* Interpretability matters
* Small dataset

### Use polynomial regression when:

* Clear curvature in data
* You validate degree using cross-validation
* Prediction accuracy > interpretability

---

# 6. One-line exam answers

* **Graphical interpretation:**
  *Univariate regression fits a straight line minimizing squared vertical distances from data points.*

* **Confidence interval:**
  *A range of values that likely contains the true model parameter with a specified confidence level.*

* **Comparison:**
  *Polynomial regression models non-linear relationships using powers of a single predictor, while univariate linear regression assumes linearity.*


