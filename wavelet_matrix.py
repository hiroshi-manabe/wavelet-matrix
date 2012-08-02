#!/usr/bin/env python

from bit_vector_mock import BitVectorMock

class WaveletMatrix(object):
    def __init__(self, bits, array):
        if bits < 0:
            raise ValueError

        self._bits = bits

        max_value = 1 << bits

        for n in array:
            if n >= max_value:
                raise ValueError

        self._length = len(array)

        cur_array = array
        self._wavelet_matrix = []
        self._zero_counts = []

        for i in range(bits):
            test_bit = 1 << (bits - i - 1)
            next_array = [[], []]
            self._wavelet_matrix.append(BitVectorMock())

            for n in cur_array:
                bit = 1 if (n & test_bit) else 0
                self._wavelet_matrix[i].AddBit(bit)
                next_array[bit].append(n)

            self._zero_counts.append(len(next_array[0]))

            cur_array = next_array[0] + next_array[1]


    def Rank(self, num, pos):

        if num < 0 or num >= (1 << self._bits):
            raise ValueError

        if pos < 0 or pos > self._length:
            raise ValueError

        lower_bound = 0
        upper_bound = pos
        prev_bit = 0

        for i in range(self._bits):
            bit = 1 if num & (1 << (self._bits - i - 1)) else 0
            if prev_bit:
                lower_bound += self._zero_counts[i-1]
                upper_bound += self._zero_counts[i-1]

            upper_bound = self._wavelet_matrix[i].Rank(bit, upper_bound)
            lower_bound = self._wavelet_matrix[i].Rank(bit, lower_bound)

            prev_bit = bit
        
        return upper_bound - lower_bound
