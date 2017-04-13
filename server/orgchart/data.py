import itertools
from collections import OrderedDict

import attr
from attr import ib as attribute, s as AttributedModel

from orgchart import fixture


@AttributedModel()
class Node:
    value = attribute()
    parent = attribute(default=None, repr=False)
    children = attribute(default=attr.Factory(list))


class Tree:
    def __init__(self, items, id_name='name', parent_name='parent'):
        self.id_name = id_name
        self.parent_name = parent_name
        self.items = {item[self.id_name]: item for item in items}
        self.nodes = {item[self.id_name]: Node(item[self.id_name]) for item in items}
        self.roots = []

    def build(self):
        for item in self.items.values():
            node = self.nodes[item[self.id_name]]
            parent = self.nodes.get(item[self.parent_name])
            if parent:
                node.parent = parent
                parent.children.append(node)

        self.roots = [node for node in self.nodes.values() if not node.parent]

    def clone_children(self, entourage_node, node, distance):
        if distance <= 0 or not node.children:
            return
        for child in node.children:
            entourage_child = Node(child.value, node)
            entourage_node.children.append(entourage_child)
            self.clone_children(entourage_child, child, distance - 1)

    def get_entourage(self, id, distance):
        node = self.nodes[id]
        i = 0
        while node.parent and i < distance:
            node = node.parent
            i += 1
        entourage_node = Node(node.value)
        self.clone_children(entourage_node, node, distance + i)
        return entourage_node

    def to_orgchart_dict(self, node):
        employee = self.items[node.value]
        full_node = self.nodes[node.value]  # arg might be partial view
        return OrderedDict([
            ('name', employee['name']),
            ('title', employee['title']),
            ('relationship', self.get_flags(full_node)),
            ('children', [self.to_orgchart_dict(child) for child in node.children] or None)
        ])

    def get_flags(self, full_node):
        flags = [
            full_node.parent is not None,
            len(full_node.parent.children) > 1 if full_node.parent else False,
            len(full_node.children) > 0
        ]
        return ''.join('1' if flag else '0' for flag in flags)

    def get_children(self, id):
        node = self.nodes.get(id)
        if node:
            return (Node(child.value) for child in node.children)
        return []

    def get_parent(self, id):
        node = self.nodes.get(id)
        if node and node.parent:
            return Node(node.parent.value)
        return []

    def get_siblings(self, id):
        node = self.nodes.get(id)
        if node and node.parent:
            return (Node(child.value) for child in node.parent.children)
        return []

    def get_family(self, id):
        node = self.nodes.get(id)
        if node and node.parent:
            return Node(node.parent.value, children=[
                Node(child.value) for child in node.parent.children
            ])
        return []

    def search(self, query):
        for name in self.items.keys():
            if query.lower() in name.lower():
                yield name


def load_mock_tree():
    tree = Tree(fixture.db)
    tree.build()
    return tree
