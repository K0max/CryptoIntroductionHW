import math
from functools import reduce
# import itertools # 这个库本来是我用来跑全排列的，但是全排列太哈人，遂作罢
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import time
import sys
import numpy as np
# import LandauFunction as LF

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return (a * b // gcd(a, b))

# 实际上MaxOrder就是K_max
def getMaxOrder(N):
    # 本来用下面这个函数跑的，但是鼠鼠不会Python的相对路径
    # return LF.Landau_function(N)
    max_order_time_start = time.time()
    primes = []
    max_prime = [0] * (2 * N + 1)
    for i in range(2, 2 * N + 1):
        if max_prime[i] == 0:
            max_prime[i] = i
            primes.append(i)
        j = 0
        while j < len(primes) and primes[j] <= max_prime[i] and primes[j] * i <= 2 * N:
            max_prime[primes[j] * i] = max_prime[i]
            j += 1
    g = [[1 for i in range(len(primes) + 1)] for j in range(N + 1)]
    for p in range(1, len(primes) + 1):
        for i in range(0, N + 1):
            g[i][p] = g[i][p - 1]
            power = primes[p - 1]
            while power <= i:
                new_option = g[i - power][p - 1] * power
                g[i][p] = max(g[i][p], new_option)
                power *= primes[p - 1]
    print(f"Get max order K_max cost {time.time() - max_order_time_start} seconds")
    return g[N][len(primes)]

def getIndex(afterPermutation):
    originForm = [i for i in range(1, len(afterPermutation) + 1)]
    eachIndex = []
    flag = [0] * len(afterPermutation)
    for i in range(len(afterPermutation)):
        if flag[i] == 1:
            continue
        j = i
        count = 0
        while True:
            count += 1
            if afterPermutation[j] == originForm[i]:
                eachIndex.append(count)
                break
            else:
                j = originForm.index(afterPermutation[j])
            flag[j] = 1
    return reduce(lambda x, y: lcm(x, y), eachIndex)

# 下面这个垃圾代码要跑完所有置换，时间复杂度是O(N!*N!)，这太哈人了，N=7要跑几十秒，不过这坨答辩我就留在这了，供各位路过观赏一下
# def draw_pK_plot(N):
#     total_permutation = math.factorial(N)
#     K = [i for i in range(1, total_permutation + 1)]
#     K_num = [0] * total_permutation
#     originForm = [i for i in range(1, N + 1)]
#     iter_list = list(itertools.permutations(originForm))
#     for i in iter_list:
#         this_permutation = list(i)
#         this_index = getIndex(this_permutation)
#         for j in range(this_index, total_permutation):
#             K_num[j] += 1
#     P = [float(K_num[i]) / float(total_permutation) for i in range(total_permutation)]
#     # draw plot of P and K, x axis is K, y axis is P
#     plt.plot(K, P)
#     plt.show()

# 生成N元的所有划分
def generate_lists(N):
    stack = [[i] for i in range(N+1)]
    while stack:
        curr = stack.pop()
        if len(curr) == N:
            if sum(curr) == N:
                yield curr
        else:
            last = curr[-1]
            for i in range(last, -1, -1):
                new_partial = curr + [i]
                if sum(new_partial) <= N:
                    stack.append(new_partial)

def getEquivalentNum(N_cycle_list, N, total_permutation_num):
    # 编写一个字典，key为N_cycle_list里面出现的非零元素，value为该元素出现的次数
    # 例如N_cycle_list = [1, 1, 2, 2, 2, 0, 0, 0]，那么这个字典为{1: 2, 2: 3}
    n = N
    N_cycle_dict = {}
    for i in N_cycle_list:
        if i != 0:
            if i not in N_cycle_dict.keys():
                N_cycle_dict[i] = 1
            else:
                N_cycle_dict[i] += 1
    # 计算其排列组合的个数
    # 例如N_cycle_dict = {1: 2, 2: 3}，那么N=1*2+2*3=8,其排列组合的个数为comb(8,1)*comb(7,1)*comb(6,2)*comb(4,2)*comb(2,2)/(perm(2,2)*perm(3,3))=420
    portion_inverse = 1
    for key, value in N_cycle_dict.items():
        portion_inverse *= key**value * math.factorial(value)
    result = total_permutation_num // portion_inverse
    return result

def draw_pK_plot(N, K_max):
    draw_time_start = time.time()
    # 此处的K是x轴的所有取值
    K_list = [i for i in range(1, K_max + 1)]
    # K_value是y轴的所有取值
    K_value_list = [0] * K_max
    # 计算全排列，防止重复计算
    total_permutation_num = math.factorial(N)
    for N_cycle_list in generate_lists(N):
        # 去掉N_cycle_list中的所有0
        N_cycle_list = [i for i in N_cycle_list if i != 0]
        this_index = reduce(lambda x, y: lcm(x, y), N_cycle_list)
        # 这里要写一个函数，计算与N_cycle_list等价的所有排列的个数
        this_cycle_num = getEquivalentNum(N_cycle_list, N, total_permutation_num)
        K_value_list[this_index - 1] += this_cycle_num
    # 因为上面的K_value_list[this_index - 1] += 1是只计算了K值，而不是K值以下的所有值，所以这里要累加
    for k in range(1, K_max):
        K_value_list[k] += K_value_list[k - 1]
    P_list = [float(K_value_list[i]) / total_permutation_num for i in range(K_max)]
    plt.plot(K_list, P_list)
    plt.show()
    print(f"draw plot time cost: {time.time() - draw_time_start}")

def LogisticMapping(mu, x0, N):
    X_list = [x0]
    for i in range(N):
        X_list += [mu * X_list[-1] * (1 - X_list[-1])]
    X_list.pop(0)
    sorted_X_list = sorted(X_list)
    mapping = [(sorted_X_list.index(i) + 1) for i in X_list]
    return mapping

def permutationByMapping(mapping, originForm):
    afterPermutation = [0] * len(originForm)
    for i in range(len(originForm)):
        afterPermutation[i] = originForm[mapping[i] - 1]
    return afterPermutation

def chaosEvalutate(N, originForm):
    chaos_time_start = time.time()
    figure = plt.figure()
    ax = figure.add_subplot(111, projection='3d')
    MU_list = np.arange(3.64, 4, 0.008)
    X0_list = np.arange(0.1, 1, 0.02)
    X0_list, MU_list = np.meshgrid(X0_list, MU_list)
    # use numpy to calculate the index
    index_list = np.zeros(shape=(len(X0_list), len(MU_list)))
    for i in range(len(X0_list)):
        for j in range(len(MU_list)):
            mapping = LogisticMapping(MU_list[i][j], X0_list[i][j], N)
            LogisticMappingPermutation = permutationByMapping(mapping, originForm)
            index_list[i][j] = getIndex(LogisticMappingPermutation)
    ax.plot_surface(X0_list, MU_list, index_list, rstride=1, cstride=1, cmap='rainbow')
    plt.show()
    print(index_list)
    print(f"Chaos evaluation time cost: {time.time() - chaos_time_start}")

N = 15
originForm = [i for i in range(1, N + 1)]
# mu = 3.9
# x0 = 0.5

if __name__ == '__main__':
    print(f'N={N}')
    time_start = time.time()
    K_max = getMaxOrder(N)
    
    draw_pK_plot(N, K_max)
    chaosEvalutate(N, originForm)
    print(f"Done, total cost {time.time() - time_start} seconds")