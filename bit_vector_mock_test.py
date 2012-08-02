#!/usr/bin/env python

import unittest
import functools

from bit_vector_mock import BitVectorMock

class BitVectorMockTest(unittest.TestCase):
    def setUp(self):
        self.bits = [ 1,  0,  0,  0,  1,  1,  1,  0,
                      1,  0,  0,  0,  0,  1,  0,  1,
                      0,  1,  1,  1,  0,  1,  1,  0, 
                      0,  0,  0,  1,  0,  0,  0,  1,
                      ]
        self.bit_vector = BitVectorMock(self.bits)

    def test_rank(self):
        self.assertEqual(self.bit_vector.Rank(0, 8), 4)
        self.assertEqual(self.bit_vector.Rank(1, 16), 7)
        self.assertEqual(self.bit_vector.Rank(0, 24), 12)
        self.assertEqual(self.bit_vector.Rank(1, 32), 14)
        self.assertRaises(self.bit_vector.Rank(3, 16))
        self.assertRaises(ValueError, self.bit_vector.Rank, 0, 33)
        self.assertRaises(ValueError, self.bit_vector.Rank, 0, -1)

    def test_equals(self):
        another = BitVectorMock(self.bits)
        self.assertTrue(self.bit_vector.Equals(another))

    def test_length(self):
        self.assertEqual(self.bit_vector.GetLength(), 32)

    def test_concat(self):
        data = [
            [1, 0, 0, 0, 1, 1, 1, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [1,  1,  1,  0,  1,  1,  0,  0,  0,  0,  1,  0,  0,  0,  1],
            ]

        b = BitVectorMock()

        for d in data:
            another = BitVectorMock(d)
            b.Concatinate(another)

        self.assertTrue(self.bit_vector.Equals(b))


suite = unittest.TestLoader().loadTestsFromTestCase(BitVectorMockTest)

unittest.TextTestRunner(verbosity=2).run(suite)
