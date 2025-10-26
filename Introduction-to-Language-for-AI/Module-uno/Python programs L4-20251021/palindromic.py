def palind(S):
    if len(S)<=1:
        return True
    if S[0]!=S[-1]: #they both exist!
        return False
    return palind(S[1:-1])