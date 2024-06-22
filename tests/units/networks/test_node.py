import unittest
from tools.tools.networks.Node import Node


class TestNode(unittest.TestCase):
    def setUp(self):
        self.n1 = Node(10.0, 'test')
        self.n2 = Node(20.0, 'test2')

    def tearDown(self):
        Node.reset_ids()

    def test_declaration_properties(self):
        self.assertEqual(self.n1.nom, 'test')
        self.assertAlmostEqual(self.n1.poids, 10.0)

        self.assertEqual(self.n2.nom, 'test2')
        self.assertAlmostEqual(self.n2.poids, 20.0)

        self.n1.positions = (20, 500)
        self.assertEqual(self.n1.position, (20, 500))

    def test_boolean_operator(self):
        self.assertEqual(self.n1 < 11.0, True)
        self.assertEqual(self.n1 <= 10.0, True)
        self.assertEqual(self.n1 >= 10.0, True)
        self.assertEqual(self.n1 > 8.0, True)
        self.assertEqual(self.n1 != 5.0, True)

        self.assertEqual(self.n1 < self.n2, True)

    def test_math_operator(self):
        self.assertAlmostEqual(self.n1 + self.n2, 30.0)
        self.assertAlmostEqual(self.n1 - self.n2, -10.0)

        self.assertAlmostEqual(self.n1 * 10.0, 100.0)
        self.assertAlmostEqual(self.n1 / 10.0, 1.0)
        self.assertAlmostEqual(self.n1 ** 2, 100.0)

    def test_magic_operator(self):
        self.assertAlmostEqual(self.n1, 10.0)
        self.n1 += 10.0
        self.assertAlmostEqual(self.n1, 20.0)
        self.n1 -= self.n2
        self.assertAlmostEqual(self.n1, 0.0)
        self.n1 += 1.0
        self.n1 *= 10.0
        self.assertAlmostEqual(self.n1, 10.0)
        self.n1 /= 10.0
        self.assertAlmostEqual(self.n1, 1.0)

    def test_ids(self):
        self.assertEqual(self.n1.id_, 1)
        self.assertEqual(self.n2.id_, 2)

        del self.n2

        n3 = Node(2, 'test')
        self.assertEqual(n3.NodeId, 3)