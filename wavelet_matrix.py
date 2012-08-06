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
        def get_reversed_first_bits(num, max_bit, bit_num, bit_reverse_table):
            return bit_reverse_table[num & ((1 << max_bit) -
                                            (1 << (max_bit - bit_num)))]

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
        self._node_begin_pos = [0] * bits
        self._node_begin_pos[bits-1] = []

        for i in range(len(cur_array)):
            while self._bit_reverse_table[cur_array[i]] >= n:
                self._node_begin_pos[-1].append(i)
                n += 1

        # self._node_begin_pos[bits-1][max_value] is a sentinel
        while n <= max_value:
            self._node_begin_pos[-1].append(self._length)
            n += 1

        for i in reversed(range(bits-1)):
            self._node_begin_pos[i] = []
            pos = 0
            for j in range(1 << (i+1)):
                self._node_begin_pos[i].append(pos)
                pos += (self._node_begin_pos[i+1][j+1] -
                        self._node_begin_pos[i+1][j] +
                        self._node_begin_pos[i+1][j + (1 << (i+1)) + 1] -
                        self._node_begin_pos[i+1][j + (1 << (i+1))])

            self._node_begin_pos[i].append(pos)


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
        (less, more, rank) = self.RankAll(num, pos)
        return rank

    def RankLessThan(self, num, pos):
        (less, more, rank) = self.RankAll(num, pos)
        return less

    def RankMoreThan(self, num, pos):
        (less, more, rank) = self.RankAll(num, pos)
        return more

    def RankAll(self, num, pos):
        if num < 0 or num >= (1 << self._bits):
            raise ValueError

        if pos < 0 or pos > self._length:
            raise ValueError

        if pos == 0:
            return (0, 0, 0)

        more_and_less = [0, 0]
        node_num = 0
        node_begin_pos = 0

        for i in range(self._bits):
            bit = 1 if num & (1 << self._bits - i - 1) else 0
            range_bits = pos - node_begin_pos

            node_num |= bit << i
            node_begin_pos = self._node_begin_pos[i][node_num]
            pos = self._wavelet_matrix[i].Rank(bit, pos)
            if bit:
                pos += self._zero_counts[i]

            non_match_bits = range_bits - (pos - node_begin_pos)
            more_and_less[bit] += non_match_bits

        return (more_and_less[1], more_and_less[0],
                pos - node_begin_pos)

    def Select(self, num, rank):
        if num < 0 or num >= (1 << self._bits):
            raise ValueError

        if rank <= 0:
            raise ValueError

        num_rev = self._bit_reverse_table[num]

        if (rank > self._node_begin_pos[self._bits - 1][num_rev+1] -
            self._node_begin_pos[-1][num_rev]):
            return -1

        index = self._node_begin_pos[-1][num_rev] + rank

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
        from_zero = True if begin_pos == 0 else False
        node_num = 0

        for i in range(self._bits):
            if from_zero:
                begin_zero = self._node_begin_pos[i][node_num]
            else:
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

            node_num |= bit << i
            num |= bit << (self._bits - i - 1)

        return (num, self.Select(
                num, begin_pos + k -
                self._node_begin_pos[-1][self._bit_reverse_table[num]] + 1) - 1)


