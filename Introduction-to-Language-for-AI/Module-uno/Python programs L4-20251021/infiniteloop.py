L=[10]

for e in L:
    L=L+[e]
print(L)
# this prints [10,10]

for e in L:
    L.append(e)
print(L)
# we never arrive to this print
# because the for is an infinite loop
