#!/usr/bin/env python3

################################################################################
# Vigenere cipher 
################################################################################

class TabulaRecta:
    """
    The Vigenère cipher consists of several Caesar ciphers in sequence with
    different shift values. To encrypt, a table of alphabets can be used,
    termed a tabula recta, Vigenère square, or Vigenère table.
    It consists of the alphabet written out 26 times in different rows,
    each alphabet shifted cyclically to the left compared to the previous alphabet,
    corresponding to the 26 possible Caesar ciphers. At different points
    in the encryption process, the cipher uses a different alphabet from one of the rows.
    The alphabet used at each point depends on a repeating keyword.
    """

    def __init__(self):
        self._size = 255
        self._first_last_char = (chr(0), chr(255))
        self._init_row = [chr(c) for c in range(ord(self._first_last_char[0]), ord(self._first_last_char[1]) + 1)]
        self._tabula_recta = self._build_tabula_recta()

    def _build_tabula_recta(self):
        tr = [list(self._init_row)]
        for i in range(1, self._size + 1):
            shifted = self._shift(tr[-1])
            tr.append(shifted)
        return tr

    def _shift(self, row, k=1):
        ord_first_char = ord(self._first_last_char[0])
        ord_last_char = ord(self._first_last_char[1])
        return [chr((ord(c) + k) % (ord_last_char + 1)) 
                if (ord(c) + k) <= ord_last_char
                else chr((ord(c) + k) % (ord_last_char + 1) + ord_first_char)
                for c in row]

    def map_char(self, char):
        # TODO: finish this method
        return 'a'                   # <---------------------------------------

    def __str__(self):
        s = ''
        for r in self._tabula_recta:
            s += ''.join([(str(ord(c)) + ' ') for c in r]) + '\n'
        return s

def main():
    tr = TabulaRecta()
    print(tr)

if __name__ == '__main__':
    main()
