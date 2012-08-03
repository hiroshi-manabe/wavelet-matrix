#!/usr/bin/env python
#
# Copyright (c) 2012 Hiroshi Manabe (manabe.hiroshi@gmail.com)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above Copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above Copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the authors nor the names of its contributors
#    may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
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
                self._wavelet_matrix[i].Add(bit)
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

    def Access(self, pos):
        if pos < 0 or pos >= self._length:
            raise ValueError

        index = pos
        num = 0

        for i in range(self._bits):
            bit = self._wavelet_matrix[i].Peek(index)
            num |= bit << i

            index = self._wavelet_matrix[i].Rank(bit, index)

            index += self._zero_counts[i] * bit

        return num

    def Rank(self, num, pos):
        if num < 0 or num >= (1 << self._bits):
            raise ValueError

        if pos < 0 or pos > self._length:
            raise ValueError

        if pos == 0:
            return 0

        if self._pos_cache[num+1] == self._pos_cache[num]:
            return 0

        index = pos

        for i in range(self._bits):
            bit = 1 if num & (1 << i) else 0

            index = self._wavelet_matrix[i].Rank(bit, index)

            index += self._zero_counts[i] * bit
        
        return index - self._pos_cache[num]

    def Select(self, num, rank):
        if num < 0 or num >= (1 << self._bits):
            raise ValueError

        if rank < 0:
            raise ValueError

        if rank == 0:
            return 0

        if rank > self._pos_cache[num+1] - self._pos_cache[num]:
            return -1

        index = self._pos_cache[num] + rank

        for i in reversed(range(self._bits)):
            bit = 1 if num & (1 << i) else 0

            index -= self._zero_counts[i] * bit

            index = self._wavelet_matrix[i].Select(bit, index)

        return index
