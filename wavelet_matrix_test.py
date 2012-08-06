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

    def test_access(self):
        self.assertEqual(self.wavelet_matrix.Access(24), 14)
        self.assertEqual(self.wavelet_matrix.Access(23), 7)
        self.assertEqual(self.wavelet_matrix.Access(31), 6)
        self.assertEqual(self.wavelet_matrix.Access(0), 11)
        self.assertRaises(ValueError, self.wavelet_matrix.Access, 136)
        self.assertRaises(ValueError, self.wavelet_matrix.Access, -5)
        self.assertRaises(ValueError, self.wavelet_matrix.Access, 32)

    def test_rank(self):
        self.assertEqual(self.wavelet_matrix.Rank(7, 24), 3)
        self.assertEqual(self.wavelet_matrix.Rank(7, 23), 2)
        self.assertEqual(self.wavelet_matrix.Rank(11, 31), 4)
        self.assertEqual(self.wavelet_matrix.Rank(0, 32), 2)
        self.assertEqual(self.wavelet_matrix.Rank(15, 0), 0)
        self.assertRaises(ValueError, self.wavelet_matrix.Rank, 136, 16)
        self.assertRaises(ValueError, self.wavelet_matrix.Rank, -5, 24)
        self.assertRaises(ValueError, self.wavelet_matrix.Rank, 0, 33)

    def test_rank_less_than(self):
        self.assertEqual(self.wavelet_matrix.RankLessThan(8, 8), 5)
        self.assertEqual(self.wavelet_matrix.RankLessThan(12, 16), 10)
        self.assertEqual(self.wavelet_matrix.RankLessThan(5, 24), 7)
        self.assertEqual(self.wavelet_matrix.RankLessThan(14, 32), 29)
        self.assertEqual(self.wavelet_matrix.RankLessThan(13, 0), 0)
        self.assertRaises(ValueError, self.wavelet_matrix.RankLessThan, 136, 2)
        self.assertRaises(ValueError, self.wavelet_matrix.RankLessThan, -5, 1)

    def test_rank_more_than(self):
        self.assertEqual(self.wavelet_matrix.RankMoreThan(8, 8), 3)
        self.assertEqual(self.wavelet_matrix.RankMoreThan(12, 16), 3)
        self.assertEqual(self.wavelet_matrix.RankMoreThan(5, 24), 16)
        self.assertEqual(self.wavelet_matrix.RankMoreThan(14, 32), 1)
        self.assertEqual(self.wavelet_matrix.RankMoreThan(13, 0), 0)
        self.assertRaises(ValueError, self.wavelet_matrix.RankMoreThan, 136, 2)
        self.assertRaises(ValueError, self.wavelet_matrix.RankMoreThan, -5, 1)

    def test_select(self):
        self.assertEqual(self.wavelet_matrix.Select(7, 3), 24)
        self.assertEqual(self.wavelet_matrix.Select(7, 2), 21)
        self.assertEqual(self.wavelet_matrix.Select(11, 4), 26)
        self.assertEqual(self.wavelet_matrix.Select(0, 2), 10)
        self.assertEqual(self.wavelet_matrix.Select(11, 5), -1)
        self.assertRaises(ValueError, self.wavelet_matrix.Select, 11, 0)
        self.assertRaises(ValueError, self.wavelet_matrix.Select, 136, 2)
        self.assertRaises(ValueError, self.wavelet_matrix.Select, -5, 1)

    def test_quantile_range(self):
        self.assertEqual(self.wavelet_matrix.QuantileRange(0, 8, 2), (5, 4))
        self.assertEqual(self.wavelet_matrix.QuantileRange(8, 16, 6), (13, 12))
        self.assertEqual(self.wavelet_matrix.QuantileRange(20, 32, 11),
                         (14, 30))
        self.assertEqual(self.wavelet_matrix.QuantileRange(10, 26, 0), (1, 16))
        self.assertEqual(self.wavelet_matrix.QuantileRange(0, 23, 9), (6, 14))
        self.assertRaises(ValueError, self.wavelet_matrix.QuantileRange,
                          20, 32, 12)
        self.assertRaises(ValueError, self.wavelet_matrix.QuantileRange,
                          -5, 1, 3)
        self.assertRaises(ValueError, self.wavelet_matrix.QuantileRange,
                          15, 33, 3)
        self.assertRaises(ValueError, self.wavelet_matrix.QuantileRange,
                          15, 20, -1)

suite = unittest.TestLoader().loadTestsFromTestCase(WaveletMatrixTest)

unittest.TextTestRunner(verbosity=2).run(suite)
