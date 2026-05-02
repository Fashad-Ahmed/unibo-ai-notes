**Regularization & Dropout**

Neural networks are inherently prone to overfitting. To combat this, several techniques are used, including early stopping, weight-decay, data augmentation, and dropout.

- Dropout Mechanism: Dropout stochastically "cripples" the neural network by disabling hidden units during training with a specific probability, such as $p = 0.5$.
- Purpose: This prevents hidden units from co-adapting with one another. It effectively acts as a way to train many different crippled networks and average their results.
- Geometric Averaging: During training, only the active (crippled) network is trained via backpropagation, and weights are shared among all the different crippled configurations. To compensate for the disabled units mathematically, the weights of the remaining active units are multiplied by $1/p$.


**Normalization Layers**

Normalization aims to increase the independence between layers, leading to more stable and potentially faster training.

- Batch Normalization: This operates on single layers on a per-channel basis. During each training iteration, it normalizes the input by subtracting the moving batch mean ($\mu_B$) and dividing by the batch standard deviation ($\sigma_B$).
- Learned Parameters: After normalizing, it applies an opposite transformation using learned parameters: $\gamma$ (scale) and $\beta$ (center).
- Prediction Mode: Batch normalization behaves differently during prediction. Once training is complete, stable statistics computed from the entire training dataset are used instead of moving batch statistics.