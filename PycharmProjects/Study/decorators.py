from datetime import datetime

# Декораторы


# Верхняя обертка может получить свой аргумент, например name
def timeit(arg):
    print(arg)
    # Из-за определения имени в верхней функции, создается промежуточная функция, которая получает целевую функцию
    def outer(func):
        def wrapper(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            print(datetime.now() - start)
            return result
        return wrapper
    return outer


@timeit('name')
def one(n):
    l = []
    for i in range(n):
        if i % 2 == 0:
            l.append(i)
    return l


@timeit('name')
def two(n):
    l = [x for x in range(n) if x % 2 == 0]
    return l


one(10)
two(10)

# вызов декорируемой функции - тоже самое, что вызов типа
# l1 = timeit('name')(one)(10)