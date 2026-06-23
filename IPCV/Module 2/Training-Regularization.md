
# The big picture

This lecture answers: *given a fixed architecture, how do you actually get it to train well and generalize well?* It has three acts:
1. **Generalization theory** — what causes a gap between training and test performance, and how "capacity" controls it (both theoretical and *effective* capacity).
2. **Learning rate** — the single most important optimization hyperparameter, and the schedules used to set it over time.
3. **Regularization** — a long catalog of specific techniques (weight decay, label smoothing, dropout, stochastic depth, data augmentation in its many forms) that all share one purpose: shrink the test error without necessarily helping (and sometimes slightly hurting) the training error.

It closes with **practical "recipe" wisdom**: how all these pieces get combined and tuned in real training pipelines.Now let's go through every section.

---

# Part 1 — Generalization error and model capacity (Slides 2–8)

## The fundamental curve (Slide 2)

Plot error rate against **model capacity**. Training error keeps falling as capacity grows (a more flexible model can always fit the training set better). **Validation/test error** initially falls too — but past some point, it starts rising again, even though training error keeps falling. This creates the classic **U-shaped generalization curve**:

- **Underfitting region** (low capacity): both training and test error are high — the model is too simple to capture the true pattern.
- **Overfitting region** (high capacity): training error keeps dropping, but test error rises — the model starts memorizing noise/idiosyncrasies specific to the training set rather than learning the true underlying signal.
- **Optimal model capacity**: the sweet spot where test error is minimized.

**What controls capacity**, exactly as listed: network width, network depth, input resolution, architecture, etc.

## Worked example: polynomial regression (Slide 3)

Ground truth: a noisy cubic $y=ax^3+bx^2+cx+d+\epsilon$. Fit with polynomials of degree $K$:

- **$K=1$ (linear model)**: too simple to capture the cubic curvature — **underfitting**. Low $R^2$ on both train (0.709) and test (0.865) — note here test even looks *better* than train, just because of how the particular sampled points land, but both are clearly mediocre.
- **$K=3$ ("right" model)**: matches the true generating function's degree exactly — excellent fit on both train (0.999) and test (0.993).
- **$K=9$ ("interpolating" model)**: degree far exceeds what's needed — the model has enough freedom to **pass through every single training point exactly** ($R^2_{train}=1.000$), but wildly oscillates between points, producing **catastrophic** test performance ($R^2_{test}=-447.7$, i.e. far worse than even just predicting the mean). This is the canonical picture of **overfitting**: perfect training fit, useless generalization.

## Effective capacity (Slide 4) — a crucial distinction for deep learning

In practice, with neural networks, you typically train one **fixed architecture** whose **theoretical capacity** (decided once: width, depth, resolution) is large and unchanging. But the **effective capacity actually realized during training** can still move around substantially due to **optimization hyperparameters and regularization** — things like learning rate, favoring small parameter values, and total training time.

**Why this distinction matters, conceptually**: you don't need to literally shrink the architecture to control overfitting — you can keep a huge, expressive theoretical-capacity model, and instead **constrain how much of that capacity gets actually used** during training via the choices you make in the training recipe. This is the conceptual bridge that justifies the rest of the lecture: regularization techniques are precisely the tools for dialing **effective capacity** down from a fixed **theoretical capacity** ceiling.

---

# Part 2 — Learning rate (Slides 5–11)

## Why learning rate matters so much (Slide 5)

Comparing training loss curves for different fixed learning rates:
- **Very high LR**: loss initially decreases but then **diverges/explodes upward** — the optimizer overshoots minima repeatedly, with steps too large to settle anywhere.
- **Low LR**: steady, monotonic decrease, but **very slow** — training takes far longer than necessary to reach a good loss.
- **High LR** (moderate-high, not "very high"): fast initial decrease, but then **plateaus early and gets stuck** at a mediocre loss value — too large a step size to settle into the bottom of a narrow minimum.
- **Good LR**: fast decrease *and* continues improving, reaching the lowest final loss.

**The core problem stated explicitly**: it's genuinely **hard to find one single, fixed learning rate** that's simultaneously good for the early phase of training (where you want big, fast steps to traverse the loss landscape quickly) and the later phase (where you want small, careful steps to settle precisely into a minimum).

**The solution, stated directly**: *use a mixture of high and low* — i.e., don't use one constant LR for the entire run, **vary it over time** according to a **schedule**. This motivates the entire rest of the LR section.

## Why a too-large LR causes early stalling, intuitively (Slide 6)

A 1D loss-landscape sketch: if the learning rate is too large, gradient descent steps **overshoot** the local curvature of the loss — instead of smoothly descending into a basin, the parameter **bounces between the two walls** of a narrow valley, repeatedly overshooting the minimum rather than converging into it. Training loss drops fast at first (while still far from any minimum, where the landscape is broad) but then **gets stuck oscillating** once it nears a narrower region, since the fixed large step size is now too coarse to actually settle there.

## Step decay schedule (Slide 7)

**Recipe**: start with a high learning rate (e.g. 0.1), and **divide by 10** whenever the validation/training error **plateaus** (stops improving).

The ResNet plot shown is the canonical illustration: training error drops in clear "shelves" — a steep fall, then a long flat plateau, then a sudden further drop exactly at the moment the learning rate is divided by 10, then another plateau, then another drop. **Each LR drop "unsticks" the optimizer from whatever plateau the previous (now too-large) LR had stalled it on**, letting it carve out additional, finer-grained progress. This was the schedule used, e.g., in ResNet's original training.

## The "favor wide minima" intuition (Slide 8) — an important nuance

The slide poses something subtle: **why does decaying the LR over time, in this staged fashion, tend to generalize *better* than just using a small LR from the very start?**

The cited explanation (Hochreiter & Schmidhuber 1997; Keskar et al. 2017): minima of the loss landscape come in different "widths" — **flat/wide minima vs sharp/narrow minima**. The intuition is that **wide minima generalize better** than narrow minima, because a wide minimum is more "forgiving": small differences between the train and test loss landscapes (since the test set is a slightly different sample) still leave you near a good solution, whereas a narrow minimum's good performance is fragile to such small landscape shifts.

