
## Table of Contents

1. [Course Overview & Definition](https://www.google.com/search?q=%231-course-overview--definition)
2. [Levels of Linguistic Representation](https://www.google.com/search?q=%232-levels-of-linguistic-representation)
3. [Why is NLP Hard?](https://www.google.com/search?q=%233-why-is-nlp-hard)
4. [History & Evolution of NLP Approaches](https://www.google.com/search?q=%234-history--evolution-of-nlp-approaches)
5. [Syllabus & Course Structure](https://www.google.com/search?q=%235-syllabus--course-structure)
6. [Related Academic & Technical Disciplines](https://www.google.com/search?q=%236-related-academic--technical-disciplines)
7. [Course Logistics & Assessment Guidelines](https://www.google.com/search?q=%237-course-logistics--assessment-guidelines)

---

## 1. Course Overview & Definition

### What is Natural Language Processing?

NLP is the domain of Artificial Intelligence focused on **automating the analysis, generation, and acquisition of human ("natural") language**[cite: 5, 25]:

* **Analysis (Understanding / Processing):** Input is natural language; output is a structured representation supporting useful actions[cite: 5, 7].
* **Generation (Generative AI):** Input is a structured representation; output is natural language[cite: 5, 7].
* **Acquisition:** Obtaining necessary algorithms and representations from knowledge and data[cite: 7].

### Why is NLP Useful?

* Web search and question answering over unstructured text documents[cite: 6].
* Machine translation between human languages[cite: 6].
* Accelerating medical and scientific research[cite: 6].
* Estimating public opinion and making predictive analytics[cite: 6].
* Managing conversational agents, checking grammar, filtering fake news/hate speech[cite: 6].
* Code generation, poem/novel composition, interactive learning systems, and accessibility/disaster support[cite: 6].

---

## 2. Levels of Linguistic Representation

Language processing is typically broken down into a hierarchy of linguistic strata:

```
[Discourse] 
    └── [Pragmatics]
          └── [Semantics]
                └── [Syntax]
                      └── [Lexemes / Morphology]
                            └── [Phonology / Orthography]
                                  └── [Phonetics / Speech Text]

```

* **Phonetics & Phonology / Orthography:** Sound systems, speech waveforms, and text character tokens.
* **Morphology:** Analysis of words into meaningful components (spectrum ranges from analytic/isolating languages like English/Chinese to synthetic languages like Turkish/Finnish) [cite:.
* **Lexemes (Lexical Analysis):** Normalizing and disambiguating words (e.g., handling polysemy like *bank* or *mean*, multi-word expressions, and Part-of-Speech tagging) [cite: ].
* **Syntax:** Transforming a sequence of symbols into hierarchical/compositional structures, while managing combinatorial ambiguities (e.g., prepositional phrase attachment, verb phrase attachment, coordination scope) [cite: ].
* **Semantics:** Mapping natural language sentences into formal domain representations (database queries, logic expressions, robot commands) [cite: ].
* **Pragmatics & Discourse:** Managing non-local meaning phenomena, multi-sentence structures, dialogues, and multi-party conversations [cite: ].

---

## 3. Why is NLP Hard?

* **Noisy Inputs:** Text data from the wild is unstructured, uncurated, and full of errors.
* **Latent Constructs:** Linguistic representations are theoretical models; they cannot be observed directly [cite: ].
* **Data Scarcity:** Obtaining clean training annotations for every specific linguistic aspect is expensive and difficult [cite: ].
* **Complex Mappings:** Interactions across linguistic levels are highly non-linear and context-dependent [cite: ].
* **Pervasive Ambiguity:** Every string can have multiple interpretations. While humans naturally leverage context to resolve ambiguities, computers require deep semantic understanding to do so reliably [cite: ].
* **Linguistic Diversity:** Human languages express identical concepts through radically different structures [cite: ].

---

## 4. History & Evolution of NLP Approaches

The field has evolved through four major historical eras/inflection points:

1. **Statistical & Neural Foundations (Early Era):** Early pioneers like Shannon, Osgood, and Rosenblatt (Perceptron) [cite: ].
2. **The Symbolic Turn (1960s–1970s):** Movement toward symbolic structure, driven by Chomsky's critique of statistical models and Minsky & Papert's critique of early neural models [cite: ].
3. **The Revival of Empiricism (1980s–2010s):** The resurgence of statistical NLP, hidden Markov models (HMMs), probabilistic parsing, TF-IDF, WordNet, LSA, and early neural network word embeddings (`word2vec`) [cite: ].
4. **The LLM Era (Present):** Deep learning dominance, Transformers, Attention mechanisms, Large Language Models (BERT, GPT-3), RAG, and Reinforcement Learning (RLHF/RLVR) [cite: ].

---

## 5. Syllabus & Course Structure

* **Syntactic & Lexical Analysis:** Edit distance, Part-of-Speech (POS) tagging [cite: ].
* **Semantics:** Document encoding, language modeling, distributed semantics, vector embeddings [cite: ].
* **Architectures & Tools:** Basic text processing tools, Recurrent Neural Networks (RNNs), Convolutional Neural Networks (CNNs), Seq2Seq models, and Advanced Attention/Transformer-based architectures [cite: ].
* **Large Language Models:** Encoder vs. decoder configurations, fine-tuning vs. in-context learning, prompting, pre-training, alignment, and evaluation [cite: ].
* **Applications:**
* *Analytical:* Text classification, sentiment analysis, information retrieval, question answering, argument mining [cite: ].
* *Generative:* Retrieval-Augmented Generation (RAG), neural machine translation [cite: ].



---

## 6. Related Academic & Technical Disciplines

* **Natural Language Processing (NLP):** Branch of AI focused on language processing technology (NLU & NLG) [cite: ].
* **Computational Linguistics:** Focused on implementing computational models to support linguistic theories (e.g., diachronic language change) [cite: ].
* **Information Retrieval (IR):** Obtaining resources relevant to an information need from large collections (e.g., web search engines) [cite: ].
* **Text Mining & Big Data Analytics:** Subtypes of data mining focused on discovery and extraction from massive text corpora (e.g., biomedical text mining) [cite: ].

---

## 7. Course Logistics & Assessment Guidelines

### Recommended Textbooks & Tools

* **Primary Textbook:** *Speech and Language Processing* (3rd Edition online draft) by Dan Jurafsky and James H. Martin [cite: ].
* **Reference Books:** *Natural Language Processing* (J. Eisenstein); *NLP with Python* (S. Bird); *NLP with Transformers* (L. Tunstall); *Deep Learning* (C.M. Bishop) [cite: ].
* **Software Stack:** Python, NLTK, Google Colab, PyTorch, Hugging Face, LangChain [cite: ].

### Assessment Scheme

The final score is cumulative (max 31 points for *Cum Laude*):

* **Written Exam:** Up to **22 points** (covers all course topics + a 4-point question dedicated to your assignments) [cite: ].
* **Assignments:** **2 assignments**, worth up to **4 points each** (Total 8 points) [cite: ].
* *Speed Bonus:* **+0.5 points** per assignment if submitted by **January 10, 2026** [cite: ].
* *Merit Bonus:* **+0.5 points** for exceptionally clever work [cite: ].
* Can be done individually or in groups of 2–3 students (group changes allowed between assignments) [cite: ].


