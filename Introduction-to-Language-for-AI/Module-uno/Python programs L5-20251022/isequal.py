# == between strings does not always imply identity of the objects

n='Michael'
s=' Lodi'
ns=n+s
fn='Michael Lodi'
print("id of ns is", id(ns), "while id of fn is", id(fn))
print("ns is fn?", ns is fn)
print("ns == fn?", ns == fn)

# for optimization reasons, Python machine could decide
# to use the same object for ns and fn