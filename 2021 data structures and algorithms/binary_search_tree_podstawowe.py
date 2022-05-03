class Element:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

    def get_key(self):
        return self.key

    def set_key(self, new_key):
        self.key = new_key

    def get_data(self):
        return self.data

    def set_data(self, new_data):
        self.data = new_data

    def get_right(self):
        return self.right

    def set_right(self, new_right):
        self.right = new_right

    def get_left(self):
        return self.left

    def set_left(self, new_left):
        self.left = new_left


class BST:
    def __init__(self):
        self.head = None

    def find_elem(self, key, elem=0):
        if elem == 0:
            elem = self.head
        if elem is None or elem.get_key() == key:
            return elem

        if key < elem.get_key():
            return self.find_elem(key=key, elem=elem.get_left())

        return self.find_elem(key=key, elem=elem.get_right())

    def search(self, key):
        return self.find_elem(key).get_data()

    def insert(self, key, data):
        new_elem = Element(key, data)
        temp_parent = None
        temp_child = self.head

        while temp_child is not None:
            temp_parent = temp_child
            if key < temp_child.get_key():
                temp_child = temp_child.get_left()
            elif key == temp_child.get_key():
                temp_child.set_data(data)
                return
            else:
                temp_child = temp_child.get_right()

        if temp_parent is None:
            self.head = new_elem
        else:
            if key < temp_parent.get_key():
                temp_parent.set_left(new_elem)
            else:
                temp_parent.set_right(new_elem)

    def delete(self, key):
        current = self.head
        parent = None
        while current is not None and current.get_key() != key:
            parent = current
            if current.get_key() < key:
                current = current.get_right()
            else:
                current = current.get_left()

        if current is None:
            print("Your tree doesn't have this key!")
            return None

        if current.get_left() is None or current.get_right() is None:
            if current.get_left() is None:
                new_current = current.get_right()
            else:
                new_current = current.get_left()

            if parent is None:
                self.head = new_current

            if current == parent.get_left():
                parent.set_left(new_current)
            else:
                parent.set_right(new_current)

        else:
            parent_of_inorder_successor = None
            inorder_successor = current.get_right()
            while inorder_successor.get_left() is not None:
                parent_of_inorder_successor = inorder_successor
                inorder_successor = inorder_successor.get_left()

            if parent_of_inorder_successor is not None:
                parent_of_inorder_successor.set_left(inorder_successor.get_right())
            else:
                current.set_right(inorder_successor.get_right())

            current.set_key(inorder_successor.get_key())
            current.set_data(inorder_successor.get_data())

    def print_tree(self):
        print("==============")
        self._print_tree(self.head, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            self._print_tree(node.right, lvl + 10)

            print()
            for i in range(10, lvl + 10):
                print(end=" ")
            print(node.key)
            self._print_tree(node.left, lvl + 10)

    def print_keys_vals(self, node=0):
        if node == 0:
            node = self.head
        if node is not None:
            self.print_keys_vals(node.get_left())
            print(node.get_key(), ":", node.get_data(), end=",  ")
            self.print_keys_vals(node.get_right())

    def height(self, node=0):
        if node == 0:
            node = self.head
        if node is None:
            return 0
        else:
            left_height = self.height(node.get_left())
            right_height = self.height(node.get_right())

            if left_height > right_height:
                return left_height + 1
            else:
                return right_height + 1


def main():
    my_tree = BST()
    my_tree.insert(50, "A")
    my_tree.insert(15, "B")
    my_tree.insert(62, "C")
    my_tree.insert(5, "D")
    my_tree.insert(20, "E")
    my_tree.insert(58, "F")
    my_tree.insert(91, "G")
    my_tree.insert(3, "H")
    my_tree.insert(8, "I")
    my_tree.insert(37, "J")
    my_tree.insert(60, "K")
    my_tree.insert(24, "L")
    print("Drzewo - etap początkowy:")
    my_tree.print_tree()
    my_tree.print_keys_vals()
    print("\n\n")
    print("Wartość klucza 24:", my_tree.search(24))
    my_tree.insert(15, "AA")
    my_tree.insert(6, "M")
    my_tree.delete(62)
    my_tree.insert(59, "N")
    my_tree.insert(100, "P")
    my_tree.delete(8)
    my_tree.delete(15)
    my_tree.insert(55, "R")
    my_tree.delete(50)
    my_tree.delete(5)
    my_tree.delete(24)
    print("Wysokość drzewa:", my_tree.height())
    print("\n\nDrzewo - etap końcowy:")
    my_tree.print_keys_vals()
    print("\n\n")
    my_tree.print_tree()


main()
