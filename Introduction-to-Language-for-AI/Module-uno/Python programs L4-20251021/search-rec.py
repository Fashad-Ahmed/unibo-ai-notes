def ric_lin(S,el):
    if len(S)==0:
        return False
    if S[0]==el:
        return True
    return ric_lin(S[1:],el)

def ric_lin_aux(S,index,el):
    if index==len(S):
        return -1
    if S[index]==el:
        return index
    return ric_lin_aux(S,index+1,el)
def ric_lin_v(S,el):
    return ric_lin_aux(S,0,el)

def ric_bin_r(S,el):  #binary search, recursive
    if len(S)==0:
        return False
    if len(S)==1:
        return S[0]==el
    med=len(S)//2
    if S[med]==el:
        return True
    if el<S[med]:
        return ric_bin_r(S[:med],el)
    else: # el>S[med]
        return ric_bin_r(S[med+1:],el)
    
    
    
    
