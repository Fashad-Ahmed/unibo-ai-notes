# Natural Language Processing: Vector Semantics and Sparse Embeddings

---

## Table of Contents

1. [Lexical Semantics](https://www.google.com/search?q=%231-lexical-semantics)
2. [Distributional Semantics](https://www.google.com/search?q=%232-distributional-semantics)
3. [Word Vectors and Co-occurrence Matrices](https://www.google.com/search?q=%233-word-vectors-and-co-occurrence-matrices)
4. [Vector Comparison Metrics](https://www.google.com/search?q=%234-vector-comparison-metrics)
5. [Reweighting Schemes (TF-IDF & PPMI)](https://www.google.com/search?q=%235-reweighting-schemes-tf-idf--ppmi)

---

## 1. Lexical Semantics

### Lemmas and Senses

* **Lemma (Citation Form):** The base dictionary form representing a set of inflected or archaic variants (e.g., *pipe* represents *pipes*, *pype*, *pyppe*, etc.). Dictionaries do not contain separate definitions for inflected forms.
* **Word Sense:** The discrete meaning component or concept associated with a word. Lemmas can be polysemous (possessing multiple meanings).
* **Word Sense Disambiguation (WSD):** The task of determining the correct word sense given a specific context. A strong baseline is choosing the most frequent sense.

### Lexical Relations

* **Synonymy:** A relation of near-identity between two senses of different words (e.g., *couch/sofa*, *water/$H_2O$*, *car/automobile*). Words are synonyms if they are mutually substitutable in any sentence without changing truth conditions (same propositional meaning). However, due to the *principle of contrast*, differences in linguistic form always signal subtle differences in meaning (slang, register, politeness), meaning true perfect synonymy is extremely rare.
* **Antonymy:** Senses that are opposites with respect to a single feature of meaning while remaining otherwise similar (e.g., *dark/light*, *short/long*, *fast/slow*). Antonyms can represent binary oppositions, scale endpoints, or reversives (*rise/fall*, *up/down*).
* **Other Semantic Relations:**
* **Hyponymy / IS-A (Subordination):** From specific concepts to superordinates (e.g., *car* is a subordinate of *vehicle*).
* **Hypernymy (Superordination):** From broad categories to subtypes (e.g., *furniture* $\rightarrow$ *lamp* $\rightarrow$ *desk lamp*).
* **Meronymy:** Part-whole relations (e.g., *wheel* or *brake* as parts of a *wheeled vehicle*).



### WordNet and Semantic Structures

* **WordNet:** A lexical database organized as a network of word senses, synsets, and lexical-semantic relations.
* **Supersenses:** 26 coarse lexicographic categories for nouns (such as *ACT*, *ANIMAL*, *ARTIFACT*, *FOOD*, *PERSON*, *SUBSTANCE*) that group fine-grained word senses.
* **Word Relatedness / Association:** Broader relationships connected via semantic fields (e.g., hospitals: *surgeon, scalpel, nurse, anaesthetic*) or semantic frames (perspectives/participants in events, such as a commercial transaction involving a *buyer, seller, goods, money*).
* **Connotation (Affective Meaning):** Evaluated across three dimensions: **Valence** (pleasantness), **Arousal** (intensity), and **Dominance** (control) (Osgood et al., 1957). Representing word meaning as coordinates in a multi-dimensional space formed the earliest expression of vector semantics.

---

## 2. Distributional Semantics

### Philosophical Foundations

* **Wittgenstein's Philosophical Investigations (1945):** Argued that concepts like *games* cannot be defined by a single unified feature, but are instead characterized by overlapping **"family resemblances"** (similarities and relationships criss-crossing across board-games, card-games, ball-games, etc.).
* **Distributional Hypothesis:** Defines a word by its usage and linguistic environment:
* *"The meaning of a word is its use in the language"* (Wittgenstein, 1953).
* *"If A and B have almost identical environments we say that they are synonyms"* (Harris, 1954).
* *"A word is characterized by the company it keeps"* (Firth, 1950).


* **Example:** By observing that *Ongchoi* appears in contexts like *"sautéed with garlic"*, *"over rice"*, and *"with salty sauces"*—similar to spinach, chard, or collard greens—we deduce its meaning.

### Vector Semantics and Embeddings

* **Vector Semantics:** Combines the distributional intuition (counting neighboring words) with the geometric intuition (defining word meaning as a point in an $N$-dimensional space).
* **Embeddings:** Words represented as vectors embedded in semantic space, where similar words reside nearby. Embeddings enable efficient semantic similarity computations for words, sentences, and documents without requiring complex manual supervision.

---

## 3. Word Vectors and Co-occurrence Matrices

Vector models are built upon co-occurrence matrices that record how frequently words appear together.

### Matrix Design Choices

* **Term-Document Matrix ($\vert{}V\vert{} \times \vert{}D\vert{}$):** Rows represent vocabulary words, and columns represent documents (e.g., tracking word frequencies across Shakespearean plays). Documents are represented as count vectors identifying points in $\vert{}V\vert{}$-dimensional space.
* **Word-Word (Term-Context) Matrix ($\vert{}V\vert{} \times \vert{}V\vert{}$):** Rows represent target words, and columns represent context words occurring within a defined window (commonly a symmetric window of 4 words to the left and right).

### Window Size and Scaling

* **Larger, flatter windows** capture broader thematic and semantic information.
* **Smaller, scaled windows** (such as $\frac{1}{n}$ distance weighting) capture local syntactic and collocational information.

---

## 4. Vector Comparison Metrics

To quantify the similarity between two word or document vectors, several geometric metrics are used:

* **Dot Product:** $\text{dot-product}(w, v) = w \cdot v = \sum_{i=1}^{n} w_i v_i$. Yields high values if vectors have large values in the same dimensions; equals 0 if orthogonal.
* **Vector Length:** $\vert{}v\vert{} = \sqrt{\sum_{i=1}^{n} v_i^2}$.
* **Cosine Similarity:** The normalized dot product measuring the cosine of the angle between two vectors:

$$\text{cosine}(w, v) = \frac{w \cdot v}{\vert{}w\vert{}\vert{}v\vert{}}$$



The cosine score reaches its maximum of 1 when the angle between two vectors is smallest ($0^\circ$).

---

## 5. Reweighting Schemes (TF-IDF & PPMI)

Raw frequency counts suffer from a frequency paradox: overly frequent stopwords are uninformative and poorly discriminative. Reweighting aims to amplify important, trustworthy, and unusual features while deemphasizing mundane words.

### TF-IDF (Term Frequency-Inverse Document Frequency)

Used primarily for term-document matrices:

* **Term Frequency ($tf$):** Typically log-transformed counts:

$$tf_{t,d} = \begin{cases} 1 + \log_{10} \text{Count}(t, d) & \text{if } \text{Count}(t, d) > 0 \\ 0 & \text{otherwise} \end{cases}$$


* **Inverse Document Frequency ($idf$):**

$$idf_t = \log_{10} \frac{N}{df_t}$$



where $N$ is the total number of documents and $df_t$ is the document frequency of term $t$. Words appearing in all documents (like *good* or *sweet*) receive an idf of 0.

### Positive Pointwise Mutual Information (PPMI)

An alternative weighting scheme used for word-word matrices, measuring how much more two words co-occur than expected by chance:

* **Pointwise Mutual Information (PMI):**

$$\text{PMI}(w, c) = \log_2 \frac{P(w, c)}{P(w)P(c)}$$


* **Positive PMI (PPMI):** Because negative PMI values (indicating co-occurrence less than chance) are unreliable noise, they are truncated to zero:

$$\text{PPMI}(w, c) = \max(\text{PMI}(w, c), 0)$$


* **Weighting / Smoothing PPMI:** Because standard PMI is biased toward extremely rare words (which yield artificially inflated scores), context probabilities can be smoothed using parameter $\alpha$ (typically set to $0.75$):

$$\text{PPMI}_\alpha(w, c) = \max \left( \log_2 \frac{P(w, c)}{P(w)P_\alpha(c)}, 0 \right)$$



where $P_\alpha(c) = \frac{\text{Count}(c)^\alpha}{\sum_c \text{Count}(c)^\alpha}$. Raising counts to $\alpha = 0.75$ increases probability assigned to rare contexts and lowers their PMI.