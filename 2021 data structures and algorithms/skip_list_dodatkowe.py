import random
import string


class Element:
    def __init__(self,  key, data, height):
        self.key = key
        self.data = data
        self.next = [None for _ in range(height)]
        self.height = height

    def get_key(self):
        return self.key

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_data(self, new_data):
        self.data = new_data

    def set_next(self, new_next, i):
        self.next[i] = new_next


class SkipList:

    def __init__(self, max_height):
        self.head = Element(-1, None, max_height)
        self.max_height = max_height

    def random_level(self, p=0.5):
        lvl = 1
        while random.random() < p and lvl < self.max_height:
            lvl = lvl + 1
        return lvl

    def search(self, key):
        temp = self.head
        for i in range(self.max_height-1, -1, -1):
            while temp.get_next()[i] is not None and temp.get_next()[i].get_key() < key:
                temp = temp.get_next()[i]

        temp = temp.get_next()[0]
        if temp is not None and temp.get_key() == key:
            return temp.get_data()
        else:
            print("Key not found!")
            return None

    def insert(self, key, data):
        lvl = self.random_level()
        elem = Element(key, data, lvl)
        temp = self.head
        previous = [self.head] * self.max_height

        for i in range(temp.height-1, -1, -1):
            while temp.get_next()[i] is not None and temp.get_next()[i].get_key() < key:
                temp = temp.get_next()[i]
            previous[i] = temp

        temp = temp.get_next()[0]
        if temp is None or temp.get_key() != key:
            for i in range(lvl):
                elem.set_next(previous[i].get_next()[i], i)
                previous[i].set_next(elem, i)
        elif temp.get_key() == key:
            temp.set_data(data)

    def delete(self, key):
        previous = [None] * self.max_height
        temp = self.head

        for i in range(self.max_height-1, -1, -1):
            while temp.get_next()[i] and temp.get_next()[i].key < key:
                temp = temp.get_next()[i]
            previous[i] = temp

        temp = temp.get_next()[0]
        if temp is not None and temp.key == key:
            for i in range(self.max_height):
                if previous[i].get_next()[i] != temp:
                    break
                previous[i].set_next(temp.get_next()[i], i)

    def display_list_(self):
        node = self.head.get_next()[0]  # pierwszy element na poziomie 0
        keys = []  # lista kluczy na tym poziomie
        while node is not None:
            if isinstance(node, list):
                break
            keys.append(node.get_key())
            node = node.get_next()[0]

        for lvl in range(self.max_height - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.get_next()[lvl]
            idx = 0
            while node is not None:
                if isinstance(node, list):
                    break
                while node.get_key() > keys[idx]:
                    print("  ", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.get_key()), end=" ")
                node = node.get_next()[lvl]
            print("")

    def __str__(self):
        temp = self.head.get_next()[0]
        my_string = ""
        while temp is not None:
            my_string += str(temp.get_key()) + " : " + str(temp.get_data()) + ",  "
            temp = temp.get_next()[0]
        return my_string


def main():
    my_list = SkipList(4)
    for i in range(1, 16):
        my_list.insert(i, string.ascii_lowercase[i-1])
    print("\nLista po wpisaniu 15 elementów:")
    my_list.display_list_()
    print("\nPoziom 0 listy (__str__):")
    print(my_list)

    print("\ndana o kluczu 2:", my_list.search(2))
    my_list.insert(2, "jestem nowe 2!")
    print("dana o kluczu 2 (po nadpisaniu):", my_list.search(2))
    my_list.delete(5)
    my_list.delete(6)
    my_list.delete(7)

    print("\nLista po usunięciu elementów o kluczah 5, 6, 7:\n", my_list, "\n")
    my_list.display_list_()
    my_list.insert(6, "jestem nowe 6!")
    print("\nLista po wpisaniu danej o kluczu 6:\n", my_list)


main()
