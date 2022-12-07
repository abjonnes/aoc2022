class Node:
    def __init__(self, parent, dir_, size=None):
        self.parent = parent
        self.dir = dir_
        self._size = size
        if dir_:
            self.children = dict()

    def process_ls(self, data):
        for info, filename in (x.split() for x in data):
            child = Node(self, True) if info == "dir" else Node(self, False, int(info))
            self.children[filename] = child

    @property
    def size(self):
        if self.dir:
            return sum(child.size for child in self.children.values())
        return self._size


class DataIterator:
    """Processes the data and allows for "peeking" at the next line without consuming it."""

    def __init__(self, data):
        self._iter = (x.strip() for x in data.split("\n") if x.strip())
        self.next = next(self._iter)
        self._stopped = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._stopped:
            raise StopIteration

        return_value = self.next

        try:
            self.next = next(self._iter)
        except StopIteration:
            self._stopped = True
            self.next = None

        return return_value


def build_tree(data):
    current_node = root = Node(None, True)
    iterator = DataIterator(data)
    for line in iterator:
        if line.startswith("$ cd"):
            target = line[5:]
            if target == "/":
                current_node = root
            elif target == "..":
                current_node = current_node.parent
            else:
                current_node = current_node.children[target]
        elif line == "$ ls":
            ls_data = list()
            while iterator.next is not None and not iterator.next.startswith("$"):
                ls_data.append(next(iterator))
            current_node.process_ls(ls_data)
    return root


def get_dirs(root):
    to_visit = [root]
    while to_visit:
        node = to_visit.pop()
        to_visit.extend(child for child in node.children.values() if child.dir)

        yield node


def part1(data):
    root = build_tree(data)

    return sum(dir_.size for dir_ in get_dirs(root) if dir_.size <= 100000)


def part2(data):
    root = build_tree(data)

    return min(
        dir_.size for dir_ in get_dirs(root) if dir_.size >= root.size - 40000000
    )
