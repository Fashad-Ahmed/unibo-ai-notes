# N-gram Language Models

## 1. Language Models Overview

### What is a Language Model?
* **Core Goal:** To define the probability of a word given its context: $P(w\vert{}c)$[cite: 5].
* **Applications:** Fundamental in NLP, including spelling correction (via the noisy channel model), speech recognition, augmentative/alternative communication systems, natural language generation, and text classification[cite: 5].
* **Sequence Probability:** Computes the joint probability of an entire sentence or sequence of words: 
  $$P(W) = P(w_1, w_2, w_3, \dots, w_n)$$
[cite: 6]

### The Chain Rule of Probability
Using the chain rule, the joint probability of a word sequence $w_1^n$ can be decomposed into conditional probabilities[cite: 7]:
$$P(w_1^n) = \prod_{i=1}^{n} P(w_i \vert{} w_1^{i-1}) = P(w_1)P(w_2\vert{}w_1)P(w_3\vert{}w_1^2)\dots P(w_n\vert{}w_1^{n-1})$$
[cite: 7]

* **The Sparsity Problem:** Estimating these exact conditional probabilities by simple counting (e.g., $\frac{\text{Count}(\text{history} + \text{word})}{\text{Count}(\text{history})}$) fails because there are too many possible sentences; we will never see enough training data to cover all histories[cite: 8].

### The Markov Assumption
To make probability estimation tractable, we introduce approximations by assuming that only the preceding $k$ words matter (history is limited)[cite: 9]:
$$P(w_i \vert{} w_1^{i-1}) \approx P(w_i \vert{} w_{i-k}^{i-1})$$
[cite: 9]

* **Unigram Model ($k=0$):** History does not matter at all; words are treated as independent[cite: 10]:
  $$P(w_1^n) \approx \prod_{i=1}^{n} P(w_i)$$
[cite: 10, 12]
* **Bigram Model ($k=1$):** Only the single immediate previous word matters[cite: 13]:
  $$P(w_1^n) \approx \prod_{i=1}^{n} P(w_i \vert{} w_{i-1})$$
[cite: 13]
* **Higher-Order Models:** Trigrams, 4-grams, and 5-grams capture more local context, though they still struggle with long-range dependencies[cite: 14].

---

## 2. Estimating N-gram Probabilities

### Maximum Likelihood Estimation (MLE)
The bigram probability using MLE is calculated by dividing the raw co-occurrence count of the bigram by the unigram count of the history word[cite: 16]:
$$P(w_i \vert{} w_{i-1}) = \frac{\text{Count}(w_{i-1} w_i)}{\text{Count}(w_{i-1})}$$
[cite: 16]

### Example (Berkeley Restaurant Project Corpus)
* Given a sample corpus of user queries, bigram counts and probabilities are extracted to compute sentence likelihoods[cite: 17, 18].
* For instance, computing the probability of a sequence like *I want English food*[cite: 19]:
  $$P(\text{I want English food}) = P(i\vert{}\emptyset)P(\text{want}\vert{}i)P(\text{english}\vert{}\text{want})P(\text{food}\vert{}\text{english})P(\emptyset\vert{}\text{food})$$
[cite: 19]
* **Kinds of Knowledge Captured:** N-grams implicitly encode syntactic preferences, semantic frames (e.g., personal assistant domains), and cultural tendencies based on training frequencies[cite: 20].

---

## 3. Evaluating Language Models

### Evaluation Strategy
* Models are trained on a training set and tested on an independent, unseen **test set** (with hyperparameters tuned on a separate **dev set**)[cite: 22].
* A better model assigns a higher probability to the test set[cite: 22].

### Extrinsic vs. Intrinsic Evaluation
1. **Extrinsic (Downstream / In-Vivo) Evaluation:** Placing the language model into an end-to-end task (like a speech recognizer, machine translation system, or spelling corrector) and measuring final task performance accuracy[cite: 23]. This is the most reliable method but is costly and time-consuming[cite: 23].
2. **Intrinsic Evaluation (Perplexity):** Evaluating the model component independently using probability-based metrics[cite: 24].

