#!/usr/bin/python3

import os
import argparse
from subprocess import call

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('basedir', type=str, help='The base directory to walk from')
    args = parser.parse_args()
    print('The base dir is: {}'.format(args.basedir))
    for dirname, subdirs, filenames in os.walk(args.basedir):
        for filename in filenames:
            full_path = os.path.join(dirname, filename)
            if filename.endswith('.bz2'):
                print("Decompressing {}".format(full_path))
                call(["bzip2", "-d", full_path])
            else:
                print("Ignoring {}".format(full_path))
