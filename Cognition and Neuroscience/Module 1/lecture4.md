# Detailed Lecture Notes: Introduction to Animal Reinforcement Learning

These notes integrate the lecture **“Introduction to Animal Reinforcement Learning”**, Daw and O’Doherty’s chapter on **multiple systems for value learning**, and Lee and Seymour’s article on **decision-making in brains and robots**.   

---

## 1. Reinforcement learning and decision-making

### Optimal decision-making

Optimal decision-making involves selecting actions that:

* maximize rewards;
* minimize punishments or costs;
* produce the greatest expected long-term benefit.

This is not simply a matter of reacting to an immediately available reward. A decision-maker must:

1. represent the available alternatives;
2. assign a value or utility to each alternative;
3. compare those values;
4. select the alternative with the highest subjective value;
5. predict the possible future consequences of the choice.

The term **subjective value** is important because the value of an outcome depends on the organism’s current needs, preferences, internal state, and previous experience. Food, for example, has greater value when an animal is hungry than when it is full.

### Why optimal decision-making is difficult

Outcomes are often:

* uncertain;
* delayed;
* dependent on a sequence of actions;
* influenced by environmental changes;
* affected by other choices made before or after the current action.

For example, the success of a chess move may only become apparent many moves later. The organism must determine which earlier action contributed to the eventual success or failure.

### The credit-assignment problem

The **credit-assignment problem** is the difficulty of determining which earlier states, actions, or decisions were responsible for a later reward or punishment.

It is difficult when:

* the outcome is delayed;
* many actions occur before the outcome;
* several environmental events could have contributed;
* the same action can have different effects in different contexts.

Many real-world decisions can be represented as **Markov decision processes**, involving sequences of states and actions before an important outcome. Reinforcement-learning mechanisms address this problem by updating predictions about earlier states and actions based on later outcomes.  

---

# 2. Basic forms of learning

## Definition of learning

**Learning** is an enduring change in behavior or response that occurs as a result of experience.

A temporary change caused by fatigue, illness, drugs, or immediate motivation would not ordinarily count as learning unless it produces a relatively stable modification.

## Non-associative learning

In **non-associative learning**, the organism learns about the properties of a single stimulus. It does not have to form an association between two stimuli or between an action and an outcome.

### Habituation

**Habituation** is a decrease in an innate response following repeated exposure to a stimulus.

Example:

* A person initially notices the sound of a nearby clock.
* With repeated exposure, the response decreases.
* The stimulus is judged to be harmless or unimportant.

Habituation allows attention and energy to be directed toward novel or significant events.

### Sensitization

**Sensitization** is an increase in responsiveness following repeated or intense stimulation.

Example:

* After hearing a frightening sound, a person may become unusually responsive to later noises.
* Following a painful event, even mild stimulation may produce an exaggerated response.

Sensitization increases vigilance when the environment may be dangerous.

## Associative learning

In **associative learning**, the organism learns a relationship:

* between two stimuli; or
* between a behavior and its consequence.

The two main forms are:

1. **Pavlovian or classical conditioning**: stimulus–outcome learning;
2. **instrumental or operant conditioning**: action–outcome learning.

---

# 3. Reinforcement learning

## Definition

**Reinforcement learning (RL)** is learning through interaction with the environment, in which actions are modified according to their rewarding or punishing consequences.

Its goal is to learn a policy for choosing actions that maximizes expected future reward or minimizes expected future cost.

An RL system typically includes:

* an **agent**: the organism or decision-maker;
* an **environment**;
* **states**: situations in which the agent may find itself;
* **actions**: available behavioral choices;
* **outcomes**;
* **rewards or punishments**;
* **values**: predictions of future outcomes;
* a **policy**: a rule for selecting actions.

RL differs from simple supervised learning because the agent is not always told the correct response. It must discover useful actions through trial and error.

## Reinforcers

A **reinforcer** is an outcome that increases the future probability of a behavior.

### Primary reinforcers

Primary reinforcers have intrinsic biological significance and do not require learning.

Examples include:

* food;
* water;
* warmth;
* relief from pain;
* sexual reward.

They are closely related to survival, physiological regulation, and reproduction.

### Secondary or conditioned reinforcers

Secondary reinforcers acquire value through association with primary reinforcers or other established rewards.

Examples include:

* money;
* grades;
* praise;
* tokens;
* status symbols.

Money has no direct nutritional value, but it acquires reinforcing power because it predicts access to many other rewards.

