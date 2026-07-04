Lesson 21: Policy Gradients & Advanced Reinforcement Learning

If Q-Learning (Lesson 19) and DQN (Lesson 20) taught the AI how to estimate the value of a state, Lesson 21 represents the final evolution of Reinforcement Learning: teaching the AI to learn the Policy directly.

This lecture covers the exact algorithms (specifically PPO) that power modern AI giants like ChatGPT (via Reinforcement Learning from Human Feedback - RLHF).

1. The Limits of Value-Based Methods (Q-Learning)

In Q-Learning, the agent's behavior (the Policy) is implicit. The agent just calculates the Q-values for every action and picks the highest one (argmax Q).

The Flaw: This works perfectly when you have 4 distinct buttons (Up, Down, Left, Right). It completely fails in continuous action spaces (e.g., steering a car 12.5 degrees, or articulating a robot arm with 100 fluid joints). You cannot calculate the maximum of infinity.

The Fix: We drop the value calculations as our primary goal and directly mathematically optimize the policy itself.

2. On-Policy vs. Off-Policy (SARSA)

Before jumping to deep policy gradients, the slides mention SARSA (State-Action-Reward-State-Action). This highlights the fundamental difference between On-Policy and Off-Policy learning.

Q-Learning (Off-Policy): Learns the optimal policy even if the agent is exploring randomly. The Bellman update mathematically assumes the agent will take the absolute best action in the future (max Q(s', a')), even if it is currently taking random exploratory moves.

SARSA (On-Policy): Evaluates the exact policy the agent is currently executing. Instead of assuming the agent will take the max action, it updates based on the actual next action chosen by the $\epsilon$-greedy exploration:


$$Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma Q(s', a') - Q(s,a)]$$


(I have added a toggle for you in the GridWorld simulator to see how SARSA learns slightly safer, more cautious paths compared to Q-Learning because it accounts for its own random mistakes!)

3. Policy Gradients (REINFORCE)

Instead of predicting Q-values, we use a Neural Network to directly output a probability distribution over actions: $\pi_\theta(a|s)$.

The Goal: Maximize the expected cumulative reward $J(\theta)$.

The Math: We use gradient ascent. The agent plays a full episode. If the sequence of actions leads to a highly positive reward, we mathematically increase the probabilities of all actions taken in that sequence. If it falls in a trap, we decrease the probabilities.

4. Actor-Critic Architectures (A2C & A3C)

Pure Policy Gradients are unstable because rewards fluctuate wildly. We solve this by combining Policy networks and Value networks into an Actor-Critic setup:

The Actor: The policy network $\pi(s)$. It decides which action to take.

The Critic: The value network $V(s)$. It evaluates the state and tells the Actor if the action was better or worse than expected.

To make this exponentially faster, DeepMind introduced A3C (Asynchronous Advantage Actor-Critic):

Instead of one agent playing the game, you spawn 16 parallel agents in 16 isolated instances of the environment.

They all explore simultaneously, asynchronously sending their gradient updates back to a global master network. This gathers diverse data rapidly and breaks harmful correlations.

5. Proximal Policy Optimization (PPO)

This is the holy grail of modern Reinforcement Learning.

The Danger of Policy Gradients: If an Actor-Critic agent discovers a good action, standard gradient ascent might update the network's weights so aggressively that the network "overshoots" and completely breaks its own brain (catastrophic forgetting).

The PPO Solution (Clipped Objective): PPO introduces a strictly bounded mathematical guardrail.
It calculates the ratio between the new policy and the old policy. If the update tries to change the network by more than a specific threshold $\epsilon$ (usually 20%), the equation mathematically clips the gradient.


$$\mathcal{L}^{CLIP}(\theta) = \min \left( \text{ratio} \cdot A_t, \text{clip}(\text{ratio}, 1-\epsilon, 1+\epsilon) \cdot A_t \right)$$

The Result: PPO guarantees monotonic improvement. The agent takes small, perfectly stable steps toward mastery without ever falling off a mathematical cliff. It is the default algorithm used to train OpenAI's generative models today.
