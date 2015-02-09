#!/usr/bin/env python3
 
################################################################################
# The matasano crypto challenges
# http://cryptopals.com/sets/1/challenges/1/
# Set 1   Challenge 1
# Convert hex to base64
################################################################################
# The string:
# 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
# Should produce:
# SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
###############################################################################
 
from base64 import b64encode
from itertools import zip_longest
 
s = b'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
 
b64 = b64encode(bytes(''.join([chr(int(chr(el[0]) + chr(el[1]), base=16)) for el in zip_longest(s[::2], s[1::2])]), 'utf-8')).decode('utf-8')
res = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
assert(res == b64)
