import numpy as np
import time


def primes(n, start=101):
    tab = []
    i = start
    cnt = 1
    while len(tab) != n:
        prime = True
        for j in range(2, int(i/2 + 1)):
            if i % j == 0:
                prime = False
                break
        if prime:
            tab.append(i)
        i += 13
        if i > 288:
            i = start + 2*cnt
            cnt += 1
    return tab


def hash(N, S, qs, m=None):
    d = 256
    idx_tab = []
    idx = 0
    for q in qs:
        for i in range(m+1, N+m+1):
            idx = (d * idx + ord(S[i])) % q
        idx_tab.append(idx)
    return idx_tab


def Rabin_Karp_bloom(S, W, P=0.001, n=20, start_q=101):
    start_time = time.time()
    b = int(np.ceil(-n * np.log(P) / ((np.log(2)) ** 2)))  # rozmiar tablicy Blooma
    k = int(np.ceil(b / n * np.log(2)))  # liczba funkcji haszujących
    bloom = [0 for _ in range(b)]
    cnt = 0
    error_cnt = 0
    start_idxs = []
    M = len(S)
    N = len(W[0])
    qs = primes(k, start_q)
    for subW in W:
        idxs_W = hash(N, subW, qs, -1)
        for i in idxs_W:
            bloom[i] = 1

    for m in range(M - N + 1):
        idxs_S = hash(N, S, qs, m-1)
        match = True
        for i in idxs_S:
            if bloom[i] != 1:
                match = False
                break

        if match:
            cnt += 1
            if S[m: m + N] in W:
                start_idxs.append(m)
            else:
                if error_cnt < 10:
                    print("Błędne dopasowanie:", S[m: m + N])
                error_cnt += 1

    stop_time = time.time()
    t = stop_time - start_time
    return start_idxs, t, cnt, error_cnt


def main():
    with open('lotr.txt', encoding='utf-8') as f:
        sample = f.readlines()

    S = ' '.join(sample).lower()
    WW = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however', 'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself', 'present', 'deliver', 'welcome', 'baggins', 'further']
    W1 = [WW[0]]
    W2 = WW[0:6]
    W3 = WW[0:11]
    W4 = WW

    for W in [W1, W2, W3, W4]:
        print("\nSzukane wzory:", W)
        starts, t, cnt, errors = Rabin_Karp_bloom(S, W)
        print("Liczba powtórzeń wzorów:", len(starts))
        print("Czas wykonywania:", t)
        print("Liczba porównań:", cnt)
        print("Liczba błędnych dopasowań:", errors)

main()

#Pomimo zwiększania liczby wzorców czas wykonywania pozostaje niemal ten sam.