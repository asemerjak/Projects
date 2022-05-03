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


def nil():
    return None


def cons(new_data, lst):
    elem = Element(new_data)
    elem.set_next(lst)
    return elem


def first(lst):
    return lst.get_data()


def rest(lst):
    return lst.next


def create():
    return nil()


def destroy(lst):
    lst = None
    return lst


def add(el, lst):
    return cons(el, lst)


def remove(lst):
    if lst is None:
        raise ValueError("List is already empty!")
    return rest(lst)


def is_empty(lst):
    return lst is None


def length(lst, cnt = 0):
    if lst is None:
        return cnt
    rest_lst = rest(lst)
    cnt += 1
    if rest_lst is None:
        return cnt
    return length(rest_lst, cnt)


def get(lst):
    if lst is None:
        raise ValueError("List is empty!")
    return first(lst)


def print_list(lst):
    if lst is None:
        return
    print(first(lst))
    rest_lst = rest(lst)
    print_list(rest_lst)


def append(el, lst):
    if lst is None:
        return cons(el, lst)
    else:
        first_el = first(lst)
        rest_lst = rest(lst)
        return cons(first_el, append(el, rest_lst))


def pop(lst):
    if lst is None:
        raise ValueError("List is already empty!")
    if rest(lst) is None:
        return remove(lst)
    else:
        first_el = first(lst)
        rest_lst = rest(lst)
        return cons(first_el, pop(rest_lst))


def reverse(lst, new_list = nil()):
    if lst is None:
        return new_list
    new_list = cons(first(lst), new_list)
    rest_lst = rest(lst)
    return reverse(rest_lst, new_list)


def take(n, lst):
    size = length(lst)
    if n >= size:
        return lst
    return take(n, pop(lst))


def drop(n, lst, counter = 0):
    size = length(lst)
    if n >= size and counter == 0:
        return nil()
    if counter == n:
        return lst
    lst = rest(lst)

    return drop(n, lst, counter+1)


def main():
    my_list = nil()

    my_list = add(('UP', 'Poznań', 1919), my_list)
    my_list = add(('UW', 'Warszawa', 1915), my_list)
    my_list = add(('PW', 'Warszawa', 1915), my_list)
    my_list = add(('UJ', 'Kraków', 1364), my_list)
    my_list = add(('AGH', 'Kraków', 1919), my_list)

    my_list = append(('PG', 'Gdańsk', 1945), my_list)

    print_list(my_list)

    print("\nLiczba elementów (length()):", length(my_list))
    print("\nCzy lista jest pusta? (is_empty())", is_empty(my_list))

    my_list = reverse(my_list)
    print("\nlista odwrócona (reverse()):")
    print_list(my_list)

    print('\nhead (get()):', get(my_list))

    print("\npo usunięciu elementu z początku (remove()):")
    my_list = remove(my_list)
    print_list(my_list)

    print("\npo usunięciu elementu z końca (pop()):")
    my_list = pop(my_list)
    print_list(my_list)

    print("\npierwsze 3 elementy listy (take(3)):")
    new_list = take(3, my_list)
    print_list(new_list)

    print("\nLista z pominięciem jej pierwszych dwóch elementów (drop(2)):")
    new_list_2 = drop(2, my_list)
    print_list(new_list_2)

    my_list = destroy(my_list)
    print("\nPo usunięciu listy (destroy()) - Czy lista jest pusta?", is_empty(my_list))


main()
