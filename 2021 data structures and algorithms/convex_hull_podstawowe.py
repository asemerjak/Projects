class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def d(p, r, q):
    return (r.y - p.y)*(q.x - r.x) - (q.y - r.y)*(r.x - p.x)

def Jarvis(p, v2=False):
    n = len(p)
    left_idx = 0
    for i in range(1, n):
        if p[left_idx].x > p[i].x:
            left_idx = i

        if p[left_idx].x == p[i].x:
            if p[left_idx].y > p[i].y:
                left_idx = i
    result = [left_idx]
    temp_idx = left_idx
    iter = 0
    while iter == 0 or temp_idx != left_idx:
        iter = 1
        q_idx = (temp_idx + 1) % n
        for r_idx in range(n):
            dir = d(p[temp_idx], p[r_idx], p[q_idx])
            if dir < 0:
                q_idx = r_idx

            if dir == 0 and v2:
                if p[temp_idx].x > p[q_idx].x > p[r_idx].x or p[temp_idx].x < p[q_idx].x < p[r_idx].x or p[temp_idx].y > p[q_idx].y > p[r_idx].y or p[temp_idx].y < p[q_idx].y < p[r_idx].y:
                    q_idx = r_idx

        result.append(q_idx)
        temp_idx = q_idx

    points = []
    for i in result:
        points.append(Point(p[i].x, p[i].y))

    return points


def _sort(p):
    n = len(p)
    down_idx = 0
    for i in range(1, n):
        if p[down_idx].y > p[i].y:
            down_idx = i
        if p[down_idx].x == p[i].x:
            if p[down_idx].x > p[i].x:
                down_idx = i

    P0 = p.pop(down_idx)
    p.insert(0, P0)
    i = 1
    while i < n - 1:
        s = i
        dir = d(p[0], p[i], p[i + 1])
        if dir < 0:
            i += 1
        else:
            p[i], p[i + 1] = p[i + 1], p[i]
            if dir > 0:
                s -= 1

                while s > 0:
                    dir = d(p[0], p[s], p[s + 1])
                    if dir > 0:
                        p[s], p[s + 1] = p[s + 1], p[s]
                        s -= 1
                    else:
                        if dir == 0:
                            if p[s].x > p[s + 1].x:
                                p[s], p[s + 1] = p[s + 1], p[s]
                        break
            i += 1


def Graham(p):
    _sort(p)
    i = 1
    while i < len(p) - 1:
        dir = d(p[0], p[i], p[i + 1])
        if dir == 0:
            p.pop(i)
        else:
            i += 1

    stack = p[0:3]
    S = p[3:]

    for i in range(len(S)):
        stack.append(S.pop(0))
        last = stack[-3:]
        dir = d(last[0], last[1], last[2])
        if dir > 0:
            stack.pop(-2)

    points = []
    for i in range(len(stack)):
        points.append(Point(stack[i].x, stack[i].y))
    return points


def str_points(data):
    s = ""
    for p in data:
        s += "(" + str(p.x) + ', ' + str(p.y) + "), "
    return s[:-2]


def main():
    data1 = [Point(0, 3), Point(0, 0), Point(0, 1), Point(3, 0), Point(3, 3)]
    data2 = [Point(0, 3), Point(0, 1), Point(0, 0), Point(3, 0), Point(3, 3)]
    data3 = [Point(2, 2), Point(4, 3), Point(5, 4), Point(0, 3), Point(0, 2), Point(0, 0), Point(2, 1), Point(2, 0), Point(4, 0)]
    data4 = [Point(0, 3), Point(1, 1), Point(2, 2), Point(4, 4), Point(0, 0), Point(1, 2), Point(3, 1), Point(3, 3)]

    print("== Jarvis ==")
    print("Dane:", str_points(data1))
    print("wynik:", str_points(Jarvis(data1)))
    print("\nDane:", str_points(data2))
    print("wynik:", str_points(Jarvis(data2)))
    print("\nDane:", str_points(data3))
    print("wynik:", str_points(Jarvis(data3))) # dla zestawu 3 ta funkcja uwzględnia punkty współliniowe, natomiast wersja 2.0 tego nie robi (stąd rozbieżne wyniki)

    print("\n\n== Jarvis 2.0 ==")
    print("Dane:", str_points(data1))
    print("wynik:", str_points(Jarvis(data1, True)))
    print("\nDane:", str_points(data2))
    print("wynik:", str_points(Jarvis(data2, True)))
    print("\nDane:", str_points(data3))
    print("wynik:", str_points(Jarvis(data3, True)))

    print("\n\n== Graham ==")
    print("Dane:", str_points(data4))
    print("wynik:", str_points(Graham(data4)))

main()