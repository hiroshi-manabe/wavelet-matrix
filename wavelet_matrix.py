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

        self._bit_reverse_table = []
        for i in range(max_value):
            rev = 0
            for j in range(bits):
                rev |= ((i & (1 << j)) >> j) << (bits - j - 1)

            self._bit_reverse_table.append(rev)

        for n in array:
            if n >= max_value:
                raise ValueError

        self._length = len(array)

        cur_array = array
        self._wavelet_matrix = []
        self._zero_counts = []
        self._pos_cache = []

        for i in range(bits):
            test_bit = 1 << (bits - i - 1)
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
            while self._bit_reverse_table[cur_array[i]] >= n:
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
            num <<= 1
            num |= bit

            index = self._wavelet_matrix[i].Rank(bit, index)

            if bit:
                index += self._zero_counts[i]

        return num

    def Rank(self, num, pos):
        if num < 0 or num >= (1 << self._bits):
            raise ValueError

        if pos < 0 or pos > self._length:
            raise ValueError

        if pos == 0:
            return 0

        num_rev = self._bit_reverse_table[num]

        if (self._pos_cache[num_rev+1]  == self._pos_cache[num_rev]):
            return 0

        index = pos

        for i in range(self._bits):
            bit = 1 if num & (1 << (self._bits - i - 1)) else 0

            index = self._wavelet_matrix[i].Rank(bit, index)

            if bit:
                index += self._zero_counts[i]
        
        return index - self._pos_cache[num_rev]

    def RankLessThan(self, num, pos):
        (less, more, rank) = self.RankAll(num, 0, pos)
        return less

    def RankMoreThan(self, num, pos):
        (less, more, rank) = self.RankAll(num, 0, pos)
        return more

    def RankAll(self, num, begin_pos, end_pos):
        if num < 0 or num >= (1 << self._bits):
            raise ValueError

        if (begin_pos < 0 or begin_pos > self._length
            or end_pos < 0 or end_pos > self._length):
            raise ValueError

        if end_pos <= begin_pos:
            return (0, 0, 0)

        more_and_less = [0, 0]

        for i in range(self._bits):
            bit = 1 if num & (1 << self._bits - i - 1) else 0
            range_bits = end_pos - begin_pos

            begin_pos = self._wavelet_matrix[i].Rank(bit, begin_pos)
            end_pos = self._wavelet_matrix[i].Rank(bit, end_pos)
            non_match_bits = range_bits - (end_pos - begin_pos)
            more_and_less[bit] += non_match_bits

            if bit:
                begin_pos += self._zero_counts[i]
                end_pos += self._zero_counts[i]

        return (more_and_less[1], more_and_less[0], end_pos - begin_pos)

    def Select(self, num, rank):
        if num < 0 or num >= (1 << self._bits):
            raise ValueError

        if rank <= 0:
            raise ValueError

        num_rev = self._bit_reverse_table[num]

        if rank > self._pos_cache[num_rev+1] - self._pos_cache[num_rev]:
            return -1

        index = self._pos_cache[num_rev] + rank

        for i in reversed(range(self._bits)):
            bit = 1 if num & (1 << (self._bits - i - 1)) else 0

            if bit:
                index -= self._zero_counts[i]

            index = self._wavelet_matrix[i].Select(bit, index)

        return index

    def QuantileRange(self, begin_pos, end_pos, k):
        if (begin_pos < 0 or begin_pos > self._length
            or end_pos < 0 or end_pos > self._length):
            raise ValueError

        if k < 0 or k >= end_pos - begin_pos:
            raise ValueError

        num = 0

        for i in range(self._bits):
            begin_zero = self._wavelet_matrix[i].Rank(0, begin_pos)
            end_zero = self._wavelet_matrix[i].Rank(0, end_pos)
            zero_bits = end_zero - begin_zero

            bit = 0 if k < zero_bits else 1

            if bit:
                k -= zero_bits
                begin_pos += self._zero_counts[i] - begin_zero
                end_pos += self._zero_counts[i] - end_zero
            else:
                begin_pos = begin_zero
                end_pos = end_zero

            num |= bit << (self._bits - i - 1)

        return (num, self.Select(num, k+1) - 1)


