#!/usr/bin/env python3

################################################################################
# The matasano crypto challenges
# http://cryptopals.com/sets/1/challenges/3/
# Set 1   Challenge 3
# Single byte XOR cipher
################################################################################
# The hex encoded string:
# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
# has been XOR'd against a single character. Find the key, decrypt the message.
# Key:      int=88, char='X'
# Message:  Cooking MC's like a pound of bacon
################################################################################

def find_key(key, tuple_):
    return chr(int(tuple_[0] + tuple_[1], base=16) ^ key)

def decode_with_key(key, s):
    decoded_msg = ''
    for t in zip(s[0::2], s[1::2]):
        decoded_msg += find_key(key, t)

    print('Decoded message: {0}'.format(decoded_msg))

def decode(s):
    for key in range(0, 256):
        print('[*] Trying the key: int: {0}, char: {1}'.format(key, chr(key)))
        decode_with_key(key, s)
        print()

def main():
    s = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    decode(s)

if __name__ == '__main__':
    main()
