#!/usr/bin/env python

class BitVectorMock(object):
    def __init__(self, size):
        self._bytearray = bytearray(size + 7 / 8)
        self._bit_len = size

    def Set(self, pos, bit):
        if pos >= self._bit_len:
            raise ValueError

        if bit not in (0, 1):
            raise ValueError

        self._bytearray[pos / 8] |= bit << (pos % 8)

    def Peek(self, pos):
        if pos < 0 or pos >= self._bit_len:
            raise ValueError

        return 1 if (self._bytearray[(pos / 8)] & (1 << pos % 8)) else 0

    def GetLength(self):
        return self._bit_len

    def Rank(self, bit, pos):
        if bit not in (0, 1):
            raise ValueError

        if pos < 0:
            raise ValueError

        rank = 0

        for i in range(pos):
            if self.Peek(i) == bit:
                rank += 1

        return rank

    def Select(self, bit, rank):
        if bit not in (0, 1):
            raise ValueError

        if rank <= 0:
            return -1

        pos = 0

        r = 0
        for i in range(self._bit_len):
            if self.Peek(i) == bit:
                r += 1
                if rank == r:
                    return i + 1

        return -1
