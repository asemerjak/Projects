import time


def naive(S, W):
    start_time = time.time()
    cnt = 0

    start_idxs = []
    for m in range(len(S)):
        cnt += 1
        if S[m] == W[0]:
            found = True

            for i in range(1, len(W)):
                cnt += 1
                if S[m + i] != W[i]:
                    found = False
                    break
            if found:
                start_idxs.append(m)

    stop_time = time.time()
    t = stop_time - start_time
    return start_idxs, t, cnt, None


def hash(W, S, match=True, hS=None, m=None):
    d = 256
    q = 101
    N = len(W)
    if match:
        hW = 0
        for i in range(N):
            hW = (d*hW + ord(W[i])) % q
        return hW
    h = 1
    for i in range(N - 1):
        h = (h*d) % q
    hS = (d*(hS - ord(S[m])*h) + ord(S[m + N])) % q
    if hS < 0:
        hS += q
    return hS


def Rabin_Karp(S, W):
    start_time = time.time()
    cnt = 0
    error_cnt = 0
    start_idxs = []
    M = len(S)
    N = len(W)
    hW = hash(W, S)
    hS = 0
    for m in range(M - N + 1):
        if m == 0:
            hS = hash(S[0: N], S)
        else:
            hS = hash(W, S, False, hS, m - 1)

        if hS == hW:
            cnt += 1
            if S[m: m + N] == W:
                start_idxs.append(m)
            else:
                error_cnt += 1
    stop_time = time.time()
    t = stop_time - start_time
    return start_idxs, t, cnt, error_cnt


def tab(W):
    T = [0 for _ in range(len(W) + 1)]
    pos = 1
    cnd = 0
    T[0] = -1
    while pos < len(W):
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]
        pos += 1
        cnd += 1
    T[pos] = cnd
    return T


def Knuth_Morris_Pratt(S, W):
    start_time = time.time()
    cnt = 0
    start_idxs = []
    T = tab(W)
    m = 0
    i = 0
    while m < len(S):
        cnt += 1
        if W[i] == S[m]:
            i += 1
            m += 1
            if i == len(W):
                start_idxs.append(m - i)
                i = T[i]
        else:
            i = T[i]
            if i < 0:
                i += 1
                m += 1
    stop_time = time.time()
    t = stop_time - start_time
    return start_idxs, t, cnt, None


def main():
    with open('lotr.txt', encoding='utf-8') as f:
        sample = f.readlines()

    S = ' '.join(sample).lower()
    Ws = ['elves', 'baggins', 'were']
    for W in Ws:
        results = [naive(S, W), Rabin_Karp(S, W), Knuth_Morris_Pratt(S, W)]
        methods = ["naiwna", "Rabina Karpa", "Knutha-Morrisa-Pratta"]

        print("\nSzukany wz??r:", W)
        for i in range(len(results)):
            starts, t, cnt, errors = results[i]
            method = methods[i]
            print("\n\n==== metoda", method, "====")
            print("Liczba powt??rze?? wzoru:", len(starts))
            print("Czas wykonywania:", t)
            print("Liczba por??wna??:", cnt)
            if errors:
                print("Liczba b????dnych dopasowa??:", errors)
                print(starts)

main()

# Najszybsz?? metod?? okaza??a si?? metoda naiwna, mimo, ??e wykonuje ona najwi??cej por??wna??. Zaraz potem (oko??o 2-3 razy
# wolniejsza) metoda Knutha-Morrisa-Pratta (z niewiele mniejsz?? liczb?? por??wna??). Na ko??cu plasuje si?? metoda
# Rabina Karpa z ponad 100krotnie mniejsz?? liczb?? por??wna??, jednak oko??o 10krotnie d??u??szym czasem wykonywania ni??
# metoda naiwna. Dodatkowo zaobserwowano, ??e wraz ze wzrostem liczby q maleje liczba b????dnych dopasowa??. Ma to jednak
# negatywny wp??yw na czas wykonywania operacji haszowania, kt??ra i tak jest czasoch??onna nawet dla ma??ej warto??ci q.
















