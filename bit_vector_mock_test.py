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

    def test_peek(self):
        self.assertEqual(self.bit_vector.Peek(7), 0)
        self.assertEqual(self.bit_vector.Peek(15), 1)
        self.assertEqual(self.bit_vector.Peek(23), 0)
        self.assertEqual(self.bit_vector.Peek(31), 1)
        self.assertRaises(ValueError, self.bit_vector.Peek, 32)
        self.assertRaises(ValueError, self.bit_vector.Peek, -1)

    def test_rank(self):
        self.assertEqual(self.bit_vector.Rank(0, 8), 4)
        self.assertEqual(self.bit_vector.Rank(1, 16), 7)
        self.assertEqual(self.bit_vector.Rank(0, 24), 12)
        self.assertEqual(self.bit_vector.Rank(1, 32), 14)
        self.assertRaises(ValueError, self.bit_vector.Rank, 3, 16)
        self.assertRaises(ValueError, self.bit_vector.Rank, 0, 33)
        self.assertRaises(ValueError, self.bit_vector.Rank, 0, -1)

    def test_select(self):
        self.assertEqual(self.bit_vector.Select(0, 4), 8)
        self.assertEqual(self.bit_vector.Select(1, 7), 16)
        self.assertEqual(self.bit_vector.Select(0, 12), 24)
        self.assertEqual(self.bit_vector.Select(1, 14), 32)
        self.assertEqual(self.bit_vector.Select(1, 13), 28)
        self.assertEqual(self.bit_vector.Select(1, 15), -1)
        self.assertRaises(ValueError,self.bit_vector.Select, 1, 0)
        self.assertRaises(ValueError,self.bit_vector.Select, 3, 5)
        self.assertRaises(ValueError, self.bit_vector.Select, 0, -1)

    def test_length(self):
        self.assertEqual(self.bit_vector.GetLength(), 32)



suite = unittest.TestLoader().loadTestsFromTestCase(BitVectorMockTest)

unittest.TextTestRunner(verbosity=2).run(suite)
