
class Tree:

    def __init__(self, parent=None):

        self.parent = parent
        self.metadata = []
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_metadata(self, metadata):
        self.metadata = metadata[:]

    def sum_metadata(self):

        total = sum(self.metadata)

        for child in self.children:
            total += child.sum_metadata()

        return total

    def value(self):

        if not self.children:
            return self.sum_metadata()

        return sum(self.children[idx - 1].value() for idx in self.metadata if idx - 1 < len(self.children))


def process_node(data, parent=None):

    n_childs = data[0]
    n_metadata = data[1]

    data = data[2:]

    tree = Tree(parent=parent)
    for _ in range(n_childs):
        child, data = process_node(data, tree)
        tree.children.append(child)

    tree.add_metadata(data[:n_metadata])
    data = data[n_metadata:]

    return tree, data


with open('input_data') as in_f:
    raw_data = list(map(int, next(in_f).split()))

tree, _ = process_node(raw_data)
solution = tree.sum_metadata()
solution2 = tree.value()

print(f'P8-1: {solution}')
print(f'P8-2: {solution2}')
