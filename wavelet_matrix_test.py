#!/usr/bin/env python

import unittest
from wavelet_matrix import WaveletMatrix

class WaveletMatrixTest(unittest.TestCase):
    def setUp(self):
        self.wavelet_matrix = WaveletMatrix(
            4 ,
            [11,  0, 15,  6,  5,  2,  7, 12,
             11,  0, 12, 12, 13,  4,  6, 13,
              1, 11,  6,  1,  7, 10,  2,  7,
             14, 11,  1,  7,  5,  4, 14,  6])

    def test_rank(self):
        self.assertEqual(self.wavelet_matrix.Rank(7, 24), 3)
        self.assertEqual(self.wavelet_matrix.Rank(7, 23), 2)
        self.assertEqual(self.wavelet_matrix.Rank(11, 31), 4)
        self.assertEqual(self.wavelet_matrix.Rank(0, 32), 2)
        self.assertEqual(self.wavelet_matrix.Rank(11, 0), 0)
        self.assertRaises(ValueError, self.wavelet_matrix.Rank, 136, 16)
        self.assertRaises(ValueError, self.wavelet_matrix.Rank, -5, 24)
        self.assertRaises(ValueError, self.wavelet_matrix.Rank, 0, 33)

    def test_select(self):
        self.assertEqual(self.wavelet_matrix.Select(7, 3), 24)
        self.assertEqual(self.wavelet_matrix.Select(7, 2), 21)
        self.assertEqual(self.wavelet_matrix.Select(11, 4), 26)
        self.assertEqual(self.wavelet_matrix.Select(0, 2), 10)
        self.assertEqual(self.wavelet_matrix.Select(11, 0), 0)
        self.assertEqual(self.wavelet_matrix.Select(11, 5), -1)
        self.assertRaises(ValueError, self.wavelet_matrix.Select, 136, 2)
        self.assertRaises(ValueError, self.wavelet_matrix.Select, -5, 1)

suite = unittest.TestLoader().loadTestsFromTestCase(WaveletMatrixTest)

unittest.TextTestRunner(verbosity=2).run(suite)
