#!/usr/bin/env python3

################################################################################
# The matasano crypto challenges
# http://cryptopals.com/sets/1/challenges/2/
# Set 1   Challenge 2
# Fixed XOR
################################################################################
# Write a function that takes two equal-length buffers and produces their 
# XOR combination.
# If your function works properly, then when you feed it the string:
# 1c0111001f010100061a024b53535009181c
# ... after hex decoding, and when XOR'd against:
# 686974207468652062756c6c277320657965
# ... should produce:
# 746865206b696420646f6e277420706c6179
################################################################################

import functools

def decode(tuple_):
    """Decode tuple_'s first and second elements and XOR them."""
    first  = int(tuple_[0], base=16)
    second = int(tuple_[1], base=16)
    return '{:x}'.format(first ^ second)

def fixed_xor(buf1, buf2):
    assert(len(buf1) == len(buf2))
    return functools.reduce(lambda x, y: x + y, map(decode, zip(buf1, buf2)))

def main():
    buf1 = '1c0111001f010100061a024b53535009181c'
    buf2 = '686974207468652062756c6c277320657965'
    res  = '746865206b696420646f6e277420706c6179'
    assert(fixed_xor(buf1, buf2) == res)

if __name__ == '__main__':
    main()
