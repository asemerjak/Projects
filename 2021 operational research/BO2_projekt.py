#!/usr/bin/python
# -*- coding: utf-8 -*-

# Agata Semerjak, 402426
# Monika Sukiennik, 401060
# Maciej Wieloch, 303080
# Badania Operacyjne, Projekt algorytmu, 10.01.2022

import itertools
import math
import numpy as np
from numpy.random import randint

# f_price (float): cena za litr paliwa [zł]
f_price = 5.89  


class Car:
    """
    Klasa opisująca samochód dostawczy

    Attributes:
        trunk_width (float): Szerokość przestrzeni ładunkowej [m]
        trunk_height (float): Wysokość przestrzeni ładunkowej [m]
        trunk_depth (float): Głębokość przestrzeni ładunkowej [m]
        fuel_consumption (float): Spalanie samochodu [l/100 km]

    """
    def __init__(self, trunk_width, trunk_height, trunk_depth, fuel_consumption):
        """
        Args:
            trunk_width (float): Szerokość przestrzeni ładunkowej [m]
            trunk_height (float): Wysokość przestrzeni ładunkowej [m]
            trunk_depth (float): Głębokość przestrzeni ładunkowej [m]
            fuel_consumption (float): Spalanie samochodu [l/100 km]

        """
        self.capacity = trunk_width * trunk_height * trunk_depth
        self.fuel_consumption = fuel_consumption


# Klasa Order - obsługuje zlecenie
# order_volume - wymagana pojemność do zabrania w samochodzie [m3]
# distance - odległość do pokonania [km]
# direction - 'n, s, w, e' - kierunek drogi
class Order:
    """
    Klasa opisująca ofertę zlecenia

    Attributes:
        order_volume (float): Wymagana pojemność do zabrania zlecenia w samochodzie [m^3]
        distance (float): Odległość do pokonania [km]
        direction (str): Kierunek, w którym trzeba przewieśc zlecenie ['n', 's', 'w', 'e']

    """
    def __init__(self, order_volume, distance, direction):
        """
        Args:
            order_volume (float): Wymagana pojemność do zabrania zlecenia w samochodzie [m^3]
            distance (float): Odległość do pokonania [km]
            direction (str): Kierunek, w którym trzeba przewieśc zlecenie ['n', 's', 'w', 'e']

        """
        self.order_volume = order_volume
        self.distance = distance
        self.direction = direction

    def __str__(self):
        result = ''
        result = 'Vol = ' + str(self.order_volume) + ', Dist = ' + str(self.distance) + ', Dir = ' \
                 + str(self.direction) + ';'

        return result

    def __repr__(self):
        return self.__str__()


def select(orders, car):
    """
    Funkcja licząca wszystkie konfiguracje otrzymanych zleceń,
    które zmieszczą się w przestrzeni załadunkowej pojazdu.

    Args:
        orders (List[Order]): Lista możliwych zleceń
        car (Car): Samochód dostawczy

    Returns:
        result (List): Lista możliwych konfiguracji zleceń
    """
    order_volumes = []
    order_numbering = []

    for i in orders:
        order_volumes.append(i.order_volume)

    for i in range(0, len(orders)):
        order_numbering.append(i)

    combinations_list = []
    result = []
    for i in range(1, len(orders) + 1):
        combinations = list(itertools.combinations(order_volumes, i))
        combinations_num = list(itertools.combinations(order_numbering, i))

        for j in range(len(combinations)):
            combination_capacity = sum(list(combinations[j]))
            if combination_capacity <= car.capacity:
                combinations_list.append(combinations_num[j])

                subsolution = []
                for k in list(combinations_num[j]):
                    subsolution.append(orders[k])
                result.append(subsolution)

    return result


