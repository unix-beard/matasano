#!/usr/bin/env python3

################################################################################
# The matasano crypto challenges
# http://cryptopals.com/sets/1/challenges/4/
# Set 1   Challenge 4
# Detect single-character XOR
################################################################################
# One of the 60-character strings in the input file has been encrypted 
# by single-character XOR. Find it. 
# Key:      int=53, char='5'
# Message:  Now that the party is jumping
#
# NOTE: This implementation is strictly sequential
################################################################################

import sys
import string

def find_key(key, tuple_):
    return chr(int(tuple_[0] + tuple_[1], base=16) ^ key)

def decode_with_key(key, s):
    decoded_msg = ''
    for t in zip(s[0::2], s[1::2]):
        decoded_msg += find_key(key, t)

    if len([c for c in decoded_msg if c in string.ascii_letters + ' \n']) == len(decoded_msg):
        print('[*] Trying the key: int: {0}, char: {1}'.format(key, chr(key)))
        print('Decoded message: {0}'.format(decoded_msg))
    

def decode(s):
    print('Decoding [{0}]'.format(s))
    for key in range(0, 256):
        decode_with_key(key, s)

def remove_eol(s):
    """Removes trailing '\n' if there is one"""
    return s[0:len(s) - 1] if s[len(s) - 1] == '\n' else s

def main():
    with open(sys.argv[1], 'r') as f:
        for encoded_str in f:
            decode(remove_eol(encoded_str))

if __name__ == '__main__':
    main()
