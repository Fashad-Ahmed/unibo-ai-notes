'''The following fragment shows some of the differences
between the augmented and the "normal" assignment'''
L=[0]
def f():
    L[0]=L[0]+1
    return L[0]
V=[0,1,2,3,4,5,6,7,8]
V[f()]=V[f()]+1
''' this is V[2]=V[1]+1, because in a standard assignment
the RHS is evaluated first'''
print(V)
L=[0]
V=[0,1,2,3,4,5,6,7,8]
V[f()]+=f()
''' this is V[1]=V[1]+2, because in an augmented assignment
the LHS is evaluated first'''
print(V)  