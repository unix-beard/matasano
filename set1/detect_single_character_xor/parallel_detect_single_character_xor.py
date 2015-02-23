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
# NOTE: This implementation is parallel
################################################################################

import os
import sys
import string
import logging
import argparse
import multiprocessing
from contextlib import ContextDecorator


################################################################################
logger = logging.getLogger('parallel_detect_single_character_xor')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
################################################################################


class FileSplitter(ContextDecorator):
    """
    Splits input file into multiple smaller temporary files (one file per worker)
    The size of a smaller file is determined like this:
        size_of_input_file / number_of_workers

    After the worker is done decoding its file, 
    FileSplitter removes this temporary small file
    """

    def __init__(self, input_file, number_of_workers):
        self._input_file = input_file
        self._number_of_workers = number_of_workers
        self._split

    def __enter__(self):
        self._split_files = self._split()
        for f in self._split_files:
            logger.debug('Tmp file: {0}'.format(f.name))
        return self

    def __exit__(self, *exc):
        for f in self._split_files:
            logger.debug('Cleaning up temporary file: {0}'.format(f.name))
            os.remove(f.name)

        return False

    def __next__(self):
        for f in self._split_files:
            yield f

    def _split(self):
        logger.debug('Splitting file {0}'.format(self._input_file))
        split_files = []
        file_size, split_file_size = self._do_prelim_calculations()
        with open(self._input_file, 'r') as f:
            for worker in range(self._number_of_workers):
                split_files.append(self._read_and_split(f, worker, split_file_size))
        return split_files

    def _read_and_split(self, file_, worker, split_file_size):
        import tempfile
        with tempfile.NamedTemporaryFile(prefix=os.path.basename(self._input_file) + '.' + str(worker) + '.', delete=False) as tmp:
            logger.debug('Temporary file {0} created'.format(tmp.name))
            bytes_read = 0
            for line in file_:
                logger.debug('Writing line [{0}]'.format(line[:len(line) - 1] if line[-1] == '\n' else line))
                tmp.write(bytes(line, 'UTF-8'))
                bytes_read += len(line)
                if bytes_read >= split_file_size:
                    return tmp

            return tmp

    def _do_prelim_calculations(self):
        import math
        # Get file size in bytes
        file_size = os.path.getsize(self._input_file)

        # Calculate the size of each file (in bytes) to be split
        split_file_size = file_size // self._number_of_workers
        logger.debug('File size: {0}; split file size: {1}'.format(file_size, split_file_size))
        return file_size, split_file_size


def find_key(key, tuple_):
    return chr(int(tuple_[0] + tuple_[1], base=16) ^ key)

def decode_with_key(key, s):
    decoded_msg = ''
    for t in zip(s[0::2], s[1::2]):
        decoded_msg += find_key(key, t)

    if len([c for c in decoded_msg if c in string.ascii_letters + ' \n']) == len(decoded_msg):
        logger.info('[*] Trying the key: int: {0}, char: {1}'.format(key, chr(key)))
        logger.info('Decoded message: {0}'.format(decoded_msg))
        return decoded_msg

    return None
    
def remove_eol(s):
    """Removes trailing '\n' if there is one"""
    return s[0:len(s) - 1] if s[len(s) - 1] == '\n' else s

def decode(queue_, file_to_decode):
    results = []
    with open(file_to_decode, 'r') as f:
        for encoded_line in f:
            line = remove_eol(encoded_line)
            #logger.debug('File: {0}\n\tDecoding [{1}]'.format(f.name, line))
            for key in range(0, 256):
                decoded_msg = decode_with_key(key, line)
                if decoded_msg is not None:
                    results.append((f.name, key, decoded_msg))

    queue_.put(results)

def main():
    parser = argparse.ArgumentParser(description='Parallel detect single-character XOR')
    parser.add_argument('-w', '--workers', dest='workers', default=1, type=int,
            help='Number of workers to split the decoding work amongst')
    parser.add_argument('file', type=str, help='File to decode')
    args = parser.parse_args()

    with FileSplitter(args.file, args.workers) as fs:
        proc = []
        q = multiprocessing.Queue()
        for f in next(fs):
            #logger.info('Decoding file {0}'.format(f.name))
            proc.append(multiprocessing.Process(target=decode, args=(q, f.name,)))
            proc[-1].start()

        for p in proc:
            res = q.get()
            if res:
                logger.info('Results: {0}'.format(res))
            p.join()

if __name__ == '__main__':
    main()
