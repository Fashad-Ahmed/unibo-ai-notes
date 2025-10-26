# for i in range(1000):
#     print("Strings and tuples are immutable")

def cons_eq(S):
    for i in range(len(S)-1):
        if S[i] == S[i+1]:
            return True
    return False

def cons_eq_alt(S):
    for i in range(1, len(S)):
        if S[i-1] == S[i]:
            return True
    return False

A = "mamma"
B = "simons"
C = ""
D = "K"
E = "ee"

print(cons_eq(A))
print(cons_eq(B))
print(cons_eq(C))
print(cons_eq(D))
print(cons_eq(E))
print(cons_eq_alt(A))
print(cons_eq_alt(B))
print(cons_eq_alt(C))
print(cons_eq_alt(D))
print(cons_eq_alt(E))

#works with tuples as well