---

# 4. Multiple systems control behavior

A major theme of the lecture and Daw and O’Doherty chapter is that behavior is not controlled by a single, unitary decision system.

The same observable action may be produced by different psychological and neural mechanisms. A rat pressing a lever, for example, might do so because:

* the lever predicts food and automatically attracts approach;
* lever pressing was reinforced in the past and has become habitual;
* the rat expects that pressing will produce a currently desired food outcome.

The three major learning systems are:

1. the **Pavlovian system**;
2. the **habitual system**;
3. the **goal-directed system**.  

| System        | Learns                                            | Main function                                             | Typical behavior                               |
| ------------- | ------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------- |
| Pavlovian     | Stimulus–outcome association                      | Predict significant events and trigger prepared responses | Salivating to a food cue                       |
| Habitual      | Stimulus–response or cached action value          | Repeat actions that were rewarded previously              | Automatically taking a familiar route          |
| Goal-directed | Action–outcome relation and current outcome value | Select actions according to expected consequences         | Choosing a new route when circumstances change |

These systems operate in parallel and may cooperate or compete.

---

# 5. Reflexes as a foundation for behavioral control

A **reflex** is an innate, stereotyped response automatically triggered by a particular stimulus.

Examples include:

* withdrawing a hand from a hot surface;
* startling in response to a loud sound;
* salivating when food enters the mouth.

Reflexes are:

* rapid;
* automatic;
* present without lifetime learning;
* shaped by evolutionary history;
* relatively inflexible.

Their advantage is computational simplicity. Sensory input can be linked relatively directly to an appropriate response.

Their limitation is that they are mainly **reactive**. The organism responds only after the important event has occurred.

Pavlovian learning improves on reflexes by allowing an organism to respond in anticipation of an important event.

---

# 6. Pavlovian conditioning

## Definition

**Pavlovian conditioning**, also called **classical conditioning**, is learning that one stimulus predicts another biologically significant event.

The system learns a **stimulus–outcome association**.

It allows an organism to prepare for rewards, dangers, or other important events before they occur.

## Basic terminology

### Before conditioning

* **Unconditioned stimulus (US):** naturally produces a response.
* **Unconditioned response (UR):** innate response to the US.
* **Neutral stimulus (NS):** initially does not produce the relevant response.

Example:

* food = US;
* salivation to food = UR;
* bell before conditioning = NS.

### During conditioning

The neutral stimulus is repeatedly presented before or with the US:

**bell → food**

### After conditioning

The previously neutral stimulus becomes a:

* **conditioned stimulus (CS)**;
* it now produces a **conditioned response (CR)**.

Thus:

**bell alone → salivation**

The conditioned response is learned because the bell predicts food.

## Predictive nature of Pavlovian learning

Pavlovian learning does not merely join two events because they occur together. The CS must provide useful information about the occurrence of the US.

A conditioned response often prepares the organism for the expected outcome.

Examples:

* salivation prepares the digestive system for food;
* fear prepares the organism to escape danger;
* approach prepares the organism to obtain reward;
* withdrawal prepares the organism to avoid injury.

The conditioned response need not be identical to the unconditioned response. A cue predicting food may produce orientation or approach, whereas food itself produces chewing and ingestion.

## Pavlovian behavior is not instrumental behavior

In Pavlovian conditioning, the organism learns:

**stimulus → outcome**

It does not necessarily learn that its own response causes the outcome.

A revealing experiment can make food delivery occur only when the animal does **not** salivate. Even though salivation prevents reward, the animal may still salivate when the conditioned stimulus is presented. This demonstrates that the response is controlled by the learned predictive relationship between the stimulus and food rather than by the consequences of salivation itself. 

---

# 7. Processes in Pavlovian conditioning

## Acquisition

**Acquisition** is the stage during which the CS–US relationship is learned and the conditioned response gradually develops.

Important factors include:

* repeated pairings;
* temporal order;
* the CS normally preceding the US;
* the reliability or contingency of the CS;
* stimulus salience;
* the organism’s prior learning.

A CS is learned more effectively when it reliably predicts whether the US will occur.

## Extinction

**Extinction** occurs when the CS is repeatedly presented without the US, causing the conditioned response to decrease.

For example:

* bell repeatedly occurs without food;
* salivation gradually declines.

Extinction is usually not complete erasure of the original association. Instead, the organism appears to learn a new relationship:

