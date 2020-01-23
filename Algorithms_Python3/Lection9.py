def merge(A:list, B:list):
    """Сливает два отсортированных массива в отсортированный массив
    Первая реализация."""
    C = [0]*(len(A)+len(B))
    i = k = n = 0
    while i < len(A) and k < len(B):
        if A[i] <= B[k]:
            C[n] = A[i]
            i += 1
            n += 1
        else:
            C[n] = B[k]
            k += 1
            n += 1
    while i < len(A):
        C[n] = A[i]
        i += 1
        n += 1
    while k < len(B):
        C[n] = B[k]
        k += 1
        n += 1
    return C


# Рекурсивная функция
def merge_soft(a):
    if len(a) <= 1:
        return
    middle = len(a)//2
    l = [a[i] for i in range(middle)]
    r = [a[i] for i in range(middle, len(a))]
    merge_soft(l)
    merge_soft(r)
    c = merge(l, r)
    for i in range(len(a)):
        a[i] = c[i]
    return a


print(merge_soft([10, 20, 400, 43, 45, 15, 21, 33]))