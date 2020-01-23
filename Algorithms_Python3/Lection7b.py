def f(n):
    """Функция для подсчета факториала"""
    assert n >= 0, "Факториал отр. не определен"
    if n == 0:
        return 1
    return f(n-1)*n


def gcd(a, b):
    """находит наибольший общий делитель у a и b. gcb - grand common divisor. С помощью Алгоритма Евклида"""
    if a == b:
        return a
    elif a > b:
        return gcd(a-b, b)
    else:  # a < b
        return gcd(a, b-a)


def gcd2(a, b):
    """находит наибольший общий делитель у a и b. gcb - grand common divisor. С помощью Алгоритма Евклида
    Вариант 2, лучший способ, основанный на делении одного числа на другой по остатку"""
    return a if b == 0 else gcd(b, a%b)


def pow(a, n):
    """вычисляет a в степени n. Быстрое возведение"""
    if n == 0:
        return 1
    elif n%2 == 1:  # нечетное
        return pow(a, n-1)*a
    else: # четное
        return pow(a**2, n//2)