a = 10
b = a
print("a:", a, "b:", b) #b is a
print("is b the same of a?", a is b) #expected True
a = a+5 #a is bound to a new object
print("a:", a, "b:", b)  #b is still the "old" a; a is different
print("is b the same of a?", a is b) #expected False

print()
L1 = [1,2,3]
L2 = L1
print("L1:", L1, "L2:", L2) #L2 is L1
print("is L2 the same of L1?", L1 is L2) #expected True
L1[0] = 7 #L1 modified; no new assignment 
print("L1:", L1, "L2:", L2) #L2 is L1 (even after the modification of an element)
print("is L2 the same of L1?", L1 is L2) #expected True
L1 = [0,1] #L1 is bound to a new object 
print("L1:", L1, "L2:", L2) #L2 is still the "old" object created as L1; L1 changed
print("is L2 the same of L1?", L1 is L2) #expected False