def road(orders_list):
    """
    Funkcja obliczająca całkowitą drogę, którą
    trzeba pokonać do wykonania wszystkich zleceń

    Args:
        orders (List[Order]): Lista zleceń

    Returns:
        road_value (float): Długość drogi
    """
    if len(orders_list) == 1:
        return orders_list[0].distance

    result_s = [0]
    result_w = [0]
    result_n = [0]
    result_e = [0]

    for order in orders_list:
        if order.direction == 's':
            result_s.append(order.distance)

    for order in orders_list:
        if order.direction == 'w':
            result_w.append(order.distance)

    for order in orders_list:
        if order.direction == 'n':
            result_n.append(order.distance)

    for order in orders_list:
        if order.direction == 'e':
            result_e.append(order.distance)

    max_s = max(result_s)
    max_w = max(result_w)
    max_n = max(result_n)
    max_e = max(result_e)

    road_value = max_s/2 + math.sqrt((max_s/2)**2 + (max_w/2)**2) + math.sqrt((max_n/2)**2 + (max_w/2)**2) + math.sqrt((max_n/2)**2 + (max_e/2)**2) + max_e/2
    return road_value


def aim_function(order_list, car):
    """
    Funkcja celu - obliczająca zysk wykonania
    danych zleceń z listy podanym pojazdem

    Args:
        order_list (List[Order]): Lista zleceń
        car (Car): Samochód dostawczy

    Returns:
        result (float): Wartość zysku
    """
    d = road(order_list)

    payment = 0
    capacity_fraction = 0
    overall_distance = 0

    for order in order_list:
        capacity_fraction += (order.order_volume / car.capacity)
        overall_distance += order.distance

    payment = 10 * capacity_fraction * overall_distance

    cost = d / 100 * car.fuel_consumption * f_price

    result = payment - cost

    return result


def alike(order1, order2):
    """
    Funkcja sprawdzająca czy dwa zlecenia są takie same

    Args:
        order1 (Order): Pierwsze zlecenie
        order2 (Order): Drugie zlecenie

    Returns:
        likely_checker (int): Różnica sumy list z liczbą elemetów zbioru z dwóch list
    """
    orders_list = order1 + order2
    orders_set = set(orders_list)
    likely_checker = len(orders_list) - len(orders_set)
    return likely_checker

#????
def tabu_wrong(order_list, car, i_max):
    #order_list - lista ofert, które otrzymujemy od klientów
    orders = select(order_list, car) # lista rozwiązań spełniających ograniczenia
    idx = np.random.randint(0, len(orders))
    start_solution = orders[idx]
    max_curr_f = aim_function(start_solution, car)
    tabu_list = []
    curr_solution = start_solution
    i = 0

    while i <= i_max:
        i += 1
        for order in orders:
            if order not in tabu_list and alike(curr_solution, order) >= 1:
                aim_f = aim_function(order, car)
                tabu_list.append(curr_solution)
                if aim_f > max_curr_f:
                    curr_solution = order
                    max_curr_f = aim_f
                    break

        if len(tabu_list) == len(orders):
             break

    return (curr_solution, max_curr_f)


def max_aim(orders, car, full_return=False):
    """
    Funkcja wybierająca maksymalne rozwiązanie
    funkcji celu

    Args:
        orders (List[Order]): Lista zleceń
        car (Car): Samochód dostawczy

    Returns:
        result ((List[Order], float)): Lista zleceń gwarantuje największy zysk
                                oraz wartość tego zysku
    """
    temp = 0
    for order in orders:
        a_f = aim_function(order, car)
        if a_f > temp:
            temp = a_f
            result = (order, temp)
    if full_return:
        return result
    else:
        order1, temp1 = result
        return temp1




# ====== ALGORYTM GENETYCZNY =======

def valid(orders, tab_01, car):
    """
    Funkcja spradzająca czy rozwiązanie zakodowane w tablicy 
    zer i jedynek spełnia ograniczenie pojemności samochodu

    Args:
        orders (List[Order]): Lista możliwych zamówień
        tab_01 (List[int]): Lista zamówień w postaci zer i jedynek
        car (Car): Samochód dostawczy

    Returns:
        bool: Wartość logiczna mówiąca czy zalecenia zmieszczą się
              czy też nie
    """
    sum = 0
    for i in range(len(orders)):
        if tab_01[i] == 1:
            sum += orders[i].order_volume

    if sum > car.capacity:
        return False

    return True


def generate_population(orders, car, size_of_population):
    """
    Funkcja służąca generacji populacji 15 rozwiązań 
    spełniających ograniczenia

    Args:
        orders (List[Order]): Lista zleceń
        car (Car): Samochód dostawczy

    Returns:
        population (List[List[int]]): Lista zawierająca populacje
                                      rozwiązań
    """
    population = []
    for _ in range(size_of_population):
        val = False
        while not val:
            tab = [np.random.randint(0, 2) for _ in range(len(orders))]
            if tab in population:
                val = False
                continue
            val = valid(orders, tab, car)

        population.append(tab)

    return population


