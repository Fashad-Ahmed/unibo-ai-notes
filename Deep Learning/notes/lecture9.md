**Regularization & Dropout**

Neural networks are inherently prone to overfitting. To combat this, several techniques are used, including early stopping, weight-decay, data augmentation, and dropout.

- Dropout Mechanism: Dropout stochastically "cripples" the neural network by disabling hidden units during training with a specific probability, such as $p = 0.5$.
- Purpose: This prevents hidden units from co-adapting with one another. It effectively acts as a way to train many different crippled networks and average their results.
- Geometric Averaging: During training, only the active (crippled) network is trained via backpropagation, and weights are shared among all the different crippled configurations. To compensate for the disabled units mathematically, the weights of the remaining active units are multiplied by $1/p$.