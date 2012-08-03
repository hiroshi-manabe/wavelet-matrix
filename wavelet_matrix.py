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
        self._pos_cache = []

        for i in range(bits):
            test_bit = 1 << i
            next_array = [[], []]
            self._wavelet_matrix.append(BitVectorMock())

            for n in cur_array:
                bit = 1 if (n & test_bit) else 0
                self._wavelet_matrix[i].AddBit(bit)
                next_array[bit].append(n)

            self._zero_counts.append(len(next_array[0]))

            cur_array = next_array[0] + next_array[1]

        n = 0
        for i in range(len(cur_array)):
            while cur_array[i] >= n:
                self._pos_cache.append(i)
                n += 1

        # self._pos_cache[max_value] is a sentinel
        while n <= max_value:
            self._pos_cache.append(self._length)
            n += 1

    def Rank(self, num, pos):
        if num < 0 or num >= (1 << self._bits):
            raise ValueError

        if pos < 0 or pos > self._length:
            raise ValueError

        lower_bound = 0
        upper_bound = pos

        for i in range(self._bits):
            bit = 1 if num & (1 << i) else 0

            upper_bound = self._wavelet_matrix[i].Rank(bit, upper_bound)
            lower_bound = self._wavelet_matrix[i].Rank(bit, lower_bound)

            if bit:
                lower_bound += self._zero_counts[i]
                upper_bound += self._zero_counts[i]
        
        return upper_bound - lower_bound

    def Select(self, num, rank):
        if num < 0 or num >= (1 << self._bits):
            raise ValueError

        if rank < 0:
            raise ValueError

        if rank == 0:
            return 0

        if rank > self._pos_cache[num+1] - self._pos_cache[num]:
            return -1

        upper_bound = self._pos_cache[num] + rank

        for i in reversed(range(self._bits)):
            bit = 1 if num & (1 << i) else 0

            if bit:
                upper_bound -= self._zero_counts[i]

            upper_bound = self._wavelet_matrix[i].Select(bit, upper_bound)

        return upper_bound
