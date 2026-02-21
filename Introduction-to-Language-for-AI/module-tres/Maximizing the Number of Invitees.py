"""
Suppose you are going to marry your boyfriend (or girlfriend)
soon, and you want to decide the list of invitees. Since your
soon-to-be father-in-law will pay all bill, you have all the
interest in keeping the list of invitees as large as possible. But
actually, it would be impossible to invite all the people in the
set L = {a1, . . . , am} of all candidate invitees, since some of
them are kind of incompatible, and cannot be invited together,
i.e. there is another set I = {(b1, c1), . . . ,(bn, cn)} ⊆ L × L
whose elements are those candidate invitees pairs which are
incompatible. Would it be possible to maximize the length of
the list of invitees?


Idea of the Algorithm

At each step, for a person v, we decide:

Include v (if no conflict with current guests)

Exclude v

We explore both choices recursively.

Pruning Rule

If: current_size + remaining_possible <= best_size

"""


def maximum_independent_set(people, incompatible_pairs):
    # Build adjacency list (conflict graph)
    adj = {p: set() for p in people}
    for u, v in incompatible_pairs:
        adj[u].add(v)
        adj[v].add(u)

    best_solution = []
    n = len(people)

    def backtrack(index, current_set):
        nonlocal best_solution
        
        # Prune if even taking all remaining people can't beat best
        if len(current_set) + (n - index) <= len(best_solution):
            return
        
        # If all people considered
        if index == n:
            if len(current_set) > len(best_solution):
                best_solution = current_set[:]
            return
        
        person = people[index]
        
        # Option 1: Try including this person (if no conflict)
        if all(neighbor not in current_set for neighbor in adj[person]):
            current_set.append(person)
            backtrack(index + 1, current_set)
            current_set.pop()
        
        # Option 2: Exclude this person
        backtrack(index + 1, current_set)

    backtrack(0, [])
    return best_solution


people = ["Alice", "Bob", "Carol", "David"]

incompatible_pairs = [
    ("Alice", "Bob"),
    ("Bob", "Carol")
]

result = maximum_independent_set(people, incompatible_pairs)
print("Maximum guest list:", result)