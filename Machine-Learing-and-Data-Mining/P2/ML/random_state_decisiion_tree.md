### random_state in decision tree of scikit learn

This is explained in the documentation

The problem of learning an optimal decision tree is known to be NP-complete under several aspects of optimality and even for simple concepts. Consequently, practical decision-tree learning algorithms are based on heuristic algorithms such as the greedy algorithm where locally optimal decisions are made at each node. Such algorithms cannot guarantee to return the globally optimal decision tree. This can be mitigated by training multiple trees in an ensemble learner, where the features and samples are randomly sampled with replacement.

So, basically, a sub-optimal greedy algorithm is repeated a number of times using random selections of features and samples (a similar technique used in random forests). The random_state parameter allows controlling these random choices.

The interface documentation specifically states:

If int, random_state is the seed used by the random number generator; If RandomState instance, random_state is the random number generator; If None, the random number generator is the RandomState instance used by np.random.

So, the random algorithm will be used in any case. Passing any value (whether a specific int, e.g., 0, or a RandomState instance), will not change that. The only rationale for passing in an int value (0 or otherwise) is to make the outcome consistent across calls: if you call this with random_state=0 (or any other value), then each and every time, you'll get the same result.

https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
https://scikit-learn.org/stable/modules/tree.html#tree
https://stackoverflow.com/questions/39158003/confused-about-random-state-in-decision-tree-of-scikit-learn