**Mechanistically, why does an LR schedule favor finding wide minima?** The large steps used early in training (high LR) are **too coarse to settle into narrow minima** — a large step would simply overshoot a narrow basin entirely, so the optimizer effectively "skips over" narrow minima and continues exploring until it lands somewhere broad enough that even a large step can't escape (i.e., a wide minimum). Only **later**, once the LR has decayed and steps are small, does the optimizer carefully settle into the bottom of whichever (wide) basin it ended up exploring. So the schedule **implicitly biases the entire search toward wide minima**, which is argued to be a key reason LR schedules help generalization, not just optimization speed.

## Cosine schedule (Slide 9)

$$lr_e = lr_E + \frac{1}{2}(lr_0-lr_E)\Big(1+\cos\big(\tfrac{e\pi}{E}\big)\Big)$$

where training runs for $E$ total epochs, $lr_0$ is the initial LR, $lr_E$ is the final LR, and $lr_e$ is the LR at epoch $e$.

**What this formula does, mechanically**: at $e=0$, $\cos(0)=1$, so $lr_0$ exactly (the term simplifies to $lr_E+\tfrac12(lr_0-lr_E)\cdot2=lr_0$). At $e=E$, $\cos(\pi)=-1$, so the term becomes $lr_E+\tfrac12(lr_0-lr_E)\cdot0=lr_E$. In between, it traces a **smooth cosine-shaped decay curve** from $lr_0$ down to $lr_E$.

**Why use this instead of step decay, exactly as stated**: it *"lets the optimizer follow a similar path to step decays with less hyperparameters to tune."* Step decay requires you to manually choose **when** each plateau happens and **by how much** to divide each time (multiple discrete hyperparameters). Cosine decay achieves a qualitatively similar smooth-then-fast-then-smooth decay shape automatically, governed by just $lr_0, lr_E, E$ — far fewer knobs to tune by hand.

## Warm-up (Slide 10) — fixing a specific early-training failure

