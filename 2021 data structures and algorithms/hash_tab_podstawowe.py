import string


class Element:
    def __init__(self, key, data):
        self.key = key
        self.data = data

    def get_key(self):
        return self.key

    def get_data(self):
        return self.data


class HashTab:

    def __init__(self, size, c1=1, c2=0):
        self.size = size
        self.tab = [None for i in range(0, self.size)]
        self.c1 = c1
        self.c2 = c2
        self.counter = 0

    def hash(self, key):
        if type(key) == str:
            ascii_codes = 0
            for char in key:
                ascii_codes += ord(char)
            return ascii_codes % self.size
        else:
            return key % self.size

    def search(self, key):
        for elem in self.tab:
            if elem is not None:
                temp_key = elem.get_key()
                if temp_key == key:
                    return elem.get_data()
        print("This key doesn't exist!")
        return None

    def solve_collision(self, hash_key, i):
        return (hash_key + self.c1*i + self.c2*i**2) % self.size

    def insert(self, key, data):
        if self.counter >= self.size:
            for j in range(self.size):
                if self.tab[j].get_key() == key:
                    self.tab[j] = Element(key, data)
                    return
            print("Your tab is already full! You can't insert new element!")
            return None
        hash_key = self.hash(key)
        already_set = False
        i = 1

        while self.tab[hash_key] is not None and self.tab[hash_key].get_key() != key:
            if i >= self.size:
                for j in range(self.size):
                    if self.tab[j] is None:
                        self.tab[j] = Element(key, data)
                        already_set = True
                        break
            if already_set:
                break
            hash_key = self.solve_collision(hash_key, i)
            i += 1
        if not already_set:
            self.tab[hash_key] = Element(key, data)
        self.counter += 1

    def remove(self, key):
        hash_key = self.hash(key)
        if self.tab[hash_key] is None:
            print("This key doesn't exist!")
            return None
        self.tab[hash_key] = None
        self.counter -= 1

    def __str__(self):
        my_string = ''
        for elem in self.tab:
            if elem is not None:
                my_string += str(elem.get_key()) + " : " + str(elem.get_data()) + ', '

        my_string += '\n'
        return my_string

    def print_with_nones(self):
        my_string = ''
        for elem in self.tab:
            if elem is not None:
                my_string += str(elem.get_key()) + " : " + str(elem.get_data()) + ', '
            else:
                my_string += 'None, '

        my_string += '\n'
        print(my_string)


def test_1():
    print("\n\n---- TEST 1 ----\n")

    my_tab = HashTab(13)

    for i in range(1, 16):
        if i != 6 and i != 7:
            my_tab.insert(i, string.ascii_lowercase[i-1])
        elif i == 6:
            my_tab.insert(18, string.ascii_lowercase[i-1])
        elif i == 7:
            my_tab.insert(31, string.ascii_lowercase[i-1])

    print("\nMoja tablica (dodane 15 elementów):\n")
    my_tab.print_with_nones()

    print("Dana spod klucza = 5: ", my_tab.search(5))
    print("Dana spod klucza = 14: ")
    print(my_tab.search(14), '\n')

    my_tab.insert(5, 'zostałam nadpisana!')
    print("Dana spod klucza = 5 (po zmianie): ", my_tab.search(5))

    my_tab.remove(5)
    print("\nPo usunięciu spod klucza = 5:")
    my_tab.print_with_nones()

    print("Dana spod klucza = 31: ", my_tab.search(31))

    my_tab.insert('test', 'A')
    print("\nPo umieszczeniu elementu ('test', 'A'):")
    my_tab.print_with_nones()


def test_2():
    print("\n\n---- TEST 2 ----\n")

    my_tab = HashTab(13)

    for i in range(1, 16):
        my_tab.insert(13*i, string.ascii_lowercase[i-1])

    print("\nMoja tablica (dodane 15 elementów o kluczu 13) - próbkowanie liniowe:\n")
    my_tab.print_with_nones()


def test_3():
    print("\n\n---- TEST 3 ----\n")

    my_tab = HashTab(13, 0, 1)

    for i in range(1, 16):
        my_tab.insert(13*i, string.ascii_lowercase[i-1])

    print("\nMoja tablica (dodane 15 elementów o kluczu 13) - próbkowanie kwadratowe:\n")
    my_tab.print_with_nones()


def test_4():
    print("\n\n---- TEST 4 ----\n")

    my_tab = HashTab(13, 0, 1)

    for i in range(1, 16):
        if i != 6 and i != 7:
            my_tab.insert(i, string.ascii_lowercase[i-1])
        elif i == 6:
            my_tab.insert(18, string.ascii_lowercase[i-1])
        elif i == 7:
            my_tab.insert(31, string.ascii_lowercase[i-1])

    print("\nMoja tablica (dodane 15 elementów) - próbkowanie kwadratowe:\n")
    my_tab.print_with_nones()


test_1()
test_2()
test_3()
test_4()
