''' Round Robin loop and generators'''
# Генераторы - это функции!!!!
# Выполнение функции идет до yield (как-будто пауза). При вызове next() происходит продолжение течения функции
# после yield. yield может бьть много.
from time import time


def gen_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time() * 1000)

        yield pattern.format(str(t))

        sum = 234 + 234
        print(sum)


def gen1(s):
    for i in s:
        yield i


def gen2(n):
    for i in range(n):
        yield i


g1 = gen1('oleg')
g2 = gen2(4)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass