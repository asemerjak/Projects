class Element:
    def __init__(self, data):
        self.data = data
        self.next = None

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_data(self, new_data):
        self.data = new_data

    def set_next(self, new_next):
        self.next = new_next


class List:
    def __init__(self):
        self.head = None
        self.size = 0

    def destroy(self):
        self.head = None
        self.size = 0

    def add(self, elem_data):
        elem = Element(elem_data)
        old_head = self.head
        self.head = elem
        self.head.set_next(old_head)
        self.size += 1

    def remove(self):
        temp = self.head
        if temp:
            self.head = temp.next
            temp = None
            self.size -= 1
        else:
            raise ValueError("List is already empty!")

    def is_empty(self):
        return self.head is None

    def length(self):
        return self.size

    def get(self):
        return self.head.data

    def print_list(self):
        temp = self.head
        while temp:
            print(temp.get_data())
            temp = temp.next

    def append(self, elem_data):
        elem = Element(elem_data)
        if self.head is None:
            self.head = elem
        else:
            if self.size > 2:
                temp = self.head
                for i in range(self.size - 1):
                    temp = temp.next
                temp.set_next(elem)
            elif self.size == 2:
                self.head.next.set_next(elem)
            elif self.size == 1:
                self.head.set_next(elem)

        self.size += 1

    def pop(self):
        if self.head is None:
            raise ValueError("List is already empty!")
        else:
            if self.size == 1:
                self.destroy()
            elif self.size == 2:
                self.head.set_next(None)
                self.size -= 1
            else:
                temp = self.head
                for i in range(self.size - 2):
                    temp = temp.next
                temp.set_next(None)
                self.size -= 1

    def reverse(self):
        if self.head is None:
            raise ValueError("List is empty!")
        else:
            elem = self.head
            prev_elem = None
            next_elem = self.head.get_next()
            while elem:
                elem.set_next(prev_elem)
                prev_elem = elem
                elem = next_elem
                if next_elem:
                    next_elem = next_elem.get_next()

            self.head = prev_elem

    def take(self, n):
        new_list = List()
        temp = self.head
        for i in range(n):
            if i > self.size:
                break
            new_list.append(temp.get_data())
            temp = temp.get_next()
        return new_list

    def drop(self, n):
        new_list = List()
        temp = self.head
        for i in range(self.size):
            if i + 1 > n:
                new_list.append(temp.get_data())
            temp = temp.get_next()

        return new_list


def main():
    my_list = List()

    my_list.add(('UP', 'Poznań', 1919))
    my_list.add(('UW', 'Warszawa', 1915))
    my_list.add(('PW', 'Warszawa', 1915))
    my_list.add(('UJ', 'Kraków', 1364))
    my_list.add(('AGH', 'Kraków', 1919))
    my_list.append(('PG', 'Gdańsk', 1945))

    my_list.print_list()

    print("\nLiczba elementów (length()):", my_list.length())
    print("\nCzy lista jest pusta? (is_empty())", my_list.is_empty())

    my_list.reverse()
    print("\nlista odwrócona (reverse()):")
    my_list.print_list()

    print('\nhead (get()):', my_list.get())

    print("\npo usunięciu elementu z początku (remove()):")
    my_list.remove()
    my_list.print_list()

    print("\npo usunięciu elementu z końca (pop()):")
    my_list.pop()
    my_list.print_list()

    print("\npierwsze 2 elementy listy (take(2)):")
    my_list.take(2).print_list()

    print("\nLista z pominięciem jej pierwszych dwóch elementów (drop()):")
    my_list.drop(2).print_list()

    my_list.destroy()
    print("\nPo usunięciu listy destroy() - Czy lista jest pusta?", my_list.is_empty())


main()
