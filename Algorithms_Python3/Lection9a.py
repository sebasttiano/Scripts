def hoar_sort(a):
    """Сортировка Тони Хоара"""
    if len(a) <= 1:
        return
    barrier = a[0]
    l = []
    m = []
    r = []
    for x in a:
        if x < barrier:
            l.append(x)
        elif x == barrier:
            m.append(x)
        else:
            r.append(x)
    hoar_sort(l)
    hoar_sort(r)
    k = 0
    for x in l+m+r:
        a[k] = x
        k += 1
    return a

print(hoar_sort([10, 20, 400, 43, 45, 15, 21, 33]))