**CS → no US**

This explains why an extinguished response can return.

## Spontaneous recovery

After extinction and a delay, the conditioned response may temporarily reappear. This is **spontaneous recovery**.

It demonstrates that the original CS–US association was suppressed rather than entirely eliminated.

## Renewal

An extinguished response may return when the organism is tested outside the context in which extinction occurred.

This shows that extinction learning is often context-dependent.

## Reinstatement

Following extinction, unsignaled presentations of the US may cause the CR to return when the CS is presented again.

## Generalization

**Stimulus generalization** occurs when stimuli resembling the original CS also elicit the conditioned response.

Example:

* a person bitten by one dog may initially fear many dogs.

Generalization is adaptive because organisms do not have to relearn every minor variation of a potentially important stimulus.

Excessive generalization, however, may contribute to anxiety disorders.

## Discrimination

**Discrimination** is learning to respond differently to similar stimuli depending on which one predicts the outcome.

Example:

* one tone predicts shock;
* a slightly different tone predicts safety;
* fear becomes specific to the shock-predicting tone.

Generalization supports broad protection; discrimination prevents unnecessary responses.

---

# 8. Instrumental or operant conditioning

## Definition

**Instrumental conditioning**, also called **operant conditioning**, is learning in which behavior is modified by its consequences.

The critical relationship is:

**action → outcome**

The organism learns that performing a particular action produces a reward, prevents a punishment, causes an unpleasant event, or removes access to something desirable.

Instrumental behavior is more flexible than a Pavlovian reflex because the organism selects an action to influence the environment.

## Thorndike’s Law of Effect

Thorndike proposed that:

* responses followed by satisfying consequences become more likely;
* responses followed by discomfort or unsatisfying consequences become less likely.

This became known as the **Law of Effect**.

Thorndike’s work suggested that consequences strengthen or weaken associations between situations and responses.

## Skinner and operant behavior

Skinner developed systematic methods for studying how reinforcement and punishment affect behavior.

In a typical operant chamber:

* an animal performs an action, such as pressing a lever;
* the action produces an outcome;
* the frequency of the response is measured;
* reinforcement schedules can be precisely controlled.

---

# 9. Reinforcement and punishment

The terms positive and negative refer to whether something is **added** or **removed**, not whether it is morally good or bad.

## Positive reinforcement

A desirable stimulus is added after a behavior, increasing that behavior.

Example:

* a student studies;
* receives praise or a high grade;
* studying becomes more likely.

## Negative reinforcement

An aversive stimulus is removed or prevented after a behavior, increasing that behavior.

Example:

* fastening a seatbelt stops an unpleasant warning sound;
* seatbelt fastening becomes more likely.

Negative reinforcement is not punishment. It strengthens behavior.

## Positive punishment

An aversive event is added following a behavior, decreasing that behavior.

Example:

* touching a hot object produces pain;
* touching it becomes less likely.

## Negative punishment

A desirable event is removed following a behavior, decreasing that behavior.

Example:

* a child loses access to a game following misconduct;
* the misconduct becomes less likely.

| Consequence       | Add stimulus           | Remove stimulus        |
| ----------------- | ---------------------- | ---------------------- |
| Increase behavior | Positive reinforcement | Negative reinforcement |
| Decrease behavior | Positive punishment    | Negative punishment    |

## Problems with punishment

Punishment may suppress behavior without teaching an appropriate alternative. It may also produce:

* fear;
* avoidance;
* aggression;
* context-specific suppression;
* attempts to avoid the punishing person rather than the behavior.

Reinforcement of an alternative response may therefore produce more durable learning.

---

# 10. Reinforcement schedules

A **reinforcement schedule** specifies when a response will be reinforced.

## Continuous reinforcement

Every occurrence of the desired behavior is reinforced.

Advantages:

* rapid acquisition;
* clear action–outcome relationship;
* useful for teaching new behavior.

Disadvantage:

* rapid extinction once reinforcement stops.

## Partial or intermittent reinforcement

Only some responses are reinforced.

Advantages:

* greater resistance to extinction;
* can maintain behavior over long periods.

Partial schedules may be based on:

* the number of responses: **ratio**;
* the passage of time: **interval**;
* a predictable requirement: **fixed**;
* a changing requirement: **variable**.

## Fixed-ratio schedule

Reinforcement follows a fixed number of responses.

Example:

* reward after every tenth response.

Typical pattern:

