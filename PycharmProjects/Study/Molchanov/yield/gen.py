
def gen_countdown(n):
    while n != 0:
        yield n - 1
        n -= 1


g = gen_countdown(4)
print(next(g))