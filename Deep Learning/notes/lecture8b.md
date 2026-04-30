The Sequence Problem Paradigm
Traditional feed-forward networks struggle with sequential data. Sequence modeling involves solving distinct types of problems:

- Translation/Transformation: Turning an input sequence into a different output sequence (e.g., Language Translation, Speech-to-Text).
- Next-Term Prediction: Predicting the very next step in a sequence (e.g., predicting the next word in a sentence or the next frame in a video). This relies on shifting the target output by 1 step, blurring the line between supervised and unsupervised learning.
- Temporal State Prediction: Processing a sequence of states to predict a final result (heavily used in Reinforcement Learning and Robotics).

**Architectural Variations**

- One-to-Many: Image captioning (one image $\rightarrow$ sequence of words).
- Many-to-One: Sentiment analysis (sequence of words $\rightarrow$ one positive/negative label).
- Many-to-Many (Async): Language translation (read the whole sequence, then output a sequence).
- Many-to-Many (Sync): Video processing (output a prediction for every single frame).