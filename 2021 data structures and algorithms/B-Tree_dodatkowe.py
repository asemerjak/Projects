class Element:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf

    def __str__(self):
        return str(self.keys)

    def size(self):
        return len(self.keys)


class BTree:
    def __init__(self, max_keys):
        self.head = Element(True)
        self.max_keys = max_keys

    def insert(self, new_key):
        head = self.head
        if head.size() == self.max_keys:
            temp = Element()
            self.head = temp
            temp.children.insert(0, head)
            self.split_node(temp, 0)
            self.insert_in_node(temp, new_key)
        else:
            self.insert_in_node(head, new_key)

    def insert_in_node(self, node, new_key):
        i = len(node.keys) - 1
        if node.is_leaf:
            node.keys.append(0)
            while i >= 0 and new_key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = new_key
        else:
            while i >= 0 and new_key < node.keys[i]:
                i -= 1
            i += 1
            if node.children[i].size() == self.max_keys:
                self.split_node(node, i)
                if new_key > node.keys[i]:
                    i += 1
            self.insert_in_node(node.children[i], new_key)

    def split_node(self, node, i):
        min_children = (self.max_keys+1)//2
        child = node.children[i]
        new_node = Element(child.is_leaf)

        node.children.insert(i+1, new_node)
        node.keys.insert(i, child.keys[int(min_children - 1)])
        new_node.keys = child.keys[int(min_children): int(self.max_keys)]
        child.keys = child.keys[0: int(min_children - 1)]

        if not child.is_leaf:
            new_node.children = child.children[int(min_children): int(self.max_keys + 1)]
            child.children = child.children[0: int(min_children)]

    def print_tree(self):
        print("==============")
        self._print_tree(self.head, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node.size() > 0:
            for i in range(node.size()+1):
                if len(node.children) > 0:
                    self._print_tree(node.children[i], lvl+1)
                if i < node.size():
                    print(lvl*'  ', node.keys[i])


def main():
    my_btree = BTree(3)
    keys = [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]
    for key in keys:
        my_btree.insert(key)
    print("Drzewo z wartościami dodanymi w pomieszanej kolejności(0-19):")
    my_btree.print_tree()

    my_btree2 = BTree(3)
    for key in range(20):
        my_btree2.insert(key)
    print("\n\nDrzewo z wartościami uporządkowanymi rosnąco (0-19):") # drzewo wyższe o jeden poziom niż poprzednio
    my_btree2.print_tree()

    my_btree3 = BTree(3)
    for key in range(200):
        my_btree3.insert(key)
    print("\n\nDrzewo z wartościami uporządkowanymi rosnąco (0-199):")
    my_btree3.print_tree()

    my_btree4 = BTree(5)
    for key in range(200):
        my_btree4.insert(key)
    print("\n\nDrzewo z wartościami uporządkowanymi rosnąco (0-199) (max kluczy = 5):") # wysokość drzewa znacznie zmalała
    my_btree4.print_tree()

    
main()



