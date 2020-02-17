def lcs(A, B):
    '''Наибольшая общая подпоследовательность'''
    F = [[0] * (len(B)+1) for i in range(len(A)+1)]
    for i in range(1, len(A)+1):
        for j in range(1, len(B)+1):
            if A[i-1] == B[j-1]:
                F[i][j] = 1 + F[i-1][j-1]
            else:
                F[i][j] = max(F[i-1][j], F[i][j-1])
    return F[-1][-1]


def gis(A):
    '''Наибольшая возрастающая последовательность'''
    F = [0] * (len(A)+1)
    for i in range(1, len(A)+1):
        m = 0
        for j in range(0, i):
            if A[i] > A[j] and F[j] > m:
                m = F[j]
        F[i] = m + 1
    return F[len(A)]