LC='When in the Course of human events'

## with two lists:
## LF0: the elements of LC, with multiplicity one
## LF1: frequencies: LF1[i] frequence of LF0[i]
## LF0 = ['W','h', 'e', 'n', ' ',...]
## LF1 = [ 1 , 2, 5, ...]

LF0 = []
LF1 = []
for e in LC:
    if e not in LF0:
        LF0.append(e)
        LF1.append(1)
    else:
        LF1[LF0.index(e)] += 1
# print(LF0)
# print(LF1)

# with a dictionary
Freq={}
for e in LC:
    if e not in Freq:
        Freq[e]=1
    else:
        Freq[e]+=1
print(Freq)

# with the get() method:
Freq={}
for e in LC:
    Freq[e]=Freq.get(e,0)+1
print(Freq)

