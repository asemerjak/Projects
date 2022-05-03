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


class AVL:
    def __init__(self):
        self.head = None

    def search_helper(self, key):
        node = self.head
        while node is not None:
            if key == node.get_key():
                return node
            node = node.get_left() if key < node.get_key() else node.get_right()
        return node

    def search(self, key):
        return self.search_helper(key).get_data()

    def insert(self, key, data):
        new_elem = Element(key, data)
        temp_parent = None
        temp_child = self.head
        prev = []

        while temp_child is not None:
            temp_parent = temp_child
            if key < temp_child.get_key():
                prev.append((temp_child, "left"))
                temp_child = temp_child.get_left()
            elif key == temp_child.get_key():
                temp_child.set_data(data)
                return
            else:
                prev.append((temp_child, "right"))
                temp_child = temp_child.get_right()

        if temp_parent is None:
            self.head = new_elem
        else:
            if key < temp_parent.get_key():
                temp_parent.set_left(new_elem)
            else:
                temp_parent.set_right(new_elem)

        for i in range(len(prev) - 2): #ide po węzłach w górę sprawdzając balans
            prev_, _ = prev[-1 - i-1]
            balance = self.balance(prev_)
            if balance < -1 or balance > 1:
                prev_parent, side = prev[-1 - i - 1-1]
                if side == 'left':
                    prev_parent.set_left(self.rebalance(prev_))
                else:
                    prev_parent.set_right(self.rebalance(prev_))

        self.head = self.rebalance(self.head)

    def delete(self, key):
        current = self.head
        parent = None
        prev = []
        while current is not None and current.get_key() != key:
            parent = current
            if current.get_key() < key:
                prev.append((current, "right"))
                current = current.get_right()
            else:
                prev.append((current, "left"))
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

        for i in range(len(prev)-2): #ide po węzłach w górę sprawdzając balans
            prev_, _ = prev[-1 - i]
            balance = self.balance(prev_)
            if balance < -1 or balance > 1:
                prev_parent, side = prev[-1 - i-1]
                if side == 'left':
                    prev_parent.set_left(self.rebalance(prev_))
                else:
                    prev_parent.set_right(self.rebalance(prev_))

        self.head = self.rebalance(self.head)

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

    def balance(self, node):
        return self.height(node.left) - self.height(node.right)

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

    def left_rotation(self, node):
        new_root = node.right
        new_root_old_left = new_root.left
        new_root.set_left(node)
        node.set_right(new_root_old_left)
        return new_root

    def right_rotation(self, node):
        new_root = node.left
        new_root_old_right = new_root.right
        new_root.set_right(node)
        node.set_left(new_root_old_right)
        return new_root

    def rebalance(self, node):
        balance = self.balance(node)
        if balance > 1:
            if self.balance(node.left) >= 0:
                return self.right_rotation(node)
            node.set_left(self.left_rotation(node.left))
            return self.right_rotation(node)
        if balance < -1:
            if self.balance(node.right) <= 0:
                return self.left_rotation(node)
            node.set_right(self.right_rotation(node.right))
            return self.left_rotation(node)
        return node



def main():
    my_tree = AVL()
    my_tree.insert(50, "A")
    my_tree.insert(15, "B")
    my_tree.insert(62, "C")
    my_tree.insert(5, "D")
    my_tree.insert(2, "E")
    my_tree.insert(1, "F")
    my_tree.insert(11, "G")
    my_tree.insert(100, "H")
    my_tree.insert(7, "I")
    my_tree.insert(6, "J")
    my_tree.insert(55, "K")
    my_tree.insert(52, "L")
    my_tree.insert(51, "M")
    my_tree.insert(57, "N")
    my_tree.insert(8, "O")
    my_tree.insert(9, "P")
    my_tree.insert(10, "R")
    my_tree.insert(99, "S")
    my_tree.insert(12, "T")
    print("Drzewo - etap początkowy:")
    my_tree.print_tree()
    my_tree.print_keys_vals()

    print("\n\n")
    print("Wartość klucza 10:", my_tree.search(10))

    my_tree.delete(50)
    my_tree.delete(52)
    my_tree.delete(11)
    my_tree.delete(57)
    my_tree.delete(1)
    my_tree.delete(12)
    my_tree.insert(3, "AA")
    my_tree.insert(4, "BB")
    my_tree.delete(7)
    my_tree.delete(8)

    print("\n\nDrzewo - etap końcowy:")
    my_tree.print_keys_vals()
    print("\n\n")
    my_tree.print_tree()


main()