* high response rate;
* pause after reinforcement.

## Variable-ratio schedule

Reinforcement follows an unpredictable number of responses around an average.

Example:

* gambling or slot machines.

Typical pattern:

* very high, persistent response rate;
* strong resistance to extinction.

## Fixed-interval schedule

The first response after a fixed period is reinforced.

Example:

* studying increases as a scheduled examination approaches.

Typical pattern:

* low responding immediately after reinforcement;
* responding accelerates near the expected time.

## Variable-interval schedule

The first response after a varying and unpredictable interval is reinforced.

Example:

* checking for a message that could arrive at any time.

Typical pattern:

* steady, moderate response rate;
* resistance to extinction.

---

# 11. Habits and goal-directed actions

Instrumental behavior can be produced by two different systems.

## Habitual system

The habitual system learns to repeat actions that were successful in the past.

It can be described as:

* stimulus–response learning;
* retrospective;
* based on previous reinforcement;
* relatively computationally cheap;
* fast and automatic;
* insensitive to the current value of the outcome.

Example:

* automatically taking the usual route home even when intending to stop elsewhere.

Habits can be highly adaptive because they free cognitive resources and allow frequently repeated behavior to be performed efficiently.

However, they may become maladaptive when circumstances change.

## Goal-directed system

The goal-directed system selects actions on the basis of:

1. the **action–outcome contingency**;
2. the current value of the expected outcome.

It is:

* prospective;
* flexible;
* sensitive to changes in outcome value;
* capable of planning;
* computationally demanding.

Example:

* deciding not to buy food that is normally enjoyable after becoming ill from it.

A goal-directed action is chosen because the organism represents what the action will produce and currently wants that consequence.

---

# 12. Tolman, cognitive maps, and latent learning

Tolman challenged the claim that all instrumental learning consists of stimulus–response habits.

## Latent learning

Rats allowed to explore a maze without reward later learned to reach a rewarded location faster than rats without prior exposure.

This implies that learning occurred even without immediate reinforcement.

The rats appeared to acquire a representation of the maze’s structure.

## Cognitive maps

Tolman proposed that animals form **cognitive maps**: internal representations of relationships between places, states, actions, and outcomes.

These maps allow:

* flexible detours;
* shortcuts;
* planning;
* transfer of knowledge;
* navigation after environmental changes.

A cognitive map is more general than a literal spatial map. It can refer to a model of how states and actions lead to outcomes in any structured task. 

---

# 13. Outcome devaluation: distinguishing habits from goals

The most important behavioral test distinguishing habits from goal-directed actions is **outcome devaluation**.

## Procedure

1. A hungry rat learns to press a lever for food.
2. The value of the food is reduced:

   * the animal is fed to satiety; or
   * the food is paired with illness.
3. The rat is tested with the lever, often without receiving the food.

## Goal-directed prediction

A goal-directed animal represents:

* pressing → food;
* food is now undesirable.

Therefore, it reduces lever pressing.

## Habitual prediction

A habitual system represents a strengthened link between the situation and the lever-press response.

Because the response was rewarded previously, it continues even though the food is now devalued.

## Role of training

Moderate training tends to produce goal-directed behavior.

Extended or overtraining tends to shift control toward habitual behavior.

This is not because goal-directed knowledge necessarily disappears. Rather, the habitual system may increasingly dominate action selection.

---

# 14. Model-free and model-based reinforcement learning

The psychological distinction between habit and goal-directed control has a computational counterpart.

## Model-free learning

Model-free learning acquires values directly from experience without representing the detailed structure of the environment.

It learns a cached value such as:

* how good a state is;
* how rewarding an action has previously been in a state.

Properties:

* similar to habitual control;
* computationally efficient at choice time;
* slow to adapt when outcomes or transition structures change;
* requires direct experience to update values;
* can produce perseveration.

## Model-based learning

Model-based learning maintains an internal model of:

* state transitions;
* action–outcome relationships;
* likely consequences;
* current reward values.

The system can mentally simulate possible futures.

Properties:

* similar to goal-directed control;
* flexible;
* sensitive to outcome devaluation;
* supports planning and novel choices;
* computationally expensive;
* vulnerable to errors if the internal model is inaccurate.

## Why maintain two systems?

No single system is optimal under all conditions.

Model-based control is flexible but costly in:

* time;
* attention;
* memory;
* computational effort.

Model-free control is efficient but inflexible.