def bin_to_dec(tab01, orders):
    """
    Funkcja konwertująca rozwiązanie w formie binarnej 
    do listy zamówień jako obiektów klasy Order

    Args:
        orders (List[Order]): Lista możliwych zamówień
        tab_01 (List[int]): Lista zamówień w postaci zer i jedynek

    Returns:
        result (List[Order]): Lista zamówień jako obiektów klasy Order
    """
    result = []
    for i in range(len(tab01)):
        if tab01[i] == 1:
            result.append(orders[i])
    return result

def print_solution(tab_01, orders, car):
    """
    Funkcja wypisująca rozwiązanie

    Args:
        orders (List[Order]): Lista możliwych zamówień
        tab_01 (List[int]): Lista zamówień w postaci zer i jedynek
        car (Car): Samochód dostawczy

    """
    order_list = bin_to_dec(tab_01, orders)
    print(tab_01, aim_function(order_list, car))
    return None

def selection(population, orders, car, parents_num):
    """
    Funkcja służąca selekcji 6 najlepszych 
    rozwiązań za pomocą rankingu

    Args:
        population (List[List[int]]): Lista zawierająca populacje
                                      rozwiązań
        orders (List[Order]): Lista możliwych zamówień
        car (Car): Samochód dostawczy

    Returns:
        better_population (List[List[int]]): Populacja złożona z 6 najlepszych
                                             rozwiązań
    """
    score = []

    for solution in population:
        dec = bin_to_dec(solution, orders)
        value = aim_function(dec, car)
        score.append(value)

    idxs = []
    better_population = []
    for _ in range(parents_num):
        max_idx = np.argmax(score)
        idxs.append(max_idx)
        score[max_idx] = -1
        better_population.append(population[max_idx])

    return better_population


def make_valid_child(kid, orders, car):
    """
    Funkcja sprawdzająca czy nowopowstałe rozwiązanie mieści
    się w pojeździe. W przypadku gdy rozwiązanie nie spełnia
    warunku, usprawnia je, tak długo aż nie zostanie spełniony

    Args:
        kid (List[int]): Rozwiązanie w postaci 0 i 1
        orders (List[Order]): Lista możliwych zamówień
        car (Car): Samochód dostawczy

    Returns:
        kid (List[int]): Rozwiązanie w postaci 0 i 1 spełniające warunek
    """
    if valid(orders, kid, car):
        return kid

    while not valid(orders, kid, car):
        idx = np.random.randint(len(kid))

        while kid[idx] != 1:
            idx += 1
            if idx == len(kid):
                idx = 0

        kid[idx] = 0

    return kid


def mate(population, orders, car, kids_num, way_of_crossing):
    """
    Funkcja przeprowadzająca krzyżowanie, a następnie
    zwracająca listę nowych rozwiązań
    
    Args:
        population (List[List[int]]): Lista zawierająca populacje
                                      rozwiązań
        orders (List[Order]): Lista możliwych zamówień
        car (Car): Samochód dostawczy

    Returns:
        kids (List[List[int]]): Lista nowopowstałych rozwiązań
    """
    kids = []
    if way_of_crossing == 'half-half' or way_of_crossing == 'random':
        if way_of_crossing == 'half-half': #połowa z jednego rodzica i połowa z drugiego rodzica
            divide_idx = len(population[0])//2

        for _ in range(kids_num):
            if way_of_crossing == 'random':  # losowy indeks "rozcięcia"
                divide_idx = np.random.randint(len(population))

            mom_idx = np.random.randint(len(population))
            dad_idx = np.random.randint(len(population))
            mom = population[mom_idx]
            dad = population[dad_idx]
            kid = mom[:divide_idx] + dad[divide_idx:]
            kid = make_valid_child(kid, orders, car)
            kids.append(kid)

    elif way_of_crossing == "start-middle-end": #poczatek z mamy, srodek z taty, koniec z mamy
        divide_idx = len(population[0])//4

        for _ in range(kids_num):
            mom_idx = np.random.randint(len(population))
            dad_idx = np.random.randint(len(population))
            mom = population[mom_idx]
            dad = population[dad_idx]
            kid = mom[:divide_idx] + dad[divide_idx: divide_idx*2] + mom[divide_idx*2:]
            kid = make_valid_child(kid, orders, car)
            kids.append(kid)

    elif way_of_crossing == "every-other": #co drugi element z mamy, a co drugi z taty
        for _ in range(kids_num):
            kid = []
            mom_idx = np.random.randint(len(population))
            dad_idx = np.random.randint(len(population))
            mom = population[mom_idx]
            dad = population[dad_idx]
            for i in range(len(population[0])):
                if i % 2 == 0:
                    kid.append(mom[i])
                else:
                    kid.append(dad[i])

            kid = make_valid_child(kid, orders, car)
            kids.append(kid)

    return kids


