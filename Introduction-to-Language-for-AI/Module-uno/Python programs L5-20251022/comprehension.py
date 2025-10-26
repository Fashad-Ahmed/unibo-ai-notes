# an explicit construction of a list
T=[]
for x in range(2):
    for y in range(3):
        if x<y:
            T.append((x,y))

# its equivalent comprehension
TT=[(x,y) for x in range(2) for y in range(3) if x<y]

print(T==TT)