The brain may therefore arbitrate between them according to:

* available time;
* task complexity;
* uncertainty;
* reliability;
* cognitive resources;
* amount of training;
* stress or fatigue.

The division of labor may be worthwhile overall even though it occasionally produces costly habitual errors. 

---

# 15. Values and prediction errors

## State value

A **state value**, often written (V(s)), estimates the expected future reward associated with being in a particular state.

It is especially relevant to Pavlovian prediction because it represents the value of a situation or stimulus independently of one specific selected action.

## Action value

An **action value**, often written (Q(s,a)), estimates the expected future reward from taking action (a) in state (s).

This is especially relevant to instrumental choice.

## Reward-prediction error

A **reward-prediction error** is the difference between:

* the reward that was obtained or newly predicted;
* the reward that was expected.

Conceptually:

**prediction error = actual or updated outcome − expected outcome**

### Positive prediction error

The outcome is better than expected.

Example:

* an unexpected reward occurs.

The value of preceding stimuli or actions should increase.

### Zero prediction error

The outcome matches the prediction.

Little new learning is required.

### Negative prediction error

The outcome is worse than expected or an expected reward is omitted.

The value of preceding stimuli or actions should decrease.

Prediction errors solve part of the credit-assignment problem by propagating information backward to earlier states and actions. 

---

# 16. Temporal-difference learning

**Temporal-difference learning** updates predictions by comparing estimates at successive moments.

The agent does not have to wait until the final reward to begin learning. A later predictive cue can train an earlier cue.

Example:

1. Food initially produces a positive prediction error.
2. A tone repeatedly predicts food.
3. The prediction error transfers from the food to the tone.
4. Once food is fully predicted, food itself produces little prediction error.
5. If the predicted food is omitted, a negative prediction error occurs at the expected time.

This helps explain **second-order conditioning**, in which one conditioned stimulus gains value through association with another conditioned stimulus rather than direct pairing with the original unconditioned stimulus.

Temporal-difference learning developed partly from animal-conditioning research and later became central to both neuroscience and AI. 

---

# 17. Neural systems for value learning

The three behavioral systems involve partially dissociable cortico-basal-ganglia circuits.

## Summary

| Learning system | Main striatal region                       | Associated cortical/limbic regions       |
| --------------- | ------------------------------------------ | ---------------------------------------- |
| Pavlovian       | Ventral striatum                           | Amygdala, orbitofrontal cortex           |
| Habitual        | Dorsolateral striatum; putamen in primates | Sensorimotor cortex                      |
| Goal-directed   | Dorsomedial striatum; caudate in primates  | Medial prefrontal and associative cortex |

All three circuits receive dopaminergic input from the ventral tegmental area and substantia nigra pars compacta.  

---

## Pavlovian neural system

Major structures include:

* amygdala;
* ventral striatum;
* orbitofrontal cortex;
* hypothalamic and brainstem output systems.

### Amygdala

The amygdala is involved in learning and expressing associations between stimuli and biologically important outcomes.

Its subregions contribute differently:

* basolateral amygdala helps represent sensory-specific and value-related properties of outcomes;
* central amygdala contributes to expression of autonomic and defensive responses.

The central amygdala projects to hypothalamic and brainstem regions capable of producing conditioned autonomic responses.

### Ventral striatum

The ventral striatum contributes to:

* conditioned approach;
* avoidance;
* motivational invigoration;
* translating Pavlovian predictions into behavior.

### Orbitofrontal cortex

The orbitofrontal cortex represents:

* expected outcomes;
* changing reward values;
* sensory-specific properties of outcomes.

Neural recordings and imaging show that amygdala, orbitofrontal cortex, and ventral striatum respond to cues predicting rewarding and aversive events.  

---

## Habitual neural system

Habitual behavior depends especially on the **dorsolateral striatum** in rodents, corresponding approximately to the **putamen** in primates.

This region interacts strongly with sensorimotor cortex.

Evidence includes:

* damage to dorsolateral striatum prevents normal habit formation;
* animals may remain sensitive to outcome devaluation even after overtraining;
* activity shifts toward sensorimotor striatal systems as actions become habitual.

The circuit supports efficient repetition of well-trained responses.

---

## Goal-directed neural system

Goal-directed behavior depends especially on:

* dorsomedial striatum in rodents;
* caudate in primates;
* medial prefrontal cortex;
* orbitofrontal regions;
* possibly hippocampal contributions when relational or spatial models are required.

