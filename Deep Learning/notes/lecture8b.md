**The Sequence Problem Paradigm**

Traditional feed-forward networks struggle with sequential data. Sequence modeling involves solving distinct types of problems:

- Translation/Transformation: Turning an input sequence into a different output sequence (e.g., Language Translation, Speech-to-Text).
- Next-Term Prediction: Predicting the very next step in a sequence (e.g., predicting the next word in a sentence or the next frame in a video). This relies on shifting the target output by 1 step, blurring the line between supervised and unsupervised learning.
- Temporal State Prediction: Processing a sequence of states to predict a final result (heavily used in Reinforcement Learning and Robotics).

**Architectural Variations**

- One-to-Many: Image captioning (one image $\rightarrow$ sequence of words).
- Many-to-One: Sentiment analysis (sequence of words $\rightarrow$ one positive/negative label).
- Many-to-Many (Async): Language translation (read the whole sequence, then output a sequence).
- Many-to-Many (Sync): Video processing (output a prediction for every single frame).



**RNNs vs. Memoryless Approaches**

Before Recurrent Neural Networks (RNNs), engineers used Memoryless Approaches. These computed an output based only on a fixed, rigid window of past elements (e.g., looking strictly at $input(t-3)$ through $input(t)$). This failed because it could not handle long-term dependencies.


The RNN Solution:

RNNs introduce backward connections (loops). The hidden state $h_t$ at any given time step holds a "memory" of the past because it is calculated using the current input $x_t$ and the previous hidden state $h_{t-1}$.


**Training RNNs: Temporal Unfolding and BPTT**

Because neural networks operate on directed acyclic graphs (graphs without loops), we train RNNs using a conceptual trick called **Temporal Unfolding**.

 - Unrolling: We visualize the recurrent loop as a standard feed-forward network stretched out across time steps ($t=0, t=1, t=2 \dots$).
 - Shared Weights: The exact same weight matrices are reused at every single time step.
 - Backpropagation Through Time (BPTT): To update the weights, the network builds a stack of activities during the forward pass. During the backward pass, it calculates the gradient of the error at each time step and simply sums them together. For a shared weight $w$, the update is:$$\Delta w = \sum_{t} \frac{\partial E}{\partial w_t}$$