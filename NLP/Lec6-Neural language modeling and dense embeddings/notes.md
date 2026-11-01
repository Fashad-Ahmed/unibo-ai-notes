# Neural Language Modeling and Dense Embeddings

---

## Table of Contents

1. [From Sparse to Dense Representations](https://www.google.com/search?q=%231-from-sparse-to-dense-representations)
2. [Neural Language Modeling (Feedforward Networks)](https://www.google.com/search?q=%232-neural-language-modeling-feedforward-network)
3. [Word2Vec Models & Skip-gram Architecture](https://www.google.com/search?q=%233-word2vec-models--skip-gram-architecture)
4. [Evaluating Embeddings](https://www.google.com/search?q=%234-evaluating-embeddings)
5. [Properties and Geometric Meaning of Embeddings](https://www.google.com/search?q=%235-properties-and-geometric-meaning-of-embeddings)
6. [Analyzing Embeddings: Historical Change and Cultural Biases](https://www.google.com/search?q=%236-analyzing-embeddings-historical-change-and-cultural-biases)

---

## 1. From Sparse to Dense Representations

Traditional vector representations like **TF-IDF** and **Positive Pointwise Mutual Information (PPMI)** create vectors that are:

* **Long:** Dimensionality matches vocabulary size ($\vert{}V\vert{} = 20,000$ to $50,000$)[cite: 69].
* **Sparse:** Most elements in the vector are zeros[cite: 69].

### Why Move to Dense Vectors?

* **Compactness:** Short vectors (length $50$ to $1,000$) have fewer parameters/weights to tune when integrated into machine learning models[cite: 69, 70].
* **Generalization:** Dense vectors capture latent semantic information across dimensions rather than storing exact, isolated token counts[cite: 70].
* **Capturing Synonymy:** In sparse models, orthogonal dimensions mean that synonyms like *car* and *automobile* have zero overlap. Dense embeddings map words with similar contextual neighbors close together in continuous space[cite: 70].
* **Popular Embedding Frameworks:** Word2vec (Mikolov et al., 2013), GloVe (Pennington et al., 2014), and fastText (Mikolov et al., 2017)[cite: 70].

---

## 2. Neural Language Modeling (Feedforward Network)

Statistical n-gram models suffer from the **curse of dimensionality**; if a specific word sequence hasn't been observed during training, its probability defaults to zero[cite: 71]. Neural language models fix this by replacing exact counts with a **smooth predictive function**[cite: 72, 74].

### Feedforward Architecture

A standard multi-layer feedforward neural network computes representations using matrix multiplications and non-linear activation functions[cite: 72, 73]:

* **Input Layer ($x$):** Size $n_0 = n \times d$ (where $n$ is context window size, $d$ is embedding dimension)[cite: 73, 74].
* **Hidden Layer ($h$):** Size $n_1$, computed via[cite: 73]:

$$h = \tanh(Wx + b)$$



where $W$ is the hidden weight matrix and $b$ is the bias vector[cite: 73].
* **Output Layer ($y$):** Size $n_2 = \vert{}V\vert{}$, computed via[cite: 73, 74]:

$$y = \text{softmax}(Uh)$$



where $U$ is the output weight matrix producing a probability distribution over the vocabulary[cite: 73, 74].

```
     y1    y2    ...    yn2   (Output Layer: Softmax over Vocabulary)
      ^     ^            ^
       \    |           /
    [h1,  h2,  h3, ..., hn1]  (Hidden Layer: tanh)
      ^     ^            ^
       \    |           /
    [x1,  x2,  ..., xn0]    (Input Layer: Concatenated Embeddings)

```

### Learning Embeddings via Backpropagation

1. Every word $w \in V$ is mapped to a dense feature vector $e(w) \in \mathbb{R}^d$ stored in an embedding matrix $E \in \mathbb{R}^{d \times \vert{}V\vert{}}$[cite: 74].
2. Input words are represented as **one-hot vectors**[cite: 75]. Multiplying a one-hot vector by matrix $E$ selects out the exact $d$-dimensional embedding row/column[cite: 75].
3. The model is trained using **self-supervision** on massive unlabeled text corpora, minimizing cross-entropy loss via stochastic gradient descent, which updates weights across $E$, $W$, $U$, and $b$ simultaneously[cite: 79].

---

## 3. Word2Vec Models & Skip-gram Architecture

**Word2Vec** simplifies neural language modeling by framing it as a binary classification task rather than full vocabulary sequence prediction, making training significantly faster[cite: 82, 83].

### Core Idea: Skip-gram with Negative Sampling (SGNS)

Instead of predicting the next word using a heavy softmax over all $\vert{}V\vert{}$ words, Word2Vec trains a logistic regression classifier to determine whether a context word $o$ is likely to appear near a center target word $c$[cite: 83, 84, 85].

* **Objective Function (Negative Log-Likelihood with Negative Sampling):**

$$J_{\text{SGNS}}(o, v_c, U) = -\log(\sigma(u_o^\top v_c)) - \sum_{k=1}^{K} log(\sigma(-u_k^\top v_c))$$



[cite: 91]
where $v_c$ is the center word vector, $u_o$ is the actual outside context word vector, and $u_k$ represent $K$ randomly sampled noise (negative) words[cite: 88, 91].
* **Negative Sampling Distribution:** Noise words are sampled using unigram probabilities raised to the power of $\alpha = 3/4$ to slightly boost the selection frequency of rare words[cite: 91]:

$$P_\alpha(w) = \frac{\text{Count}(w)^\alpha}{\sum_w \text{Count}(w)^\alpha}$$



[cite: 91]

### Model Variants

* **CBOW (Continuous Bag of Words):** Predicts the target center word given its surrounding context window words[cite: 86].
* **Skip-gram:** Predicts surrounding context words independently given the target center word[cite: 86].

---

## 4. Evaluating Embeddings

Embeddings can be assessed through different evaluation paradigms:

* **Intrinsic Evaluation:**
* **Word Similarity Datasets:** Comparing model cosine similarity scores against human judgments (e.g., *SimLex-999*, *WordSim-353*, *SCWS*)[cite: 94].
* **Analogy Tasks:** Testing linear relationships like semantic or syntactic proportions[cite: 94].


* **Extrinsic Evaluation:** Assessing how well pretrained embeddings boost performance downstream on end-to-end tasks like sentiment analysis, text classification, or machine translation[cite: 94].

---

## 5. Properties and Geometric Meaning of Embeddings

### Window Size and Semantic Granularity

* **Small Windows ($C = \pm 2$):** Capture local syntactic and word-class similarities (e.g., *Hogwarts* clustered with fictional terms like *Sunnydale*)[cite: 96].
* **Large Windows ($C = \pm 5$):** Capture broad topical and thematic associations (e.g., *Hogwarts* clustered with characters like *Dumbledore* or *Malfoy*)[cite: 96].

### First-Order vs. Second-Order Co-occurrence

* **First-Order Co-occurrence (Syntagmatic):** Words that frequently appear near each other in text (e.g., *wrote* and *poem*)[cite: 97].
* **Second-Order Co-occurrence (Paradigmatic):** Words that share similar neighboring words even if they rarely co-occur directly (e.g., *wrote* and *said* share similar contextual footprints)[cite: 97].

### The Parallelogram Model and Analogies

Mikolov et al. demonstrated that continuous vector spaces encode relational meaning linearly, allowing vector offset arithmetic to solve analogy tasks[cite: 98, 99]:


$$\text{vector}(\text{king}) - \text{vector}(\text{man}) + \text{vector}(\text{woman}) \approx \text{vector}(\text{queen})$$


[cite: 100]

```
       tree
      /    \
     /      \
    apple -- grape ---- vine   (Parallelogram Vector Offsets)

```

---

## 6. Analyzing Embeddings: Historical Change and Cultural Biases

### Diachronic Word Embeddings (Studying Word History)

By training embeddings on historical book corpora split across different decades (e.g., COHA corpus), researchers can track semantic drift over time[cite: 108, 109]:

* **Semantic Shifts:** *Gay* shifted from meaning "cheerful/frolicsome" to denoting homosexuality; *broadcast* shifted from agricultural seed-casting to electronic signal transmission[cite: 109].
* **Pejoration:** *Awful* shifted from "full of awe" to "terrible/appalling"[cite: 109].

### Encoding Cultural Stereotypes and Biases

Because embeddings are learned from vast human-written corpora, they inherit and amplify historical human biases and representational harms[cite: 112, 121]:

* **Gender Stereotypes:** Word2vec vector projections align occupations along a gender axis (e.g., associating *homemaker*, *nurse* with *she*, and *maestro*, *architect* with *he*)[cite: 111].
* **Ethnic Biases:** Word-Embedding Association Tests (WEAT) mirror human Implicit Association Tests (IAT), showing that ethnic minority names exhibit higher cosine association with unpleasant descriptive attributes[cite: 112, 113].
* **Quantifying Historical Trends:** Historical embeddings correlate accurately with societal shifts over the 20th century, mirroring changes in female workforce participation rates within specific professions and evolving ethnic portrayals in literature[cite: 114, 118].

---