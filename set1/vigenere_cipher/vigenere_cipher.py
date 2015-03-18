#!/usr/bin/env python3

import argparse
import itertools

################################################################################
# Vigenere cipher encryptr/decryptr
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
        #self._first_last_char = (chr(32), chr(126))
        #self._first_last_char = (chr(65), chr(90))
        self._first_last_char = (chr(97), chr(122))
        self._size = ord(self._first_last_char[1]) - ord(self._first_last_char[0]) + 1
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

    def map_char(self, char, key_char, encrypt=True):
        row_index = ord(char) - ord(self._first_last_char[0])
        col_index = ord(key_char) - ord(self._first_last_char[0])
        ch = self._tabula_recta[row_index][col_index] if encrypt else chr(self._tabula_recta[row_index].index(key_char) + ord(self._first_last_char[0]))
        #print('Mapping {0} -> {1} (row={2}; col={3})'.format(char, ord(ch), row_index, col_index))
        return ch

    def __str__(self):
        s = ''
        for r in self._tabula_recta:
            s += ''.join(['{0:3} '.format(str(ord(c))) for c in r]) + '\n'
        return s


def crypt(message, key, encrypt=True):
    """Either encrypt or decrypt the message"""

    def extend_key(message, key):
        """
        Extend the key.
        If we want to encrypt 'message' with the key 'key',
        we need to extend the key to match the message:
        message:    'message'
        ext key:    'keykeyk'
        """
        ext_key = ''
        for pair in itertools.zip_longest(message, itertools.cycle(key)):
            if pair[0] is None: break
            ext_key += pair[1]
        return ext_key

    tr = TabulaRecta()
    ext_key = extend_key(message, key)
    msg = ''
    for pair in zip(message, ext_key):
        msg += tr.map_char(pair[0], pair[1], encrypt) if encrypt else tr.map_char(pair[1], pair[0], encrypt)
    return msg


def encrypt_wrapper(args):
    print('Encrypting message [{0}] with key [{1}]'.format(args.message, args.key))
    print(crypt(args.message, args.key))


def decrypt_wrapper(args):
    print('Decrypting message [{0}] with key [{1}]'.format(args.message, args.key))
    print(crypt(args.message, args.key, encrypt=False))


def main():
    parser = argparse.ArgumentParser(prog='Vigenere cipher')
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'

    ############################################################################
    # Parser for "encrypt" command
    ############################################################################
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt message using Vigenere cipher')
    encrypt_parser.add_argument('-m', '--message', type=str, required=True, help='Message to encrypt')
    encrypt_parser.add_argument('-k', '--key', type=str, required=True, help='Key to encrypt the message with')
    encrypt_parser.set_defaults(func=encrypt_wrapper)

    ############################################################################
    # Parser for "decrypt" command
    ############################################################################
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt message encrypted with Vigenere cipher')
    decrypt_parser.add_argument('-m', '--message', type=str, required=True, help='Message to encrypt')
    decrypt_parser.add_argument('-k', '--key', type=str, required=True, help='Key to encrypt the message with')
    decrypt_parser.set_defaults(func=decrypt_wrapper)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
