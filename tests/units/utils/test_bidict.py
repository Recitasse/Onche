import unittest
from utils.bidict.bidict import BiDict


class MyTestCase(unittest.TestCase):
    def test_declaration(self):
        bid_dic = BiDict()
        bid_dic.update({'value': 1, 'test': 'apple'})
        with self.assertRaises(ValueError):
            bid_dic.update({1: 'value'})
        self.assertEqual(bid_dic, {'value': 1, 'test': 'apple', 1: 'value', 'apple': 'test'})

    def test_pop(self):
        bid_dic = BiDict()
        bid_dic.update({'value': 1, 'test': 'apple'})
        self.assertEqual(bid_dic, {'value': 1, 'test': 'apple', 1: 'value', 'apple': 'test'})
        bid_dic.pop('value')
        self.assertEqual(bid_dic, {'test': 'apple', 'apple': 'test'})
