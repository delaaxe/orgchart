import json
import unittest

from orgchart import data

tree = data.load_mock_tree()


def max_depth(node):
    if not node or not node.children:
        return 0
    depths = (max_depth(child) for child in node.children)
    return max(depths) + 1


def dump(node):
    print(json.dumps(tree.to_orgchart_dict(node), indent=2))


class MyTestCase(unittest.TestCase):
    def test_entourage_distance_0(self):
        node = tree.get_entourage('Lao Lao', 0)
        self.assertEqual(len(node.children), 0)

        node = tree.get_entourage('Bo Miao', 0)
        self.assertEqual(len(node.children), 0)

        node = tree.get_entourage('Joan', 0)
        self.assertEqual(len(node.children), 0)

    def test_entourage_distance_1(self):
        node = tree.get_entourage('Lao Lao', 1)
        self.assertEqual(node.value, 'Lao Lao')
        self.assertEqual(len(node.children), 8)
        self.assertEqual(max_depth(node), 1)

        node = tree.get_entourage('Bo Miao', 1)
        self.assertEqual(node.value, 'Lao Lao')
        self.assertEqual(max_depth(node), 2)

        node = tree.get_entourage('Joan', 1)
        self.assertEqual(node.value, 'Jennifer')
        self.assertEqual(max_depth(node), 1)


    def test_entourage_distance_2(self):
        node = tree.get_entourage('Lao Lao', 2)
        self.assertEqual(node.value, 'Lao Lao')
        self.assertEqual(max_depth(node), 2)

        node = tree.get_entourage('Bo Miao', 2)
        self.assertEqual(node.value, 'Lao Lao')
        self.assertEqual(max_depth(node), 3)

        node = tree.get_entourage('Bessie', 2)
        self.assertEqual(node.value, 'Lao Lao')
        self.assertEqual(max_depth(node), 4)

        node = tree.get_entourage('Jacko', 2)
        self.assertEqual(node.value, 'Bo Miao')
        self.assertEqual(max_depth(node), 3)

if __name__ == '__main__':
    unittest.main()