def mutation(tab_01, orders, car):
    """
    Funkcja przeprowadzająca mutację 

    Args:
        tab_01 (List[int]): Lista zamówień w postaci zer i jedynek
        orders (List[Order]): Lista możliwych zamówień
        car (Car): Samochód dostawczy

    Returns:
        tab (List[int]): Lista zamówień powstała w wyniku mutacji
    """
    idx = np.random.randint(len(tab_01))
    tab = tab_01[:]
    if tab_01[idx] == 1:
        tab[idx] = 0
    else:
        tab[idx] = 1
        tab = make_valid_child(tab, orders, car)
    return tab


def genetic(orders, car, i_max, kids_num=6, parents_num=6, parents_mutants_num=3, kids_mutants_num=2, best_parents_num=4, way_of_crossing='half-half', full_return = False):
    """
    Funkcja, której ciało stanowi właściwe przeprowadzenie
    algorytmu genetycznego

    Args:
        orders (List[Order]): Lista możliwych zamówień
        car (Car): Samochód dostawczy
        i_max (int): Maksymalna możliwa liczba przeprowadzanych
                     iteracji

    Returns:
        solution (List[int]): Najlepsze znalezione rozwiązaniew postaci listy zer i jedynek
        money (float): Zysk uzyskany za wykonanie zamówień z rozwiązań
        i_best (float): Liczba iteracji, po której uzyskano najlepszy rezultat
    """

    size_of_population = kids_num + parents_mutants_num + kids_mutants_num + best_parents_num
    population = generate_population(orders, car, size_of_population) # 15 poprawnych losowych rozw.
    cnt = 0
    best = None
    while cnt < i_max:
        parents = selection(population, orders, car, parents_num) # 6 najlepszych
        kids = mate(parents, orders, car, kids_num, way_of_crossing) # dostajemy 6 dzieci z 6 najlepszych rodziców

        mutants = []
        for i in range(parents_mutants_num): #mutujemy 3 rodziców
            idx = np.random.randint(len(parents))
            mutant = mutation(parents[idx], orders, car)
            mutants.append(mutant)

        for i in range(kids_mutants_num): #mutujemy 2 dzieci
            idx = np.random.randint(len(kids))
            mutant = mutation(kids[idx], orders, car)
            mutants.append(mutant)

        population = parents[:best_parents_num] + kids + mutants # nowa populacja = 4 najlepszych rodziców + dzieci + mutacje

        if parents[0] != best:
            i_best = cnt #zapamiętanie ostatniej iteracji, w której nastąpiło ulepszenie rozwiązania

        best = parents[0]
        cnt += 1

    solution_01 = selection(population, orders, car, parents_num)[0]
    solution = bin_to_dec(solution_01, orders)
    money = aim_function(solution, car)
    if full_return:
        return solution, money, i_best
    else:
        return money, i_best


def generate_valid_neighbour(solution, orders, car):
    """
    Funkcja generująca sąsiada, spełniającego warunek pojemności, przy
    użyciu zmiany losowego indeksu na przeciwny 

    Args:
        solution (List[int]): Lista zamówień w postaci zer i jedynek
        orders (List[Order]): Lista możliwych zamówień
        car (Car): Samochód dostawczy

    Returns:
        neighbour (List[int]): Nowopowstałe rozwiązanie w postaci zer i jedynek
    """
    val = False
    while not val:
        idx = np.random.randint(len(solution))
        neighbour = solution[:]
        if solution[idx] == 1:
            neighbour[idx] = 0
        else:
            neighbour[idx] = 1
        val = valid(orders, neighbour, car)

    return neighbour


