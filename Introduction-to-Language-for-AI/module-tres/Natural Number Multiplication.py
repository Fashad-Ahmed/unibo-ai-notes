"""
Natural Number Multiplication
Suppose you want to write a Python program which multiplies
two positive integer numbers, which can both be expressed as
n-digits numbers, but which are represented as lists rather than
scalars. Suppose that the operations at your disposal are just
the basic arithmetic operations on digits, so that you cannot just
multiply the two numbers. How should you write your program?
"""
def multiply(A, B):
    # Reverse for easier calculation (least significant digit first)
    A = A[::-1]
    B = B[::-1]

    n = len(A)
    m = len(B)

    # Result can be at most n + m digits
    result = [0] * (n + m)

    for i in range(n):
        for j in range(m):
            result[i + j] += A[i] * B[j]

            # Carry handling
            result[i + j + 1] += result[i + j] // 10
            result[i + j] %= 10

    # Remove leading zeros
    while len(result) > 1 and result[-1] == 0:
        result.pop()

    return result[::-1]

A = [3, 4, 5]   # represents 345
B = [6, 7]      # represents 67

print(multiply(A, B))