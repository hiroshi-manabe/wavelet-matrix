#!/usr/bin/env python

class BitVectorMock(object):
    def __init__(self, bit_array=[]):
        self._bytearray = bytearray()
        self._bit_len = 0

        for b in bit_array:
            self.AddBit(b)

    def AddBit(self, bit):
        if bit not in (0, 1):
            raise ValueError

        if (self._bit_len % 8) == 0:
            self._bytearray.append(0)

        self._bytearray[-1] |= bit << (self._bit_len % 8)
        self._bit_len += 1

    def PeekBit(self, pos):
        if pos < 0 or pos >= self._bit_len:
            raise ValueError

        return 1 if (self._bytearray[(pos / 8)] & (1 << pos % 8)) else 0

    def GetLength(self):
        return self._bit_len

    def Rank(self, bit, pos):
        if pos < 0:
            raise ValueError

        rank = 0

        for i in range(pos):
            if self.PeekBit(i) == bit:
                rank += 1

        return rank

    def Concatinate(self, another):
        left_shift = (self._bit_len + 7) % 8 + 1
        right_shift = 8 - left_shift

        for i in range((another._bit_len + 7) / 8):
            if right_shift:
                self._bytearray[-1] |= (another._bytearray[i]
                                        << left_shift) % 256
            self._bytearray.append(another._bytearray[i] >> right_shift)

        self._bit_len += another._bit_len

    def Equals(self, another):
        if self._bit_len != another._bit_len:
            return False

        for i in range(self._bit_len):
            if self.PeekBit(i) != another.PeekBit(i):
                return False

        return True