def tabu(orders, car, i_max, tabu_length=20, full_return=False):
    """
    Funkcja realizująca taboo search

    Args:
        orders (List[Order]): Lista możliwych zamówień
        car (Car): Samochód dostawczy
        i_max (int): Maksymalna możliwa liczba przeprowadzanych
                     iteracji
        tabu_length (int, optional): długośc listy taboo (Domyślna wartość to 20)

    Returns:
        best_as_bin (List[int]): Najlepsze znalezione rozwiązaniew postaci 
                                 listy zer i jedynek
        best_aim (float): Zysk uzyskany za wykonanie zamówień z rozwiązań
        i_best (float): Liczba iteracji, po której uzyskano najlepszy rezultat
    """
    #generujemy pierwsze losowe rozwiązanie
    val = False
    while not val:
        solution = [np.random.randint(0, 2) for _ in range(len(orders))]
        val = valid(orders, solution, car)

    i = 0
    best = solution
    best_aim = aim_function(bin_to_dec(solution, orders), car)
    i_best = i

    tabu_list = [solution]

    while i < i_max:
        #generujemy sąsiada spelniającego założenia
        in_tabu = True
        while in_tabu:
            neighbour = generate_valid_neighbour(solution, orders, car)
            in_tabu = (neighbour in tabu_list)

        neighbour_aim = aim_function(bin_to_dec(neighbour, orders), car) #funkcja celu sąsiada

        if neighbour_aim > best_aim: #jeśli nasz sąsiad jest lepszy niż dotychczasowe najlepsze rozwiązanie to zapamiętujemy go
            best = neighbour
            best_aim = neighbour_aim
            i_best = i

        tabu_list.append(neighbour)
        if len(tabu_list) <= tabu_length:
            del tabu_list[0]

        solution = neighbour  # przepinamy nasze aktualne rozwiązanie na sąsiada
        i += 1

    best_as_bin = bin_to_dec(best, orders)
    if full_return:
        return best_as_bin, best_aim, i_best
    else:
        return best_aim, i_best


if __name__ == '__main__':
    car1 = Car(2.1, 2.2, 4.2, 11)

    order1 = Order(8, 300, "n")
    order2 = Order(8, 500, "e")
    order4 = Order(1, 100, 'w')
    order3 = Order(12, 800, "n")
    order5 = Order(2, 200, "n")
    order6 = Order(4, 100, "e")
    order7 = Order(2, 200, 'e')
    order8 = Order(20, 260, 'e')
    order9 = Order(2, 200, 'e')
    order10 = Order(7, 20, 'e')
    order11 = Order(2, 600, 'w')
    order12 = Order(12, 400, 'e')
    order13 = Order(1, 900, 's')
    order14 = Order(2, 280, 'n')
    order15 = Order(9, 20, 'e')
    order16 = Order(1, 800, 'w')
    order17 = Order(17, 650, 'e')
    order18 = Order(13, 400, 's')
    order19 = Order(21, 30, 'n')
    order20 = Order(17, 250, 'n')

    order_list = [order1, order2, order3, order4, order5, order6, order7, order8, order9, order10, order11, order12, order13, order14, order15, order16, order17, order18, order19, order20]

    orders = select(order_list, car1)
    result_brute, aim_brute = max_aim(orders, car1, full_return=True)
    print("\nNajlepsza możliwa wartość funkcji celu:       ", aim_brute)
    print(result_brute)
    result_tabu, aim_tabu, iter_tabu = tabu(order_list, car1, 10000, full_return=True)
    result_genetic, aim_genetic, iter_genetic = genetic(order_list, car1, 300, full_return=True)
    print("\nAlgorytm tabu       ===> wartość funkcji celu:", aim_tabu)
    print(result_tabu)
    print("\nAlgorytm genetyczny ===> wartość funkcji celu:", aim_genetic)
    print(result_genetic)
    '''
    for _ in range(10):
        print("\nAlgorytm genetyczny:\n", genetic(order_list, car1, 300))'''

    print("\n\nHW")