Damage to goal-directed circuitry can make behavior less sensitive to:

* outcome devaluation;
* changes in action–outcome contingency;
* new information about environmental structure.

The goal-directed system therefore supports prospective evaluation and flexible planning.

---

# 18. Dopamine and reinforcement learning

Midbrain dopamine neurons are located principally in:

* the ventral tegmental area;
* substantia nigra pars compacta.

They project to:

* ventral striatum;
* dorsal striatum;
* prefrontal cortex;
* other limbic and cortical targets.

## Dopamine as a prediction-error signal

Dopamine activity resembles a reward-prediction-error signal:

* unexpected reward → increased firing;
* fully predicted reward → little additional response at reward delivery;
* omitted expected reward → decreased firing at the expected time.

As learning progresses, the dopamine response shifts from the reward to the earliest reliable predictor of reward.

Dopamine influences plasticity in the striatum, allowing rewarded stimulus–action relationships to become stronger.

This does not mean dopamine is simply “pleasure.” Its role is more closely related to:

* learning;
* motivation;
* action invigoration;
* updating value predictions;
* selecting behavior.

The RL interpretation of dopamine has been one of the strongest links between computational theory and neural data. 

---

# 19. Interactions between the learning systems

The systems do not function independently. They may:

* cooperate;
* compete;
* bias one another;
* dominate under different circumstances.

## Habit–goal competition

A familiar action may be supported simultaneously by:

* a habit that automatically favors the response;
* a goal-directed calculation of its expected consequences.

Habits tend to dominate with:

* extensive repetition;
* time pressure;
* stress;
* reduced cognitive resources;
* stable environments.

Goal-directed control is favored by:

* changes in outcome value;
* changes in task structure;
* novelty;
* explicit planning;
* sufficient time and cognitive capacity.

Impaired balance may contribute to compulsive behavior, addiction, and obsessive-compulsive symptoms. Some findings suggest that compulsive disorders may involve overactive habits, weakened goal-directed control, or impaired arbitration between them. 

---

## Pavlovian–instrumental transfer

**Pavlovian-to-instrumental transfer (PIT)** occurs when a Pavlovian cue changes the vigor or selection of an independently learned instrumental action.

Example:

* a rat learns that a tone predicts food;
* separately, it learns to press a lever for food;
* later, the tone increases lever pressing.

PIT demonstrates that stimulus-based predictions can motivate instrumental action.

The amygdala and ventral striatum are important for this effect.

## Conditioned suppression

A cue predicting an aversive event may suppress an ongoing reward-seeking response.

Example:

* an animal presses for food;
* a cue predicting shock appears;
* lever pressing decreases.

## Choking under pressure

Very high incentives can sometimes disrupt skilled performance rather than improve it.

This may reflect maladaptive interactions between Pavlovian motivational responses and instrumental motor control.

## Conditioned reinforcement

A stimulus associated with reward can itself reinforce a new behavior, even when the original reward is not immediately present.

This is one mechanism through which secondary reinforcers acquire motivational power.

---

# 20. Advantages and disadvantages of multiple controllers

## Pavlovian system

**Advantages**

* rapid;
* evolutionarily prepared;
* anticipatory;
* protects against threats;
* prepares the body for significant outcomes.

**Limitations**

* responses are stereotyped;
* may conflict with current goals;
* can cause maladaptive avoidance or approach.

## Habitual system

**Advantages**

* fast;
* automatic;
* computationally inexpensive;
* useful for repeated actions;
* frees attention for other tasks.

**Limitations**

* insensitive to current outcome value;
* difficult to update;
* can contribute to compulsive or addictive behavior.

## Goal-directed system

**Advantages**

* flexible;
* sensitive to consequences;
* supports planning;
* adapts to new goals and environmental changes.

**Limitations**

* slow;
* cognitively demanding;
* dependent on an accurate model;
* may become overwhelmed in complex environments.

The existence of multiple systems is adaptive because different systems are efficient in different circumstances.

---

# 21. Reinforcement learning in neuroscience and robotics

Lee and Seymour argue that humans and autonomous robots face a similar general problem:

* they must act in changing and uncertain environments;
* satisfy needs;
* avoid damage;
* learn with limited prior information;
* make safe and efficient decisions over long periods.

Although neuroscience and robotics both use RL, they have developed largely separately. Cross-disciplinary exchange could improve both fields. 

---

