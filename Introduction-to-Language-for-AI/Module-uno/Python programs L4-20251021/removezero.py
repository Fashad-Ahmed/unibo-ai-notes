def remove_zero(L):
    i=0
    while i<len(L):
        if L[i]==0:
            del L[i]
        else:
            i=i+1
    return L


S=[1,2,3,0,4,5,6,0]

def remove_zero_for(L):
  #WRONG! It will result in "list index out of range"
    for i in range(len(L)):
        if L[i]==0:
            del L[i]
    return L

def remove_zero_nonselection(L):
  #WRONG! It does not modify the list,
  #       because "del" is not called on a selection
    for e in L:
        if e==0:
            del e