import unittest
from tools.tools.networks.Node import Node
from tools.tools.networks.Edge import Edge


class MyTestCase(unittest.TestCase):
    def tearDown(self):
        Node.reset_ids()

    def setUp(self):
        self.n1 = Node(10.0, 'test')
        self.n2 = Node(20.0, 'test1')
        self.n3 = Node(10.0, 'test2')

        self.e1 = Edge(20.0, liens=[self.n1, (self.n2,)])
        self.e2 = Edge(10.0, liens=[self.n2, (self.n3,)])

    def test_properties(self):
        self.assertAlmostEqual(self.e1.poids, 20.0)

    def test_added_nodes(self):
        self.assertEqual(Edge.ListEdge, {1: [2], 2: [3]})
        n4 = Node(10.0, 'test')
        e3 = Edge(5.0, liens=[self.n1, (n4,)])
        self.assertEqual(Edge.ListEdge, {1: [2, 4], 2: [3]})
        del self.n2
        print(Edge.ListEdge)


if __name__ == '__main__':
    unittest.main()
