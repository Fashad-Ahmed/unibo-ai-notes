# def modify_list(lst):
#     i = 0
#     while i < len(lst):
#         try:
#             # Try to convert to integer
#             lst[i] = int(lst[i])
            
#             # Force a ZeroDivisionError if divisible by 7
#             _ = 1 / (lst[i] % 7)
            
#         except ValueError:
#             # Element not convertible → remove
#             del lst[i]
#             continue  # don't increment i (since list shrinks)
            
#         except ZeroDivisionError:
#             # Divisible by 7 → replace with 'seven'
#             lst[i] = 'seven'
            
#         finally:
#             i += 1


# data = [14, '21', 3.5, 'x', 7, 'not', 28]
# modify_list(data)
# print(data)


# def count_t(D):
#     if not isinstance(D, dict):
#         return 0
#     result = {}
#     for v in D.values():
#         print(type(v))
#         # t = type(v)
#         t = type(v).__name__
#         result[t] = result.get(t, 0) + 1
#     return result

# print(count_t({'a': 1, 'b': 2, 'c': 'hi', 'd': 3.14, 'e': 10}))
# # Output: {'int': 3, 'str': 1, 'float': 1}

# print(count_t(123))


# class A:
#     def __init__(self, value):
#         self.value = value
#     def get(self):
#         return 10
    
# # from A import A

# class B(A):
#     def get(self):
#         return super().get() + 10

# a = A(5)
# b = B(5)
# print(b.get(), a.get())

# def collatz_gen(n):
#     while True:
#         yield n
#         if n == 1: break
#         if (n % 2) == 0 :
#             n = n // 2
#         else:
#             n = n * 3 + 1

# print(list(collatz_gen(29)))

# import numpy as np

# def maxtable(a, b):
#     return np.maximum(b[:, None], a)

# # b[:, None].  -> [[2],
# #  [5],
# #  [3]]


# a = np.array([1, 4, 7])
# b = np.array([2, 5, 3])

# print(maxtable(a, b))

# def move_zeros(L):
#     pos = 0
#     for i in range(len(L)):
#         if L[i] != 0:
#             L[pos], L[i] = L[i], L[pos]
#             pos += 1

# data = [0, 1, 0, 3, 12]
# move_zeros(data)
# print(data)
# # Expected: [1, 3, 12, 0, 0]

# D = {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 2, 'f': 2, 'g': 3, 'h': 4, 'i': 4}

# def frequent(D):
#     counts = {}
#     for v in D.values():
#         print(f"Processing value: {v}")
#         counts[v] = counts.get(v, 0) + 1
#     print(f"Results: {counts}")
#     max_count = max(counts.values())
#     print(f"Max count: {max_count}")
#     return [k for k, v in D.items() if counts[v] == max_count]
# print(frequent(D))
# def ad(D):
#     result = {}
#     for k,v in D.items():
#         if v not in result:
#             result[v] = [k]
#         else:
#             result[v].append(k)
            
#     return result

# print(ad(D))


import numpy as np

def fill(a):
    if not isinstance(a, np.ndarray) or a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("Not a square 2D array")
    
    row_means = np.mean(a, axis=1)
    np.fill_diagonal(a, row_means)
    return None
