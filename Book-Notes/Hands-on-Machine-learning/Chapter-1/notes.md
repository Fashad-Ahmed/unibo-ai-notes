
# 🤖 Machine Learning Foundational Concepts


## 1. How would you define Machine Learning?

Machine Learning is the **science (and art) of programming computers so they can learn from data** without being explicitly programmed. It enables systems to improve their performance on a specific task through experience (data).

## 2. Can you name four types of problems where it shines?

ML shines in problems that are:
1.  Require **too much fine-tuning** or long lists of rules (e.g., spam detection).
2.  Have **no good solution** using traditional approaches (e.g., speech recognition).
3.  Need to adapt to **fluctuating environments** (e.g., forecasting stock prices).
4.  Need to help humans **gain insights** from large amounts of data (e.g., data mining).

## 3. What is a labeled training set?

A labeled training set is a dataset used to train a supervised learning algorithm, where each **instance (sample)** in the set is accompanied by the **desired solution** (called a **label**).

## 4. What are the two most common supervised tasks?

1.  **Classification**: Predicting the category/class of an instance (e.g., classifying emails as spam or not spam).
2.  **Regression**: Predicting a target *numerical value* (e.g., predicting house prices).

## 5. Can you name four common unsupervised tasks?

1.  **Clustering**: Grouping similar instances (e.g., customer segmentation).
2.  **Visualization and Dimensionality Reduction**: Simplifying data without losing too much information (e.g., PCA, t-SNE).
3.  **Association Rule Learning**: Discovering relationships between items (e.g., people who buy *X* also tend to buy *Y*).
4.  **Anomaly/Novelty Detection**: Identifying unusual instances (e.g., detecting fraudulent transactions).

---

## 6. What type of Machine Learning algorithm would you use to allow a robot to walk in various unknown terrains?

**Reinforcement Learning (RL)**.
* The robot (**agent**) observes the environment and selects **actions** to maximize a **reward** over time. This is ideal for tasks where the best actions aren't predetermined.

## 7. What type of algorithm would you use to segment your customers into multiple groups?

An **Unsupervised Learning** algorithm, specifically **Clustering** (e.g., $k$-Means, DBSCAN).

## 8. Would you frame the problem of spam detection as a supervised learning problem or an unsupervised learning problem?

**Supervised Learning**.
* The task is **Classification**, where the model is trained on many example emails that have been **labeled** as either *spam* (positive class) or *not spam* (negative class).

---

## 9. What is an online learning system?

An online learning system trains the model **incrementally** by feeding it data instances sequentially, either individually or in small groups (**mini-batches**).
* It's used for systems that receive a continuous flow of data and for training on datasets that are too large to fit into the computer's main memory (**out-of-core learning**).

## 10. What is out-of-core learning?

Out-of-core learning refers to training a machine learning system on **datasets that cannot fit into a computer's main memory (RAM)**.
* It is performed using **online learning** techniques, where the data is loaded in small chunks (mini-batches) to train the model incrementally.

## 11. What type of learning algorithm relies on a similarity measure to make predictions?

**Instance-Based Learning** algorithms (e.g., $k$-Nearest Neighbors, Locally Weighted Regression).
* Instead of explicitly training a model, they learn by **memorizing the training examples** and comparing new instances to the stored examples using a **similarity measure** (like Euclidean distance).

## 12. What is the difference between a model parameter and a learning algorithm’s hyperparameter?

| Feature | Model Parameter | Hyperparameter |
| :--- | :--- | :--- |
| **Definition** | A value the model learns **from the data** (e.g., weights/biases in a Neural Network). | A value that is **set prior to the training process** (e.g., learning rate, regularization strength, $k$ in $k$-NN). |
| **Optimization** | Optimized by the **learning algorithm** during training. | Optimized by the **ML engineer** (often via techniques like grid search or random search). |

## 13. What do model-based learning algorithms search for? What is the most common strategy they use to succeed? How do they make predictions?

* **Search for**: An **optimal set of model parameters** that makes the model generalize best to new data.
* **Common Strategy**: **Minimizing a Cost Function** (or **Loss Function**) during training.
* **Predictions**: Once trained, they use the **learned parameter values** in their predictive function ($\hat{y} = h(\mathbf{x}, \boldsymbol{\theta})$) to make predictions on new data.

---

## 14. Can you name four of the main challenges in Machine Learning?

1.  **Insufficient Quantity of Training Data**: Models often require a large amount of data to generalize well.
2.  **Nonrepresentative Training Data**: The training set does not accurately reflect the instances that will be encountered in production.
3.  **Poor-Quality Data**: Data is noisy, contains errors, or has too many outliers.
4.  **Irrelevant Features (Feature Engineering)**: The input features are not informative enough for the task.
5.  **Overfitting the Training Data** (high variance).
6.  **Underfitting the Training Data** (high bias).

## 15. If your model performs great on the training data but generalizes poorly to new instances, what is happening? Can you name three possible solutions?

* **What is happening?**: The model is **overfitting** the training data. This means the model is too complex and has learned the noise/specific details of the training set rather than the underlying pattern.

* **Three possible solutions**:
    1.  **Simplify the model**: Use a simpler model, reduce the number of features, or constrain the model (e.g., regularization).
    2.  **Gather more training data**: More data can help smooth out the irrelevant patterns learned from the smaller set.
    3.  **Reduce the noise in the training data**: Fix data errors and remove outliers.

---

## 16. What is a test set, and why would you want to use it?

* **Test Set**: A set of data instances that the model **has not seen during training**.
* **Purpose**: To get an **unbiased estimate of the model's generalization error** (how well the model performs on new, unseen data). You should use it only *after* you have selected your final model and tuned its hyperparameters.

## 17. What is the purpose of a validation set?

* **Validation Set**: A subset of the training data (separate from the test set) used to **evaluate different models** and **tune hyperparameters**.
* **Purpose**: To estimate the generalization error *before* the test set is used, allowing you to compare models and select the best hyperparameters **without contaminating the test set**.

## 18. What is the train-dev set, when do you need it, and how do you use it?

* **Train-dev set**: A term mostly used in deep learning, specifically when dealing with a **data mismatch** between the training data and the data used for validation/testing.
* **When you need it**: When your training data (e.g., scraped web images) comes from a **different distribution** than your validation/test data (e.g., user-uploaded app images).
* **How to use it**: It is a subset of the **training data distribution** that you use for validation. If the model performs well on the train-dev set but poorly on the validation set (which has the target distribution), the issue is likely **data mismatch**, not overfitting or underfitting.

## 19. What can go wrong if you tune hyperparameters using the test set?

If you tune hyperparameters using the test set, the resulting generalization error estimate will be **optimistic (biased)**.

* The model will be specifically optimized for the patterns (and noise) in the test set, meaning its performance on truly **new** unseen data in a production environment will likely be **worse** than what the test score suggests. This defeats the purpose of the test set, which is to provide an unbiased final evaluation.


