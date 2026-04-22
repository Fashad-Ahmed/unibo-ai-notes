Here are the complete, structured notes based on the lecture slides provided. 

## **Course & Lecture Overview**
* **Course:** Second cycle Degree in Artificial Intelligence (2025/26), Cognition & Neuroscience[cite: 12, 13].
* **Instructor:** Giuseppe di Pellegrino, Department of Psychology, University of Bologna[cite: 3, 4].
* **Core Premise:** The brain and artificial intelligence are two distinct systems shaped by entirely different pressures, yet they arrive at partially similar solutions for perception and behavior[cite: 23].

## **The Brain vs. Artificial Intelligence**
* **Artificial Intelligence:** AI optimizes for performance on a strictly defined task[cite: 28]. Its objective function is fixed during training time, and it operates without a body, metabolic costs, or survival pressure[cite: 29, 31, 32].
* **The Brain:** The brain optimizes for individual and social survival[cite: 34, 35]. It is embedded in a body with constant survival pressure, meaning its objective function is continuously respecified by its physiological state[cite: 36, 37].
* **The Surprising Parallel:** A model trained purely on image classification, with no built-in knowledge of the brain, can predict neural responses in the visual cortex better than models explicitly designed by neuroscientists (Yamins & DiCarlo, 2014)[cite: 41, 44].

## **The Core Concept: What is a Representation?**
* **Working Definition:** A representation is a transformation of data that makes a downstream task easier[cite: 48].
* **It is Not a Copy:** A representation is not a photograph or a faithful recording of raw input[cite: 111, 112, 113]. A perfect copy of a retinal image would actually be useless for recognizing a face[cite: 118].
* **It is Inherently Lossy:** Representations preserve what matters for the specific task and actively discard what does not[cite: 115]. Being "lossy" is not a limitation, but rather a necessity[cite: 116, 120].
* **Key Properties:** Representations are relative to what the system needs to do, they are evaluable (can be better or worse), and they always involve discarding information[cite: 126].

## **The Three Core Analytical Frameworks**
The lecture relies heavily on three tools to evaluate models and systems:

**1. Marr's Three Levels of Explanation (1982)** [cite: 73]
* **Level 1 (Computational):** What specific problem is the system solving, and why? [cite: 75] For example, the goal to extract meaningful structure to build a useful representation of the world[cite: 98, 99].
* **Level 2 (Algorithmic):** What internal representations does it use, and what operations are performed on them? [cite: 77] For example, applying filters, transformations, and edge detection to build invariant representations[cite: 86, 102, 103].
* **Level 3 (Implementational):** What is the physical substrate carrying this out? [cite: 79] For example, neurons in the V1 cortex versus matrix multiplications on a GPU[cite: 89, 108].

**2. Baker's Three Questions (2022)** [cite: 143]
* **WHAT is represented?** The information the internal state carries[cite: 134].
* **HOW is it represented?** The format, geometry of the space, and whether it is local or distributed[cite: 135, 139]. 
* **WHY that format?** The pressures that shaped it and what it makes easier downstream[cite: 138, 142].

**3. Representational Similarity Analysis (RSA)** [cite: 294]
* **Geometry as Meaning:** The geometry of a space—which stimuli activation patterns are near or far from each other—is the representation[cite: 258, 260].
* **The RDM:** Researchers compute the dissimilarity between pairs of responses to build a Representational Dissimilarity Matrix (RDM)[cite: 276, 278]. 
* **Comparative Power:** RSA allows researchers to rigorously compare the geometric structures of completely different systems, such as matching a deep network layer directly against a monkey's IT cortex[cite: 285, 288, 297].

## **The Visual Hierarchy and the Untangling Problem**
* **Early Representations (The Retina):** Raw sensory data encodes light intensity and is highly structured, but it is useless for recognition because a minor shift (like one pixel) creates a completely different pattern[cite: 147, 149].
* **Late Representations (IT Cortex):** Deep in the visual hierarchy, representations are impoverished of raw detail but highly useful because the same object produces a similar activation pattern regardless of its position, lighting, or size[cite: 169, 170].
* **The Untangling Problem:** In pixel space, object categories are "tangled" and interleaved, meaning no straight line can separate them[cite: 344, 346]. The visual hierarchy transforms this data, stage by stage, into an "untangled" format where distinct categories cluster together[cite: 348, 364].
* **Parallel Architecture:** The stages of the brain's ventral stream empirically mirror the layers of a deep network (e.g., V1 acts like early convolutional layers finding edges, while the IT cortex acts like final hidden layers finding complete objects)[cite: 184, 185, 187, 188, 190, 194].

## **What Makes a Representation "Good"?**
* A good representation allows task-relevant information to be read out easily by a simple downstream mechanism, such as a single biological neuron computing a weighted sum, or a linear classifier in an AI model[cite: 300, 301, 302, 303].
* **Separability:** Objects of the same category form linearly separable clusters[cite: 306, 310].
* **Invariance:** The representation remains stable despite changes to inputs that do not matter for the task, such as moving or rotating a coffee cup[cite: 308, 315].

## **Three Open Questions Driving the Course**
* Is the Yamins (2014) model a genuine representation of biological vision, or just a black box that happens to correlate with the brain's black box? [cite: 376]
* What is the brain's true "Level 1" computational problem? Is it strictly object recognition, or something entirely different? [cite: 377, 378]
* How do physiological states continuously reshape the brain's objective function, and what does this mean for the representations it builds compared to static AI models? [cite: 379, 380]