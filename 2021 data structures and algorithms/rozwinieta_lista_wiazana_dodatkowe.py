class Element:
    size = 6

    def __init__(self):
        self.tab = [None for i in range(self.size)]
        self.next = None
        self.length = 0

    def get_next(self):
        return self.next

    def set_next(self, new_next):
        self.next = new_next

    def get_size(self):
        return self.size

    def get_length(self):
        return self.length

    def get_by_index(self, index):
        return self.tab[index]

    def delete(self, index):
        if self.tab[index]:
            self.tab[index] = None
            for i in range(index, self.size - 1):
                self.tab[i] = self.tab[i+1]
            self.tab[self.size - 1] = None
            self.length -= 1

    def insert_in_tab(self, index, data):
        if self.tab[index]:
            i = self.size - 2
            while i >= index:
                self.tab[i+1] = self.tab[i]
                i -= 1
            self.tab[index] = data
        else:
            self.tab[index] = data
        self.length += 1

    def print_tab(self):
        print('[', end='')
        for i in range(self.size):
            print(self.tab[i], end=' ')
        print("]", end=' ')


class UnrolledLinkedList:
    def __init__(self):
        self.head = Element()
        self.size = 0

    def get(self, index):
        temp = self.head
        i = index
        while i > (temp.get_length()-1):
            i -= temp.get_length()
            temp = temp.get_next()

        return temp.get_by_index(i)

    def insert(self, index, data):
        temp = self.head
        i = index
        size_of_tab = temp.get_size()

        while i > (temp.get_length() - 1):
            if temp.get_next():
                i -= temp.get_length()
                temp = temp.get_next()
            else:
                break

        if temp.get_length() < size_of_tab:
            temp.insert_in_tab(i, data)
            return
        else:
            new_tab = Element()
            half_size_of_tab = round(size_of_tab/2)
            for i in range(half_size_of_tab):
                data_to_be_moved = temp.get_by_index(half_size_of_tab + i)
                new_tab.insert_in_tab(i, data_to_be_moved)
            for i in range(half_size_of_tab):
                temp.delete(size_of_tab - i - 1)

            new_tab.set_next(temp.get_next())
            temp.set_next(new_tab)

            self.insert(index, data)

    def delete(self, index):
        temp = self.head
        i = index
        size_of_tab = temp.get_size()
        while i >= (temp.get_length()):
            i -= temp.get_length()
            temp = temp.get_next()

        temp.delete(index)
        if size_of_tab/2 > temp.get_length():
            temp_next = temp.get_next()
            if temp_next:
                first_of_next = temp_next.get_by_index(0)
                temp.insert_in_tab(temp.get_length(), first_of_next)
                temp_next.delete(0)

                if size_of_tab/2 > temp_next.get_length():
                    for j in range(temp_next.get_length() - 1):
                        temp.insert_in_tab(j + temp.get_length(), temp_next.get_by_index(0))
                        temp_next.delete(0)
                    temp.insert_in_tab(temp.get_length(), temp_next.get_by_index(0))
                    temp.set_next(temp_next.get_next())
                    temp_next.set_next(None)

    def print_list(self):
        temp = self.head
        while temp:
            temp.print_tab()
            temp = temp.get_next()
        print("\n")


def main():
    my_list = UnrolledLinkedList()
    for i in range(9):
        my_list.insert(i, i)

    my_list.print_list()
    print("Czwarty element listy: ", my_list.get(3))

    my_list.insert(1, 11)
    my_list.insert(8, 88)
    print("\nLista po dodaniu 11 pod indeks 1 i 88 pod 8:")
    my_list.print_list()
    my_list.delete(1)
    print("\nLista po usunięciu danej spod indeksu 1:")
    my_list.print_list()
    my_list.delete(2)
    print("\nLista po usunięciu danej spod indeksu 2:")
    my_list.print_list()


main()