# 22. Why decision neuroscience needs robotics

## 22.1 Learning in real environments

Many neuroscience models are tested in simplified laboratory tasks involving:

* discrete states;
* discrete actions;
* short durations;
* stable reward structures;
* low-dimensional input;
* controlled noise.

Real environments involve:

* continuous space and time;
* enormous state and action spaces;
* sensory noise;
* motor variability;
* changing body dynamics;
* long-term development;
* uncertain environmental conditions.

Robotics can test whether brain-inspired learning algorithms remain effective under realistic physical constraints.

### The reality gap

The **reality gap** refers to the failure of a system that performs well in simulation to work equally well in physical hardware.

Reasons include:

* friction;
* mechanical flexibility;
* sensor noise;
* actuator error;
* unpredictable environmental interactions.

Robotic testing prevents neuroscience theories from being accepted solely because they fit highly controlled experimental data.

## 22.2 Modeling complex disease

Computational psychiatry and neurology attempt to explain symptoms in terms of disrupted computations.

However, disorders may not result from one isolated deficit. They may involve a network of interacting computational abnormalities—a **computome**.

For example, chronic pain may involve combinations of:

* excessive pain-value predictions;
* low perceived controllability;
* impaired prediction of relief;
* negative perceptual expectations;
* overgeneralization of aversive learning.

Robotic or computational systems can test how multiple abnormalities interact to produce behavior. 

## 22.3 Evolutionary modeling

Neuroscience can describe how a system operates, but it must also explain why that architecture evolved.

Evolutionary robotics uses:

* artificial agents;
* fitness functions;
* selection over generations;
* changing environments.

This may help investigate:

* why multiple controllers evolved;
* why some stimuli have intrinsic value;
* why humans show impulsivity or compulsivity;
* how learning systems balance efficiency, flexibility, and safety.

---

# 23. Why robotics needs neuroscience

Lee and Seymour identify three major contributions from decision neuroscience to robotics.

## 23.1 Multiple-controller architectures

Biological systems use several parallel controllers:

* reflexive;
* Pavlovian;
* habitual;
* goal-directed.

Robots could benefit from a similar organization.

### Reflex controller

Provides immediate safety responses.

Example:

* rapidly avoiding collision without complex planning.

### Habitual controller

Produces efficient well-practiced responses.

Example:

* repeating a frequently successful movement sequence.

### Goal-directed controller

Plans when the environment changes.

Example:

* simulating several routes around an obstacle.

### Meta-controller

A higher-level system can decide which controller should govern behavior.

This balances:

* speed;
* accuracy;
* safety;
* computational cost;
* environmental uncertainty.

## 23.2 Rapid and single-shot learning

Many artificial RL systems require huge amounts of training.

Humans can sometimes learn from:

* one event;
* very few examples;
* episodic memory;
* verbal instruction;
* observation.

A robot with biologically inspired rapid learning could:

* adjust quickly in a new environment;
* reduce dangerous trial and error;
* transfer prior experience;
* improve human–robot interaction.

The hippocampus may inspire an **episodic controller**, which retrieves a single relevant past episode to guide current behavior. 

## 23.3 Metacognitive learning

**Metacognition** is the ability to evaluate one’s own cognitive processes.

It includes estimates of:

* confidence;
* uncertainty;
* competence;
* reliability of current predictions.

A metacognitive robot could:

* recognize when its model is uncertain;
* act cautiously under high uncertainty;
* seek more information;
* switch learning strategies;
* avoid overconfident errors;
* communicate uncertainty to users.

Confidence could help determine whether the agent should:

* exploit what it already knows;
* explore;
* request assistance;
* update its model;
* change controllers.

Lee and Seymour argue that metacognition may increase robustness in changing and noisy environments. 

---

# 24. Broader interdisciplinary benefits

The paper proposes a two-way relationship:

## Neuroscience-inspired robotics

Neural findings can inspire:

* multiple learning controllers;
* episodic memory;
* grid-like spatial representations;
* confidence monitoring;
* adaptive learning rates;
* social decision-making;
* intrinsic motivation.

## Robotics-driven neuroscience

Robots provide physical test platforms for:

* models of continuous action;
* navigation;
* long-term learning;
* motor noise;
* embodiment;
* environmental uncertainty;
* competing controllers.

## Automated scientific discovery

AI and robotics may also improve neuroscience research by helping to:

