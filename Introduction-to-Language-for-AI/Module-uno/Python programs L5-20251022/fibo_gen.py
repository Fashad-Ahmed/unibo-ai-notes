def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fibo_numbers = fibonacci_generator()

for n in fibo_numbers: #infinite loop
    print("Next fibo number is", n)