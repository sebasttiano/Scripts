def traj_num(N):
    '''Задачка про кузнечика'''
    K = [0, 1] + [0] * N
    for i in range(2, N+1):
        K[i] = K[i-2] + K[i-1]
    return K[N]


print(traj_num(6))


def count_trajectories(N, allowed: list):
    '''Варианты прыжков: +1, +2, +3. Также есть запрещенные клтеки'''
    K = [0, 1, int(allowed[2])] + [0]*(N-3)
    for i in range(3, N+1):
        if allowed[i]:
            K[i] = K[i-1] + K[i-2] + K[i-3]


def count_min_cost(N, price: list):
    '''Минимальная стоимость достижения клетки N'''
    C = [None, price[1], price[1] + price[2]] + [0] * (N-2)
    for i in range(3, N+1):
        C[i] = price[i] + min(C[i-1], C[i-2])
    return C[N]