* optimize experimental designs;
* select task parameters;
* distinguish competing hypotheses;
* automate data collection;
* analyze high-dimensional results.

## Human–robot interaction

Robots that learn in more human-like ways may be easier for humans to understand.

Possible benefits include:

* greater trust;
* easier prediction of robot intentions;
* cooperation;
* joint decision-making;
* observational learning;
* assistance for people with cognitive impairments.

The paper’s main conclusion is that decision neuroscience and robotics should not progress independently. Each discipline contains tools for addressing the other’s limitations. 

---

# 25. High-yield comparison table

| Feature                   | Pavlovian                                                    | Habitual                                          | Goal-directed                                  |
| ------------------------- | ------------------------------------------------------------ | ------------------------------------------------- | ---------------------------------------------- |
| Association               | Stimulus–outcome                                             | Stimulus–response/cached action value             | Action–outcome                                 |
| Question answered         | “What event is predicted?”                                   | “What action worked before?”                      | “What will this action produce now?”           |
| Response form             | Prepared, stereotyped                                        | Repeated, automatic                               | Flexible, planned                              |
| Outcome-value sensitivity | Sometimes prediction-specific, but response often inflexible | Low                                               | High                                           |
| Computational analogue    | Often model-free state value                                 | Model-free action value                           | Model-based action value                       |
| Main neural circuit       | Amygdala–OFC–ventral striatum                                | Sensorimotor cortex–dorsolateral striatum/putamen | Prefrontal cortex–dorsomedial striatum/caudate |
| Main advantage            | Rapid anticipation                                           | Efficiency                                        | Flexibility                                    |
| Main limitation           | Can conflict with goals                                      | Perseveration                                     | Computational cost                             |

---

# 26. Key distinctions to remember

### Negative reinforcement versus punishment

* Negative reinforcement **increases** behavior by removing something aversive.
* Punishment **decreases** behavior.

### Pavlovian versus instrumental learning

* Pavlovian: a stimulus predicts an outcome.
* Instrumental: an action produces an outcome.

### Habitual versus goal-directed behavior

* Habitual behavior depends on past reinforcement.
* Goal-directed behavior depends on anticipated consequences and their current value.

### Extinction versus forgetting

* Extinction is new learning that the CS no longer predicts the US.
* The original association may remain and later recover.

### Dopamine versus pleasure

* Dopamine is not simply a pleasure chemical.
* It contributes to prediction errors, learning, motivation, action selection, and plasticity.

### Model-free versus model-based learning

* Model-free learning stores cached values.
* Model-based learning uses an internal representation of transitions and outcomes to plan.

---

# 27. Glossary

**Acquisition:** Development of a learned association through experience.

**Action–outcome association:** Knowledge that a particular action causes a particular consequence.

**Associative learning:** Learning a relationship between events or between an action and its outcome.

**Conditioned response:** Learned response elicited by a conditioned stimulus.

**Conditioned stimulus:** Previously neutral stimulus that predicts an important outcome after learning.

**Credit assignment:** Determining which earlier state or action caused a later outcome.

**Discrimination:** Learning to respond differently to similar stimuli.

**Extinction:** Reduction in a conditioned response when the CS occurs without the US.

**Generalization:** Responding to stimuli resembling the trained stimulus.

**Goal-directed control:** Selection based on expected action consequences and their current value.

**Habit:** Stimulus-triggered action strengthened through repetition and reinforcement.

**Habituation:** Decreased response to repeated harmless stimulation.

**Instrumental conditioning:** Learning how behavior changes environmental outcomes.

**Model-based RL:** Planning using an internal model of states, transitions, and rewards.

**Model-free RL:** Learning cached values directly from experience.

**Negative reinforcement:** Increasing behavior by removing or avoiding an aversive event.

**Pavlovian conditioning:** Learning that one stimulus predicts another event.

**Policy:** A rule that maps situations to actions.

**Prediction error:** Difference between expected and obtained or newly predicted outcome.

**Primary reinforcer:** Intrinsically biologically valuable outcome.

**Punishment:** Consequence that reduces behavior.

**Reinforcement:** Consequence that strengthens behavior.

**Secondary reinforcer:** Learned reinforcer that acquires value through association.

**Sensitization:** Increased response after repeated or intense stimulation.

**State value:** Expected future reward associated with a state.

**Temporal-difference learning:** Learning by comparing predictions at successive moments.

**Unconditioned stimulus:** Stimulus that naturally elicits a response without previous learning.

---
