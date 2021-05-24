'''
Implement a function to compute the double factorial, that is the product of natural numbers with the same parity and
not exceeding a given number.

For example:
7!!=7⋅5⋅3⋅1
8!!=8⋅6⋅4⋅2

The function argument can be any non-negative integer.

Another answer:
def f(x):
    return x * f(x-2) if x > 0 else 1
'''


def f(x):
    if x <= 0:
        return 1
    else:
        return x * f(x - 2)
