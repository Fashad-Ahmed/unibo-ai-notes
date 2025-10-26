from random import randint

def howmanybefore(x):
    if x<0 or x>99:
        return -1
    
    extract=randint(0,99)
    howmany=1
    
    while extract!=x:
        extract=randint(0,99)
        howmany=howmany+1
        
    return howmany