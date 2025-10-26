
def ins_ord(L,el):
    '''L: ordered list, in increasing order
insert el in L, in place
Linear search'''
    i=0
    while i<len(L) and L[i]<el:
        i = i+1
    L.insert(i,el)  # equivalent: L[i:i]=[el]
    return L

def ins_ord_b(L,el):
    '''L: ordered list, in increasing order
insert el in L, in place
binary search'''
    low=0
    high=len(L)
    while low<high:
        med=(low+high)//2
        if L[med]>el:
            high=med
        else:
            low=med+1
    L.insert(high,el)  # equivalent: L[high:high]=[el]
    return L

def ins_ord_L(L,el):
    '''An inefficent solution:
it solved the problem, but it costs more than the others.
It append the element, then re-sort the list.
Sorting costs more than a single scan of the list'''
    L.append(el)
    L.sort()
    return None


S=[1,2,5,6]