### Perplexity (PP)
* Defined as the inverse probability of the test set, normalized by the number of words[cite: 26]:
  $$\text{PP}(w_1^N) = P(w_1^N)^{-\frac{1}{N}} = \left( \prod_{i=1}^{N} \frac{1}{P(w_i \vert{} w_{i-1})} \right)^{\frac{1}{N}}$$
[cite: 26]
* **Intuition:** Perplexity can be thought of as the **weighted average branching factor** of the language model (how many plausible next words the model thinks it has to choose from)[cite: 27].
* **Lower Perplexity = Better Model:** Higher-order models (e.g., trigrams) yield lower perplexity than bigrams or unigrams because they provide more predictive information about word sequences[cite: 28].

---

## 4. Generalization, Zeros, and OOV Words

### The Perils of Overfitting & Sparsity
* N-gram models are heavily dependent on the training corpus. If the test corpus differs in genre or style from the training set (e.g., training on the Wall Street Journal vs. testing on Shakespeare), performance drops significantly[cite: 29, 30].
* **The Zero-Probability Problem:** N-grams not observed during training receive an MLE probability of **zero**[cite: 31]. If even a single unseen n-gram appears in the test set, the entire test set probability collapses to zero, and perplexity becomes infinite[cite: 31].

### Out-Of-Vocabulary (OOV) Words
* **Open Vocabulary Systems:** Must handle words outside the training vocabulary.
* **Solution:** Introduce a special pseudo-word token, `<UNK>`, by mapping rare words in training or handling unknown test words through subword tokenizers[cite: 32]. 
* *Note:* Perplexity can only be compared across language models that share an identical vocabulary[cite: 28, 32].

---

## 5. Smoothing Techniques

To prevent language models from assigning zero probability to unseen events, **smoothing** (or discounting) shaves probability mass from frequent events and redistributes it to unseen or rare n-grams[cite: 34].

### Laplace (Add-1) Smoothing
* Adds 1 to all n-gram counts and normalizes by the vocabulary size $V$[cite: 35]:
  $$P^*_{\text{Laplace}}(w_i \vert{} w_{i-1}) = \frac{\text{Count}(w_{i-1} w_i) + 1}{\text{Count}(w_{i-1}) + V}$$
[cite: 35]
* * drawback:* Shifts too much probability mass away from frequent items, making it suboptimal for modern language modeling.

### Add-$k$ Smoothing
* A parametric extension that adds a fractional value $k$ (e.g., $k = 0.05$ or $0.01$) optimized on a dev set[cite: 37]:
  $$P^*_{\text{Add-}k}(w_i \vert{} w_{i-1}) = \frac{\text{Count}(w_{i-1} w_i) + k}{\text{Count}(w_{i-1}) + kV}$$
[cite: 37]

### Backoff and Interpolation
* **Backoff:** If a higher-order n-gram (e.g., trigram) has a count of zero, "back off" to lower-order models (bigram or unigram), scaling back probability via a backoff weight $\alpha$[cite: 38].
* **Interpolation:** Mix probability estimates linearly from all n-gram estimators simultaneously[cite: 39]:
  $$\hat{P}(w_i \vert{} w_{i-2} w_{i-1}) = \lambda_1 P(w_i \vert{} w_{i-2} w_{i-1}) + \lambda_2 P(w_i \vert{} w_{i-1}) + \lambda_3 P(w_i)$$
  where $\sum \lambda_i = 1$[cite: 39].

### Advanced Smoothing Methods
* **Kneser-Ney Smoothing:** One of the best-performing traditional smoothing methods. It utilizes absolute discounting based on held-out counts and considers the *continuation probability* of a word (how likely a word is to appear in diverse left-contexts) rather than just its raw frequency[cite: 40].
* **Stupid Backoff:** Used for massive Web-scale corpora (where normalization is too computationally expensive). It applies simple unnormalized fallback ratios with a constant penalty factor $\lambda$[cite: 41]:
  $$S(w_i \vert{} w_{i-k+1}^{i-1}) = \begin{cases} \frac{\text{Count}(w_{i-k+1}^i)}{\text{Count}(w_{i-k+1}^{i-1})} & \text{if Count}(w_{i-k+1}^i) > 0 \\ \lambda S(w_i \vert{} w_{i-k+2}^{i-1}) & \text{otherwise} \end{cases}$$
[cite: 41]

