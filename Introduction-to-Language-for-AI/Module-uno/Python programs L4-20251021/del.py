L=[1,2,0,3,0,5,0]
for e in L:
    if e == 0:
        del e

# for i in range(len(L)):
#     if L[i]==0:
#         del L[i]

i=0
while i<len(L):
    if L[i]==0:
        del L[i]
    else:
        i=i+1
