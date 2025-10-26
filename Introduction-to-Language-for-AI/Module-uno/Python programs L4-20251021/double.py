L=[10,20,30]

for el in L:
    el=el*2
# NO! el would be a name which is introduced and changed
# at any iteration, without effect on L
# Try it in Pythontutor!
print(L)

# we must a use a selection on the left of = 
for i in range(len(L)):
    L[i]=L[i]*2

print(L)