**The specific problem it solves**: schedules conventionally **start** with a high LR — but for **very deep networks** (the slide's example: ResNet-110 on CIFAR-10), starting immediately at a high LR can **slow down convergence dramatically at the very beginning**: accuracy can remain stuck at chance level for several epochs before training "kicks in" at all.

**Diagnosis, stated explicitly**: this stalling is usually a **symptom of poor initialization** — the network's random initial weights put it in a part of the loss landscape where large gradient steps (driven by the high starting LR) are actively harmful/destabilizing rather than helpful, because the gradients computed from a poorly-initialized network can be unreliable or huge in magnitude.

**Fix**: use a **lower learning rate for a few epochs** at the very start of training (even less than one full epoch, e.g. "until accuracy increases") before switching to the normal (higher) scheduled LR. **Bonus benefit, also explicitly noted**: warm-up is *"usually beneficial also for shallower, randomly initialized networks"* in general, since early training is often in a "hard-to-navigate" region of the loss landscape regardless of depth — warm-up gives the optimizer a gentler initial foothold before ramping up.

## One-cycle schedule (Slide 11)

This is a genuinely different *shape* of schedule from step/cosine — it **increases** the LR first, then decreases it, all within a single training run (hence "one cycle").

$$lr_i = \begin{cases} lr_{max} + (lr_0-lr_max)\left(1-\dfrac{i}{pI}\right) & \text{if } i < pI \\[6pt] lr_{min}+(lr_{max}-lr_{min})\left(1-\dfrac{i-pI}{I-pI}\right) & \text{if } i\ge pI\end{cases}$$

where $I$ is the total number of iterations (note: **per-iteration/mini-batch**, not per-epoch — this is a finer-grained schedule than step or cosine, which update once per epoch), and $p$ is the **fraction of iterations spent increasing** the LR (e.g. $p=0.3$).

**Mechanically**: for the first $pI$ iterations, LR **rises** from $lr_0$ up to a peak $lr_{max}$; for the remaining $(1-p)I$ iterations, LR **falls** from $lr_{max}$ down to $lr_{min}$ (note $lr_{min}$ can be, and often is, even lower than the original starting $lr_0$ — undershooting at the very end, for fine convergence).

**Implementation note explicitly given**: the **original proposal had 3 phases**, but **PyTorch and other popular implementations use 2 phases** (rise then fall, as written above), and this two-phase version is **usually implemented using cosine-shaped segments** rather than the straight-line interpolation the formula above literally describes (the formula shown is the simpler linear version, but practical implementations smooth each segment with a cosine curve instead).

---

# Part 3 — Regularization: definition and the general template (Slide 12)

## The definition (memorize verbatim — likely to be asked directly)

> **Regularization is any modification we make to the training recipe that is intended to (1) reduce generalization (test) error, but (2) not necessarily reduce — and possibly even slightly increase — training error.**

This definition is the single filter to run every technique in this lecture through: each one trades away a *bit* of training-set fit in exchange for a model that's less tailored to training-set-specific noise, and thus generalizes better.

**Techniques the lecture reviews, listed exactly**: parameter norm penalties, early stopping, label smoothing, dropout, stochastic depth, data augmentation.

**Effect on the capacity curve**: regularization effectively **shifts the U-shaped generalization curve**, moving the **optimal model capacity point further to the right** — i.e., with good regularization in place, you can use a *larger*, more expressive model (more theoretical capacity) before overfitting becomes a problem, because the regularizer is actively suppressing the model's tendency to exploit that extra capacity to memorize noise.

---

# Part 4 — Parameter norm penalties / weight decay (Slides 13–15, 18)

## The general formula (Slide 13)

$$L(\theta;D^{train}) = L^{task}(\theta;D^{train}) + \lambda\, L^{reg}(\theta)$$

- $L^{task}$: the **task (data) loss** — e.g. cross-entropy — measures how well the model fits the actual data/labels.
- $L^{reg}(\theta)$: the **regularization loss** — depends only on the parameters $\theta$ themselves, not on any data — penalizes "complex" parameter configurations.
- $\lambda$: the regularization **strength** hyperparameter, controlling the trade-off between the two terms.

**Two common norms, exactly as given:**
$$l_2\text{ regularization: } L^{reg}(\theta)=\sum_i \theta_i^2 \qquad l_1\text{ regularization: } L^{reg}(\theta)=\sum_i|\theta_i|$$

**The intuition, stated directly**: *"even if a model has millions of parameters, a constraint on the overall norm of the parameters forces them to be small, thereby limiting the effective capacity of the model."* This is exactly the "effective vs theoretical capacity" idea from Part 1 in action: the architecture's theoretical capacity hasn't shrunk at all, but constraining parameter magnitudes prevents the model from realizing its full expressive potential, which empirically tends to reduce overfitting (large, finely-tuned weights are typically what's needed to fit noise precisely; small weights bias the model toward smoother, simpler functions).

## Worked example: $l_2$-regularized polynomial regression (Slide 14)

Same setup as Part 1's cubic example, but now fitting a **high-capacity degree-9 polynomial** while varying $\lambda$:

- **$\lambda\to+\infty$ ("linear" model)**: the penalty dominates so heavily that essentially all coefficients except the lowest-order ones get crushed toward zero — effectively forcing the high-capacity model to *behave* like a low-capacity (linear) one. Underfitting again.
- **Appropriate $\lambda$ ("right" model)**: balances fitting the data against keeping weights small — recovers a good fit ($R^2_{train}=0.968,R^2_{test}=0.954$), almost matching the earlier "correctly chosen degree-3" result, but now achieved with a *high-capacity* model that's been properly regularized rather than by hand-picking the "correct" architecture size.
- **$\lambda\to0$ ("interpolating" model)**: no effective penalty, so we're back to the same severe overfitting catastrophe as the unregularized degree-9 case.

**The big lesson here**: regularization strength $\lambda$ is itself acting exactly like model capacity did in Part 1 — it's a **second knob for controlling effective capacity**, independent of and in addition to the architecture's raw size.

## Why $l_2$ regularization = "weight decay" (Slide 15, 18) — the full derivation

$$L(\theta;D^{train}) = L^{task}(\theta;D^{train}) + \frac{\lambda}{2}\|\theta\|_2^2$$

(Note: the $\tfrac12$ factor is just a convenience — it cancels neatly with the derivative of the squared term, as you'll see.)

**Derive the SGD update step**, starting from the plain gradient-descent rule:

$$\theta^{(i+1)} = \theta^{(i)} - lr\,\nabla_\theta L(\theta^{(i)};D^{train})$$

Substitute the full (task + regularization) loss:

$$= \theta^{(i)} - lr\,\nabla_\theta\Big[L^{task}(\theta^{(i)};D^{train}) + \frac{\lambda}{2}\|\theta^{(i)}\|_2^2\Big]$$

The gradient of $\frac{\lambda}{2}\|\theta\|_2^2 = \frac{\lambda}{2}\sum_i\theta_i^2$ with respect to $\theta$ is simply $\lambda\theta$ (power rule on each term, the $\tfrac12$ cancels the exponent-2's factor of 2):

$$= \theta^{(i)} - lr\Big[\nabla_\theta L^{task}(\theta^{(i)};D^{train}) + \lambda\theta^{(i)}\Big]$$

Distribute and regroup:

$$= \theta^{(i)} - lr\,\nabla_\theta L^{task}(\theta^{(i)};D^{train}) - lr\,\lambda\,\theta^{(i)} = \underbrace{(1-lr\,\lambda)\,\theta^{(i)}}_{\text{decayed parameter vector}} \;-\; \underbrace{lr\,\nabla_\theta L^{task}(\theta^{(i)};D^{train})}_{\text{gradient without regularization}}$$

**Why this is called "weight decay"**: notice the update is now **exactly the same as the ordinary, unregularized gradient step**, *except* that **before** applying the usual gradient update, the current parameter vector first gets **multiplied by $(1-lr\,\lambda)$**, a number slightly less than 1. So every single optimization step, **regardless of what the gradient says**, the weights get pulled a tiny bit toward the origin (multiplied by a factor just under 1) — they **decay**. This is for **plain SGD specifically**; the slide notes this exact equivalence (decay-then-gradient-step ≡ $l_2$-penalized loss gradient step) is why frameworks like PyTorch literally implement weight decay as a separate `weight_decay` hyperparameter in the optimizer (`torch.optim.SGD(..., weight_decay=0, ...)`) rather than making you manually add the penalty term to your loss function — they're mathematically identical for plain SGD.

**Other names, explicitly given**: $l_2$ regularization is also known as **ridge regression** or **Tikhonov regularization** (these are the names used in classical statistics/applied math).

---

# Part 5 — Early stopping (Slide 16)

**Core idea**: treat the **number of training iterations/epochs itself as a hyperparameter** that controls effective capacity. As training progresses, training accuracy keeps climbing, but validation accuracy typically rises, peaks, then starts to *decline* (as the model begins to overfit). **Early stopping** = monitor validation performance during training, and at inference time, **use the checkpoint (the saved set of weights) corresponding to the best validation performance ever seen**, not necessarily the final one.

**The framing, stated explicitly**: this is literally a form of hyperparameter selection — by choosing the best-performing checkpoint, *"we are effectively selecting the best value for this hyperparameter"* (the hyperparameter being "#param updates / #epochs"). It's regularization in the cheapest possible form: you don't change the loss, the architecture, or any training mechanics — you simply **stop training at the right time** rather than running until training loss is minimized.

---

# Part 6 — Label smoothing (Slides 17–21)

## The problem cross-entropy has (Slide 17)

The standard cross-entropy loss target is the **one-hot encoding** of the true label: a vector that's exactly 1 at the correct class and exactly 0 everywhere else.

**The issue**: for the loss to reach exactly 0, the softmax output for the correct class would need to be **exactly 1**, which (since softmax is computed via exponentials, $\frac{\exp(s_y)}{\sum_k\exp(s_k)}$) requires the correct class's raw score $s_y\to+\infty$ **and** every other class's score $s_{k\neq y}\to-\infty$. **Pushing scores toward these extremes can cause overfitting**: the network is incentivized to become *infinitely* confident, which in practice means driving weights to ever-larger magnitudes chasing an unreachable target, a recipe for overconfident, poorly-calibrated, overfit predictions.

## The fix: label smoothing encoding (Slide 17)

Instead of a one-hot target, **assume the label itself might be slightly noisy/corrupted with probability $\epsilon$**, and build a softened target distribution:

$$LS(y^{(i)},\epsilon)_k = \begin{cases} 1-\epsilon\dfrac{(C-1)}{C} & k=y^{(i)} \text{ (correct class)} \\[6pt] \dfrac{\epsilon}{C} & k\neq y^{(i)} \end{cases}$$

where $C$ is the total number of classes. (Worked numeric example given directly: with $C=10,\epsilon=0.1$, correct class gets $0.91$, every other class gets $0.01$ each — summing to $0.91+9\times0.01=1.0$, confirming it's a valid probability distribution.)

**Why this helps, and the bonus interpretation explicitly given**: it prevents the "push scores to infinity" overfitting incentive, since the target is now achievable with finite scores. **It also naturally accounts for mislabeled training examples** — if a small fraction of your dataset's labels are simply wrong, training against a *slightly* soft target (rather than a maximally-confident one-hot target) makes the model somewhat more robust to that label noise, since it's never being asked to be infinitely certain about any single training example.

## Practical implementation across PyTorch versions (Slides 18–19)

- **PyTorch ≥1.10**: trivial — `torch.nn.CrossEntropyLoss(..., label_smoothing=0.0)` — just pass the *integer* correct-class index as before, and set `label_smoothing > 0`; the smoothing is handled internally.
- **PyTorch <1.10**: `CrossEntropyLoss` **only accepts a single integer class index as the target**, not a full probability vector — so you **cannot** directly pass the label-smoothing-encoded vector to it. This forces a workaround, which is exactly what motivates the next two slides (cross-entropy's information-theoretic reformulation, then `KLDivLoss`).

## Why is it called "cross-entropy" loss, precisely (Slide 20)

**Cross-entropy between two distributions $p,q$ over the same event set:**

$$H(p,q) = -\mathbb{E}_p[\log q] = -\sum_{x\in\mathbb{X}} p(x)\log q(x)$$

In classification, the event set $\mathbb{X}$ = the $C$ classes. **Key reframing**: think of the **one-hot encoding of the true label as the distribution $p$**, and the **model's softmax output as the distribution $q$**. Substituting:

$$H\big(\mathbb{1}(y^{(i)}),\,p_{model}(Y|x^{(i)};\theta)\big) = -\sum_{k=1}^C \mathbb{1}(y^{(i)})_k\log p_{model}(Y=k|x^{(i)};\theta) = -\log p_{model}(Y=y^{(i)}|x^{(i)};\theta)$$

(the sum collapses to a single term because $\mathbb{1}(y^{(i)})_k$ is 1 only at $k=y^{(i)}$ and 0 elsewhere) — **this is exactly the familiar, standard cross-entropy loss formula** you already know. The point of this derivation: it reveals that the "cross-entropy loss" is literally just the **general information-theoretic cross-entropy formula**, specialized to the case where $p$ happens to be a one-hot distribution.

## Generalizing to label smoothing via KL divergence (Slide 21)

**The payoff of the previous derivation**: since cross-entropy is defined for *any* two distributions $p,q$, you can simply **swap in the label-smoothing distribution for $p$** instead of the one-hot:

$$H\big(LS(y^{(i)},\epsilon),\,p_{model}(Y|x^{(i)};\theta)\big) = -\sum_{k=1}^{C} LS(y^{(i)},\epsilon)_k\,\log p_{model}(Y=k|x^{(i)};\theta)$$

This sum **no longer collapses to one term** (since $LS$ is nonzero at *every* class, not just the correct one) — which is exactly why plain `CrossEntropyLoss` (designed for single-index targets) can't compute this directly in old PyTorch.

**The KL-divergence connection:**

$$H(p,q) = H(p) + D_{KL}(p\,\|\,q)$$

where $H(p)$ is the **entropy** of $p$ alone (a fixed property of $p$, not depending on $q$ at all), and $D_{KL}(p\|q)$ is the **Kullback-Leibler divergence** from $q$ to $p$.

**Crucial consequence stated explicitly**: since $H(LS(y^{(i)},\epsilon))$ is a **constant** (it depends only on the fixed target distribution, never on the model's parameters $\theta$), **minimizing cross-entropy $H(p,q)$ is exactly equivalent to minimizing $D_{KL}(p\|q)$** — the constant entropy term doesn't affect where the minimum is, just shifts the loss value by a fixed offset. **Direction matters, explicitly flagged**: this is $D_{KL}(p\|q)$ — divergence "from the model $q$ to the labels $p$" — and **KL divergence is NOT commutative** ($D_{KL}(p\|q)\neq D_{KL}(q\|p)$ in general), so getting the order right matters both mathematically and for matching the API correctly.

**Practical payoff**: `torch.nn.KLDivLoss` computes exactly this — but its **API convention is the opposite of what you might guess**: `target` = $p$ (i.e., the label-smoothing-encoded true distribution) and `input` = $\log q$ (i.e., the **log** of the model's predicted probabilities, not the raw probabilities — `log_target=False` by default refers to whether the *target* is in log-space, not the input). This was the standard workaround for implementing label smoothing before native support was added to `CrossEntropyLoss`.

---

# Part 7 — Dropout (Slides 22–30)

## The mechanism (Slide 22)

**In each forward pass during training**, randomly **zero out** some activations (not weights — activations, the actual outputs of a layer for a given input). The probability of **keeping** a unit active is a hyperparameter $p$ (commonly 0.5, sometimes as high as 0.8–0.9 for less aggressive dropout). **Every mini-batch gets a freshly-sampled random binary mask** — it's not fixed once and reused; a different random subset of units is dropped every single forward pass.

**Where it can be applied, exactly as stated**: between any two layers — **but never to the output activations** (the final layer's scores must always be fully present, since you need every class's actual score to compute the loss and make a prediction).

## The "anti-conspiracy" intuition (Slide 23) — genuinely worth quoting

Hinton's own bank-teller anecdote, given verbatim in the slide, is a fun and genuinely useful mnemonic: tellers got moved around regularly so they couldn't *collude* to defraud the bank — likewise, **randomly removing a different subset of neurons on each training example prevents "conspiracies" among neurons** (groups of units that only work well by relying heavily and specifically on each other's exact co-presence), thereby **reducing overfitting**.

**The deeper statement of the mechanism**: *"each hidden unit must be able to perform well regardless of which other hidden units are in the model"* — dropout forces every unit to be independently, robustly useful in many different contexts/sub-networks, rather than allowing brittle, overly-specific co-dependencies to form between particular units.

**The disruptive-noise framing, with the nice concrete example given**: dropout applies disruptive noise even to deep hidden layers, which can **destroy selective information derived from the input** — the slide's example: a face-recognition network being forced to recognize a face correctly **even when the "has nose" feature gets dropped out**, forcing the network to learn **redundant, distributed representations** (multiple independent paths to the same correct answer) rather than over-relying on any single feature.

## The ensemble interpretation (Slide 24)

**Alternative way to think about dropout**: each randomly-sampled binary mask effectively defines a **different sub-network** ("model") — since a different mask is sampled on every training step, dropout is implicitly training a **huge ensemble** of different (but overlapping, weight-sharing) sub-networks simultaneously.

**Key difference from a normal ensemble, explicitly stated**: ordinarily, ensemble members are *separate* models with *independent* weights; in dropout, all these "sub-network models" **share weights** (they're all just different subsets of the same single underlying parameter vector). The slide further connects this to **bagging** (training many models on different random subsets of *data* — a concept covered later when discussing Random Forests) — dropout is framed as a *special form of bagging*, except the randomness is in which *units* (not which *data*) each sub-model sees.

**A subtle caveat the slide flags explicitly**: in this ensemble-of-subnetworks view, *"configurations without connections between input and output [are] highly unlikely in large models"* — i.e., you don't need to worry that a randomly-sampled mask might occasionally disconnect input from output entirely (cutting off all paths) — in a sufficiently large/wide network, the chance of *every* path being simultaneously severed is negligible.

## Dropout at test time — the core problem and two solutions (Slides 25–26)

**The problem stated precisely**: dropout makes the network's output **stochastic** at training time ($scores = f(x;\theta,m)$, depending on the randomly sampled mask $m$) — but at test time you want a single, **deterministic** prediction.

**The principled (but expensive) solution**: literally average the output over **all possible masks**, weighted by their probability:

$$f(x;\theta) = \mathbb{E}_m[f(x;\theta,m)] = \sum_{\text{all masks }m} p(m)\,f(x;\theta,m)$$

In practice this exact sum is intractable (exponentially many masks), so you'd **approximate** it by running the same test input through the network multiple times with different randomly-sampled masks and averaging the results — but this **slows down inference significantly** (multiple forward passes per test example).

**The faster, standard solution: weight scaling.** The slide derives this explicitly via a simple two-input linear neuron example: with $p=0.5$ (each of $x_1,x_2$ independently kept or dropped with equal probability), there are 4 equally likely mask outcomes (both kept, only $x_1$, only $x_2$, neither), and computing the expectation:

$$\mathbb{E}_m[a_{train}] = \frac14(w_1x_1+w_2x_2)+\frac14(w_1x_1)+\frac14(w_2x_2)+\frac14(0) = \frac12(w_1x_1+w_2x_2) = p\cdot a_{test}$$

where $a_{test}=w_1x_1+w_2x_2$ is the value computed with **no dropout at all**. **The clean result**: the expected value of the dropped-out activation during training equals **exactly $p$ times** the corresponding non-dropped activation — a remarkably simple linear relationship (exact for linear layers, used as a fast approximation even with nonlinearities present).

**Two equally valid ways to reconcile train/test, both explicitly given:**
1. **Rescale at test time** by $p$: $a_{test}=\mathbb{E}_m[a_{train}]$ — i.e., run the full (non-dropped) network at test time, but multiply its activations by $p$ to match what training "expected" on average.
2. **Rescale at training time** by $\frac1p$ ("inverted dropout"): $a_{test}=\mathbb{E}_m\big[\frac{a_{train}}{p}\big]$ — divide the *kept* activations by $p$ during training, so their expected value already matches the full, undropped test-time value exactly — meaning **test time requires zero modification**.

**Inverted dropout is preferred**, explicitly because it **leaves test time completely unchanged** (no extra step at inference, simpler deployment) — all the rescaling bookkeeping happens once, during training.

**Important caveat, explicitly flagged**: this weight-scaling equivalence is **exact only for linear layers** — but it's used as a fast, good-enough approximation even in the presence of nonlinearities (the alternative being the much slower full Monte-Carlo averaging over many masks).

## Where dropout is and isn't used in practice (Slide 30) — concrete architecture facts

- **AlexNet, VGG**: applied to **all but the last** FC layers.
- **Inception-ResNet-v2**: applied **between GlobalAveragePooling and the final FC layer** (concretely shown: keep probability 0.8, reducing a 1792-dim vector before the final classifier).
- **NOT used in ResNets and variants**: explicitly because of *"unclear interactions with BatchNorm"* (cited paper: "Understanding the Disharmony between Dropout and Batch Normalization by Variance Shift," CVPR 2019) — the two techniques can interact in ways that destabilize the variance statistics BatchNorm relies on, so architectures using heavy BatchNorm (like ResNet) typically skip dropout.
- **EfficientNet uses it again**, and **scales $p$ linearly from 0.2 to 0.5** as you move from the smallest variant (B0) to the largest (B7) — bigger models (more capacity, more overfitting risk) get stronger dropout.

---

# Part 8 — The general regularization template (Slide 28) — a unifying abstraction

This slide is conceptually important because it **retroactively unifies dropout and BatchNorm** under one template, and previews stochastic depth:

> **Training time: add randomness** — $scores=f(x;\theta,m)$ for some random mask/perturbation $m$.
> **Test time: average it out** (sometimes only approximately) — $f(x;\theta)=\sum_{\text{all }m}p(m)f(x;\theta,m)$.

**Worked example given directly: Batch Norm fits this exact template.** At training time, *"each activation is randomly influenced by other samples in the mini-batch"* (recall: batch statistics $\mu,v$ depend on which other samples happen to share the batch — that's the injected randomness/dependency). At test time, $\mu_j,v_j$ get **fixed** to the running averages accumulated during training, turning BN into a **deterministic linear operation**:

$$\hat a_j^{(i)} = \frac{a_j^{(i)}-\mu_j}{\sqrt{v_j+\epsilon}}$$

This is *exactly* the same "stochastic at train time, averaged/deterministic at test time" pattern as dropout — a genuinely useful unifying lens to bring to the exam: **dropout and batch norm, despite looking unrelated on the surface, share the identical "regularize via training-time randomness, average it out at test time" structural template.**

---

# Part 9 — Stochastic depth (Slide 29)

**Specifically designed for ResNet-like architectures** (recall from the architectures lecture: ResNet blocks compute $F(x)+x$, where $F$ is the convolutional path and $+x$ is the identity skip).

**Mechanism (training time): shrink depth randomly.** For each residual block $l$, with probability $1-p_l$, **drop the entire convolutional path** $F(x)$ for that block, keeping **only the identity skip connection** active — effectively making that block compute nothing but $x\to x$ for that particular forward pass, as if the block didn't exist at all (shrinking the network's *effective* depth for that pass).

**Survival probability decreases with depth:**

$$p_l = 1-\frac{l}{L}(1-p_L)$$

where $L$ is the total number of blocks, $l$ is the index of the current block, and $p_L$ is the survival probability of the *last* block. **What this formula means**: shallower blocks (small $l$, near the input) have **higher survival probability** (closer to 1, i.e. closer to "always keep"), while deeper blocks (large $l$, near the output) have **lower survival probability** — they get dropped more often. This makes intuitive sense in light of the ResNet-as-ensemble-of-paths idea from the architectures lecture: early blocks build foundational features that almost every effective path relies on, so they're rarely worth disabling, while late blocks contribute more "optional," incremental refinements that the network can more safely do without on any given pass.

**Test time: unmodified network** — unlike dropout (which needs the weight-scaling trick), stochastic depth simply **uses the full, complete network with every block active** at test time — no rescaling needed, since (per the slide's own template from Part 8) the residual identity-skip structure means "block missing" and "block present but contributing nothing extra" are smoothly compatible states, so the full network is already a sensible "average" behavior.

---

# Part 10 — Data augmentation (Slides 30–39)

## The general principle (Slide 30)

**Statistical motivation, stated plainly**: *"more data always reduces variance"* — if you can cheaply manufacture new, realistic, **label-preserving** training examples from existing ones, you get the generalization benefit of a larger dataset essentially for free.

**The defining criterion: any transformation that does not change the label.** The slide's own cautionary example is excellent: a horizontal flip of a bird photo is clearly fine (still a bird, same class) — but a **180° rotation of a handwritten digit** can be label-changing (a rotated "9" can look exactly like a "6", making "label: ?" the only honest answer) — this is the central judgment call every augmentation choice has to pass: **does this transformation plausibly preserve the ground-truth label, or could it secretly change what the correct answer is?**

## Multi-scale training (Slides 32) — used by VGG and inherited by ResNet

**Training procedure, step by step exactly as given:**
1. Pick a random $S$ in range $[S_{min},S_{max}]=[256,480]$.
2. **Isotropically** resize the training image so its **short side** equals $S$ (isotropic = same scale factor in both dimensions, preserving aspect ratio).
3. Sample a **random $224\times224$ crop** from that resized image.

**Why varying $S$ matters, the key insight**: when $S$ is close to 224 (the crop size), the random crop ends up capturing **roughly the whole image's content/statistics** (since there's not much room to "zoom into" a sub-region). When $S\gg224$ (much larger), the same $224\times224$ crop now corresponds to only a **small fraction** of the (much bigger) resized image — capturing **a small object, or just part of a larger object**. So varying $S$ effectively **augments scale** — exposing the network to objects appearing at many different relative sizes within the crop, which makes the trained model far more robust to scale variation at test time.

## FixRes (Slide 33) — a subtle, important follow-up problem

**The discovered discrepancy, stated precisely**: multi-scale training (and augmentation generally) creates a **systematic mismatch between the apparent object sizes the classifier sees during training vs. testing** — and counter-intuitively, *"a lower train resolution improves classification at test time"* in many setups, because of exactly this train/test scale-statistics mismatch (visualized in the slide as differing "object size" probability density functions for train vs. test).

**FixRes's fix, two parts exactly as listed:**
1. **Calibrate object sizes** by adjusting the crop size used at test time, to better match what the network effectively learned to expect from training.
2. **Adjust the statistics of global average pooling** by **fine-tuning** the classifier and the **last batch-norm layer before pooling** on *larger* crops — recall from the architectures/representations lectures that BatchNorm statistics ($\mu,v$ running averages) are sensitive to the actual data distribution seen; if test-time images effectively have a different "scale statistics" profile than training images, a brief fine-tuning pass at the *target* resolution recalibrates those stale BN statistics to match.

## Cutout / Random Erasing (Slide 34)

**Mechanism**: with some probability (the slide's example: 50%), **remove a random square region** of the input image (typically replaced with a constant gray/zero value), leaving the rest of the image untouched.

**The explicit, memorable framing**: this is literally **"Dropout of the input space"** — instead of randomly zeroing hidden *activations* (as dropout does), you randomly zero out a contiguous *region of the raw input image itself*.

**Why it helps, exactly as stated**: *"It forces the network to use a more diverse set of features, improving generalization."* If a network could otherwise get away with relying heavily on one especially-discriminative image region (e.g. always looking at the same characteristic patch), Cutout occasionally removes exactly that patch, forcing the network to **also** learn to use other, less obviously-discriminative parts of the image — directly mirroring dropout's "no single unit/feature should be a single point of failure" philosophy, just applied at the pixel/input level instead of the hidden-activation level.

## Mixup (Slides 35) — blending two entire examples

**Mechanism, step by step:**
1. Sample a random blend coefficient $\lambda$ from a $\text{Beta}(\alpha,\alpha)$ distribution, $\alpha\in(0,+\infty)$.
2. **Linearly interpolate both the input images AND the one-hot labels:**

$$x = \lambda\,x^{(i)} + (1-\lambda)\,x^{(j)} \qquad y = \lambda\,\mathbb{1}(y^{(i)}) + (1-\lambda)\,\mathbb{1}(y^{(j)})$$

**Crucial detail**: the **label** gets blended too, not just the image — a Mixup-augmented example with $\lambda=0.6$ between a "cat" and a "bird" image gets a *target* of $[0,\ 0.6,\ 0.4,\ 0,\ldots]$ (60% cat, 40% bird) — a genuinely **soft, partial-credit target**, conceptually similar in spirit to label smoothing but now derived from mixing two *different* real classes rather than uniform noise.

**Testing: unmodified input** — Mixup only ever touches the *training* data; test-time inputs and evaluation are completely standard.

**The Beta distribution's shape matters**, shown via two example plots: $\text{Beta}(0.5,0.5)$ is **U-shaped** (most mass near $\lambda=0$ or $\lambda=1$, i.e., mostly *mild* blends where one image dominates), while $\text{Beta}(0.2,0.2)$ is **even more U-shaped/extreme** (mass concentrated even closer to the two endpoints) — so $\alpha$ controls *how aggressively* the two images typically get mixed.

**Intuition for why this helps generalization, stated directly**: it *"forces the network to act linearly in between classes and have smoother transitions from one class decision boundary to another."* Rather than learning an arbitrarily sharp, possibly brittle decision boundary right at the edge between two classes, Mixup explicitly trains the network on **interpolated** points between classes with correspondingly interpolated targets — encouraging smoother, more gradual confidence transitions across class boundaries, which tends to generalize better and also improves calibration.

## CutMix (Slide 36) — combining Cutout's spatial cut-and-paste with Mixup's label blending

**Mechanism, step by step:**
1. Sample $\lambda\sim\text{Beta}(\alpha,\alpha)$, same as Mixup.
2. **Sample a rectangular region** and build a binary mask $M$ (0 inside the region, 1 outside), with the region's dimensions set so that the **fraction of image area it covers equals exactly $(1-\lambda)$**:

$$r_x\sim U(0,W),\quad r_y\sim U(0,H),\quad r_w=W\sqrt{1-\lambda},\quad r_h=H\sqrt{1-\lambda}$$

(verify: area ratio $=\frac{r_wr_h}{WH}=\frac{W\sqrt{1-\lambda}\cdot H\sqrt{1-\lambda}}{WH}=1-\lambda$ ✓ — exactly as the slide states.)

3. **Paste** a patch from image $j$ into that masked rectangular region of image $i$ (rather than blending pixel intensities everywhere, as Mixup does), and blend the **labels** using the same $\lambda$/$(1-\lambda)$ split as the area ratio:

$$x = M\odot x^{(i)} + (1-M)\odot x^{(j)} \qquad y = \lambda\,\mathbb{1}(y^{(i)}) + (1-\lambda)\,\mathbb{1}(y^{(j)})$$

(where $\odot$ denotes elementwise multiplication — the mask selects, pixel by pixel, which source image contributes to each location.)

**The key conceptual difference from Mixup, worth stating directly**: Mixup produces a **globally blurred, alpha-blended** combination of two full images (every pixel is a weighted average of both); CutMix produces an image that's **sharp and locally coherent everywhere** — each individual pixel comes cleanly from *one* of the two source images, only the **spatial region boundary** differs between the two source images. This is *why* the paper's title emphasizes "Localizable Features" — because each region of the resulting image is an authentic, undistorted crop of a real image, the network is pushed to learn features that remain meaningful and **spatially localized** (useful for tasks like weakly-supervised localization too), rather than features that only make sense on globally-blended, somewhat unnatural-looking blended images as in Mixup.

**Testing: unmodified input**, identical to Mixup.

---

# Part 11 — Hyperparameter search (Slide 37)

## Grid search vs random search

**Grid search**: for each hyperparameter, pick a fixed discrete set of candidate values (the slide's example: $lr\in\{10^{-5},10^{-4},10^{-3},10^{-2}\}$, $wd\in\{10^{-5},10^{-4},10^{-3},10^{-2}\}$), and **train one model for every combination** in the full Cartesian product grid.

**Random search**: instead, **sample** each hyperparameter independently from a continuous distribution (the slide's example: $lr$ from $10^{U[-5,-2]}$, i.e. uniform in *log-space* between $10^{-5}$ and $10^{-2}$; similarly for $wd$), and train a model for each randomly-sampled combination.

## Why random search is generally more efficient (the visual argument, Bergstra & Bengio 2012)

The diagram contrasts two grids of 9 trials each, varying an **"important" parameter** (horizontal axis, genuinely affects performance — shown as a peaked green curve) and an **"unimportant" parameter** (vertical axis, barely affects performance — flat green curve along that axis). 

- In a **grid layout**, the 9 trials only ever explore **3 distinct values** of the important parameter (since the same 3 values get repeated across all 3 rows of the unimportant parameter) — most of your trial budget is "wasted" testing redundant settings of the unimportant parameter at the same few important-parameter values.
- In a **random layout**, the same 9 trials explore **9 distinct values** of the important parameter — every single trial contributes new information about the dimension that actually matters.

**Stated conclusion**: random search *"leads to a more efficient exploration of the space"* — but with an explicit caveat: *"beware of the curse of dimensionality!"* — as the number of hyperparameters grows, even random sampling needs exponentially many trials to adequately cover the space, so this efficiency advantage, while real, doesn't fully escape the broader difficulty of high-dimensional hyperparameter search.

---

# Part 12 — Test-time tricks: ensembles and EMA (Slides 38–39)

## Ensembles (Slide 38)

**Procedure**: train **multiple independently, randomly-initialized models** on the same dataset; at test time, run each model on the test image and **average their outputs** (e.g., average the logits, *then* take the argmax of the averaged result).

**Why it works, stated directly**: *"even if networks have similar error rates, they tend to make different mistakes."* Since each model's errors stem partly from its own particular random initialization and particular noisy training trajectory, those errors are **not perfectly correlated** across different models — averaging cancels out a good portion of each individual model's idiosyncratic mistakes, in a way directly analogous to how averaging noisy pixel measurements canceled noise in the very first denoising lecture you studied.

**Empirical benefit, given precisely**: typically **+1–2%** accuracy improvement.

**Two explicit downsides:**
1. You have to **train many networks from scratch** — multiplies training cost.
2. You have to **run many networks at test time** — multiplies inference cost/latency.

## Exponential Moving Average / Polyak averaging (Slide 39) — a cheaper alternative

**The motivation, stated directly**: *"to avoid building and running a costly ensemble, we can average snapshots in weight space"* instead of averaging the *outputs* of multiple fully-separate networks.

**Mechanism**: maintain **two** parameter vectors throughout training:
- $\theta$: the **normal training parameter vector**, updated by ordinary SGD as usual: $\theta^{(i+1)}=\theta^{(i)}-lr\,\nabla_\theta L(\theta;D^{train})$.
- $\theta^{(test)}$: a **separate vector used only at test/inference time**, updated periodically (every $k$ steps) via an exponential moving average of the training vector:

$$\theta^{(test)} = (1-\rho)\,\theta^{(i+1)} + \rho\,\theta^{(test)}, \qquad \rho\in[0,1] \text{ (usually very large, e.g. close to 1)}$$

**Why a *large* $\rho$**: since $\rho$ is the weight given to the **previous** $\theta^{(test)}$ value (and $(1-\rho)$ the weight given to the *latest* raw training snapshot), a large $\rho$ means $\theta^{(test)}$ changes only **slowly**, smoothly blending in many past snapshots of $\theta$ rather than just reflecting the most recent (possibly noisy) one. This produces a parameter vector that's effectively an **average over many recent points along the SGD trajectory** — and since SGD trajectories tend to bounce around noisily near a good solution rather than settling perfectly, averaging multiple nearby points along that trajectory tends to land closer to the true underlying minimum than any single noisy snapshot, similar in spirit to why averaging the (noisy) loss curve shown in the slide's plot gives a much smoother trend than any single training step's value.

**Why this is so much cheaper than a true ensemble**: you only ever train **one** network (not many), and at test time you only run **one** forward pass (using $\theta^{(test)}$) — all the benefit of "smoothing out noise via averaging" is captured in *weight space* during a single training run, rather than requiring multiple separately-trained models and multiple separate forward passes at test time.

---

# Part 13 — The practical training recipe (Slides 40–42)

## Karpathy's six-step recipe (Slide 40) — likely to be asked to reproduce in order

The slide opens with a genuinely good quote worth remembering in spirit: getting a neural network to work well involves real "suffering," but it's manageable through being **thorough, defensive, paranoid, and obsessed with visualizing basically everything** — with **patience and attention to detail** as the two qualities correlating most strongly with success.

**The six steps, in order:**

1. **"Become one with the data"**: don't just collect summary statistics — actually *look* at individual examples, understand what's genuinely relevant/predictive in the data before writing any model code.
2. **Set up the end-to-end training/evaluation skeleton + get dumb baselines**: verify *all* the infrastructure works correctly **before** attempting anything complex — check the initial loss value is sane, deliberately try to **overfit a tiny subset** of the data (a sanity check that the model/training loop is even *capable* of learning anything at all) before trusting results on the full dataset.
3. **Overfit**: aim first for **low bias** — start with a known-good model architecture + a robust default optimizer (Adam), get the model to fit the training data well, *then* explore further from there.
4. **Regularize**: only *after* you have a model that can overfit, apply the regularization toolkit from this entire lecture — data augmentation, norm penalties, dropout, stochastic depth, CutMix, etc. — to close the generalization gap.
5. **Tune**: use **random search** for hyperparameters, searching *around* what already worked in steps 3–4 (not from scratch blindly), and bring in **LR schedules**.
6. **Test-time optimizations**: ensembles and/or **distillation** (a technique not covered in depth in this lecture, but named as a closing option).

**The crucial ordering logic embedded here, worth stating in your own words on an exam**: you deliberately **overfit first, regularize second** — this is a debugging strategy, not just a training strategy. If you jump straight to a heavily-regularized setup and get poor results, you can't tell whether the problem is your model/data pipeline being broken, or the regularization being miscalibrated. By first confirming the model *can* overfit (proving the model and pipeline genuinely work), any remaining generalization gap you see afterward can be confidently attributed to a *capacity/regularization* issue, not a bug.

## Real-world case study: PyTorch's 2021 ResNet50 recipe refresh (Slides 41–42)

The slide shows a **cumulative accuracy improvement chart** for ResNet50, stacking up the gain from each individual technique applied **in sequence**, starting from the original TorchVision recipe: LR optimizations (value + warmup + cosine schedule) → TrivialAugment → longer training → random erasing → label smoothing → mixup → cutmix → weight decay tuning (value + **no decay applied to BatchNorm parameters specifically**) → FixRes mitigations → EMA → inference-time resize adjustments — together compounding to roughly **+4–5 percentage points** of top-1 accuracy improvement, **using the exact same architecture** the whole time.

**An important honesty caveat the blog post itself makes, quoted directly in the slide**: this "idealized linear journey" is explicitly **an oversimplification** — real model development *"is not a journey of monotonically increasing accuracies and the process involves a lot of backtracking."* The clean, neatly-ordered bar chart is a retrospective narrative imposed for clarity, not a literal record of the actual (messier) experimentation process.

**The single biggest practical takeaway from this entire final section, and arguably of the whole lecture**: shown again on Slide 42 across **many different architectures** (EfficientNet, MobileNet, ResNet variants, RegNet, Wide ResNet, etc.) — for every single architecture, the **"New API" recipe consistently and substantially outperforms the "Old API" recipe**, even though **the architecture itself never changed**. This is the lecture's closing thesis made completely concrete: **the training recipe — learning rate schedule, regularization choices, data augmentation, and all the other techniques covered in this lecture — can matter as much as, or more than, the architecture itself.**

---

## Quick self-test checklist for this lecture

1. Draw/describe the generalization-error-vs-capacity curve, define underfitting/overfitting, and work through the degree-$K$ polynomial example showing which $K$ underfits, fits well, and overfits.
2. Define theoretical vs. effective capacity, and give concrete examples of hyperparameters/techniques that move effective capacity without touching theoretical capacity.
3. Explain why a single fixed learning rate is hard to choose well, and describe each schedule (step, cosine, warm-up, one-cycle) — what problem each solves and its exact formula.
4. Explain the "wide vs narrow minima" argument for why LR schedules can improve generalization, not just speed.
5. State the exact regularization definition (reduce test error, not necessarily train error) and connect it to the "shifted optimal capacity" picture.
6. Derive the weight-decay equivalence for $l_2$ regularization + plain SGD from scratch, and explain why this is called weight decay.
7. Explain early stopping as a form of selecting the "#updates" hyperparameter via validation performance.
8. Derive why one-hot cross-entropy pushes scores toward infinity, define the label-smoothing target precisely, and walk through the cross-entropy → KL-divergence reformulation explaining why direction (not commutative) matters.
9. Explain dropout's training-time mechanism, the "anti-conspiracy"/ensemble interpretations, and derive the weight-scaling/inverted-dropout equivalence at test time from the worked 2-neuron example. Know where it is and isn't used in real architectures and why (BatchNorm interaction).
10. State the general "add randomness at train time, average it out at test time" regularization template, and explain how both dropout and BatchNorm are instances of it.
11. Explain stochastic depth's mechanism, the depth-dependent survival probability formula, and why test time needs no rescaling (unlike dropout).
12. List and explain every data augmentation technique: basic label-preserving transforms, multi-scale training (and why varying S matters), FixRes's fix for the resulting train/test mismatch, Cutout ("dropout of the input"), Mixup (full derivation of x and y blending, Beta distribution shape), and CutMix (region-based variant, and how it differs conceptually from Mixup).
13. Compare grid search vs. random search and explain, using the important/unimportant parameter argument, why random search explores more efficiently.
14. Explain ensembling's benefit and cost, then explain EMA/Polyak averaging as a cheaper alternative achieving a similar effect in weight space rather than output space.
15. Reproduce Karpathy's 6-step recipe in order, and explain the "overfit first, then regularize" debugging logic.

Want me to combine this lecture with the earlier architectures lecture into one consolidated "Part 2 of the course" study guide, since they clearly build on each other (this lecture's techniques are exactly what's used to actually train the AlexNet/VGG/ResNet architectures from before)?
