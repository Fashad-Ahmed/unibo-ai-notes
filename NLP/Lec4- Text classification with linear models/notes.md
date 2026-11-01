# Text Classification with Linear Models

---

## Table of Contents
1. [Text Classification Overview](#1-text-classification-overview)
2. [Approaches to Classification](#2-approaches-to-classification)
3. [Multinomial Naive Bayes Classifiers](#3-multinomial-naive-bayes-classifiers)
4. [Logistic Regression](#4-logistic-regression)
5. [Evaluation Methods](#5-evaluation-methods)
6. [Lexicons for Sentiment, Affect, and Connotation](#6-lexicons-for-sentiment-affect-and-connotation)

---

## 1. Text Classification Overview

### What is Text Classification?
* **Definition:** Text classification (or text categorization) is the task of assigning a predefined category or label to an entire text document or text segment[cite: 5].
* **Sentiment Analysis:** A prominent text classification application focused on detecting attitudes—defined as enduring, affectively colored beliefs and dispositions toward objects, persons, or events[cite: 5]. Sentiment models identify the holder (source), the target (aspect), and the type/polarity of the attitude (positive, negative, neutral, alongside its strength)[cite: 5].
* **Applications:** Commercial brand tracking, policy-making public opinion analysis, election or market trend prediction, spam detection, language identification, authorship attribution, subject category classification, and toxic language/hate speech detection[cite: 6, 9]. In fact, foundational NLP tasks like part-of-speech tagging and sentence boundary disambiguation can be framed as classification[cite: 9].

---

## 2. Approaches to Classification

Classification tasks take an input document $x$ from a fixed set of output classes $Y = \{y_1, \dots, y_M\}$ and return a predicted class label $\hat{y} \in Y$[cite: 10]. Three primary paradigms exist:
1. **Rule-Based Classifiers:** Uses handcrafted rules, whitelists/blacklists, or regular expressions (e.g., flagging emails containing specific financial terms). They can be highly accurate when engineered by experts, but they are expensive to build and maintain[cite: 11].
2. **In-Context Learning:** Employs a decoder LLM guided by natural language prompts describing the task and classes, operating in a zero-shot or few-shot manner[cite: 11].
3. **Supervised Machine Learning:** Leverages a training set of $N$ labeled documents $\{(d_i, c_i)\}$ to train statistical models[cite: 11]. These split into two main families:
   * **Generative Approaches:** Model how a class generates data and compare test observations against class profiles (e.g., Naive Bayes)[cite: 12].
   * **Discriminative Approaches:** Directly learn decision boundaries or feature utility weights without modeling the underlying data generation process (e.g., Logistic Regression)[cite: 12].

---

## 3. Multinomial Naive Bayes Classifiers

### The Bag-of-Words Assumption
* Multinomial Naive Bayes ignores word order and document length variations, representing a text document purely as an unordered "bag of words" keeping track of individual word frequencies[cite: 13].

### Mathematical Formulation
* Naive Bayes is a probabilistic classifier that selects the class $\hat{c}$ maximizing the posterior probability using Bayes' Rule[cite: 14]:
  $$\hat{c} = \arg\max_{c \in C} P(c\vert{}d) = \arg\max_{c \in C} \frac{P(d\vert{}c)P(c)}{P(d)} = \arg\max_{c \in C} P(d\vert{}c)P(c)$$
[cite: 14]
* Representing the document via features (words $w_i$) and applying the **Naive Bayes independence assumption** (assuming features are conditionally independent given the class), the equation simplifies to[cite: 14]:
  $$\hat{c}_{\text{NB}} = \arg\max_{c \in C} P(c) \prod_{i} P(w_i \vert{} c)$$
[cite: 14]
* To prevent underflow errors from multiplying many small probabilities, calculations are performed in **log-space**[cite: 15]:
  $$\hat{c}_{\text{NB}} = \arg\max_{c \in C} \log P(c) + \sum_{i} \log P(w_i \vert{} c)$$
[cite: 15]

### Parameter Estimation & Smoothing
* Maximum Likelihood Estimates (MLE) for priors and likelihoods are derived from corpus frequencies[cite: 15]:
  $$\hat{P}(c) = \frac{N_c}{N_{\text{doc}}}, \quad \hat{P}(w_i \vert{} c) = \frac{\text{Count}(w_i, c)}{\sum_{v \in V} \text{Count}(v, c)}$$
[cite: 15]
* **Laplace (Add-1) Smoothing:** Essential in Naive Bayes to handle zero-count or out-of-vocabulary words that would otherwise nullify the entire product[cite: 16]:
  $$\hat{P}_{\text{Laplace}}(w_i \vert{} c) = \frac{\text{Count}(w_i, c) + 1}{\left(\sum_{v \in V} \text{Count}(v, c)\right) + \vert{}V\vert{}}$$
[cite: 16]

### Properties of Naive Bayes
* Extremely fast, requires low storage, and is robust to irrelevant features[cite: 18].
* Suffers from an overly strong independence assumption (overestimating evidence from correlated features), but serves as an exceptional baseline—especially for short documents or small datasets[cite: 18].

---

## 4. Logistic Regression

### Core Architecture
* Unlike Naive Bayes, **Logistic Regression** is a discriminative model that directly computes the conditional probability $P(y\vert{}x)$ without modeling how data is generated[cite: 20].
* **Logit ($z$):** Computes the weighted linear sum of evidence plus a bias term[cite: 21]:
  $$z = \left(\sum_{i=1}^{n} w_i x_i\right) + b = w \cdot x + b$$
[cite: 21]
* **Logistic (Sigmoid) Function:** Forces the linear output into a valid probability range between $0$ and $1$[cite: 21]:
  $$P(y = 1) = \sigma(z) = \frac{1}{1 + e^{-z}} = \frac{1}{1 + e^{-(w \cdot x + b)}}$$
[cite: 21]

### Feature Engineering
* Text classification via logistic regression relies on custom feature vectors (e.g., counts of positive/negative sentiment lexicon words, presence of negation like "no", first/second-person pronouns, exclamation marks, or log-transformed word counts)[cite: 22]. Features require scaling (such as z-score standardization or log transformation) to ensure compatible ranges[cite: 24].

### Optimization and Loss
* **Cross-Entropy Loss:** Measures the divergence between system predictions ($\hat{y}$) and gold labels ($y$)[cite: 25]:
  $$L_{\text{CE}}(\hat{y}, y) = -\log p(y\vert{}x) = -[y \log \hat{y} + (1 - y)\log(1 - \hat{y})]$$
[cite: 25]
* **Training:** Uses **Stochastic Gradient Descent (SGD)** with mini-batches to minimize loss on a convex objective function[cite: 26].
* **Regularization:** Employs **$L_2$ regularization** (Ridge regression, penalizing squared weights $\Vert{}\theta\Vert{}_2^2$) or **$L_1$ regularization** (Lasso regression, penalizing absolute weights $\Vert{}\theta\Vert{}_1$) to prevent overfitting[cite: 26].

### Multinomial Logistic Regression (Softmax Regression)
* Extends binary logistic regression to handle $K > 2$ classes using a weight matrix $W$ of shape $[K \times f]$ and the **softmax** activation function to normalize outputs into multi-class probability distributions[cite: 27]. Each row vector in $W$ acts as a prototype for a specific class[cite: 27].

---

## 5. Evaluation Methods

### Binary Classification Metrics
* Evaluated against gold-standard labels using a confusion matrix capturing **True Positives (TP)**, **False Positives (FP)**, **True Negatives (TN)**, and **False Negatives (FN)**.
  * **Precision:** $\frac{\text{TP}}{\text{TP + FP}}$ (proportion of selected items that are correct)[cite: 30].
  * **Recall:** $\frac{\text{TP}}{\text{TP + FN}}$ (proportion of target items successfully retrieved)[cite: 30].
  * **$F_1$-Score:** The harmonic mean of precision and recall, most commonly used because accuracy fails on unbalanced datasets[cite: 30]:
    $$F_1 = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision + Recall}}$$
[cite: 30]

### Multi-Class Averaging
* **Micro-Averaging:** Pools decisions across all classes into a single confusion matrix before computing metrics; heavily dominated by frequent classes[cite: 32].
* **Macro-Averaging:** Computes metrics independently for each class and averages them uniformly; ideal when all classes carry equal importance[cite: 32].

### Validation and Significance Testing
* **$k$-Fold Cross-Validation:** Partitions data into $k$ disjoint folds, training on $k-1$ folds and testing on the remaining fold iteratively to evaluate models reliably without wasting data[cite: 33].
* **Statistical Significance Testing:** Determines whether performance differences ($\delta(x)$) between two classifiers $A$ and $B$ are statistically meaningful rather than random chance. Standard approaches like the **paired bootstrap test** or approximate randomization compute a $p$-value (rejecting the null hypothesis $H_0$ if $p < 0.05$ or $0.01$)[cite: 34, 35].

---

## 6. Lexicons for Sentiment, Affect, and Connotation

### Affective Typologies
Affect encompasses diverse psychological states categorized by Scherer (2000): **Emotions** (brief intense responses), **Moods** (diffuse long-duration states), **Interpersonal Stances** (affective posture toward others), **Attitudes** (enduring beliefs/preferences), and **Personality Traits**[cite: 37]. 

### Emotion Theories
1. **Basic Emotion Models:** Views emotions as discrete atomic units. Ekman's 6 basic emotions include *anger, disgust, fear, happiness, sadness, and surprise*[cite: 39]. Plutchik’s wheel of emotion defines 8 basic emotions structured in four opposing pairs (*joy–sadness, anger–fear, trust–disgust, anticipation–surprise*)[cite: 39].
2. **Dimensional Models (VAD Space):** Represents emotion continuously across 2 or 3 axes: **Valence** (pleasantness), **Arousal** (intensity), and **Dominance** (control)[cite: 39, 40].

### Standard Affective Lexicons
* **Sentiment Lexicons:** General polarity lists like Hu and Liu's Opinion Lexicon or MPQA list positive and negative words[cite: 40].
* **NRC VAD Lexicon:** Assigns real-valued valence, arousal, and dominance scores to 20,000 words[cite: 40].
* **NRC Word-Emotion Association Lexicon (EmoLex):** Maps ~14,000 words to Plutchik’s 8 basic emotions and binary sentiment categories[cite: 41, 42].
* **NRC Emotion/Affect Intensity Lexicon:** Provides real-valued association intensities for specific emotions like anger, fear, joy, and sadness across 5,814 words[cite: 42, 43].
* **LIWC (Linguistic Inquiry and Word Count):** Contains over 2,300 words organized into 73 lexicons capturing social psychological dimensions, cognitive mechanisms, and emotional categories[cite: 43].

### Lexicon Induction Methods
Lexicons are constructed using expert annotators, crowdsourcing (e.g., Mechanical Turk via synonym selection and rating tasks), semi-supervised propagation from seed word lists, or supervised induction exploiting online review ratings[cite: 44].