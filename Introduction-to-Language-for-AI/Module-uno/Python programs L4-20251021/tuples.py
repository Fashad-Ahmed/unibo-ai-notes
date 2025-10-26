def zeros(ToT):
    count=0
    for t in ToT:
        for e in t:
            if e==0:
                count += 1
    return count