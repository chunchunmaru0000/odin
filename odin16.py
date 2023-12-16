import math


def factorialSimple(n):  # цикл
    f = 1
    for i in range(n):
        f *= i + 1
    return f


def factorial(n):  # рекурсия
    try:
        if n < 0:
            raise ValueError
        elif n < 2:
            return 1
        else:
            return n * factorial(n - 1)
    except ValueError:
        return 'ValueError'


factorialL = lambda n: math.factorial(n)  # анонимная

# testcase
[print(factorial(n)) for n in range(-100, 100)]
print(factorialSimple(6))
print(factorial(6))
print(factorialL(6))
