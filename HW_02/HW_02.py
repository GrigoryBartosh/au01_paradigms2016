import sys
import os
import re
import collections
from os import walk
from os import path
from hashlib import sha1 as hasher

def parse_dir(argv):
        if len(argv) != 2:
                print('Wrong format, enter top directory')
                sys.exit(0)
        return argv[1]

def all_files(top_dir):
        for root, _, files in walk(top_dir):
                for name in files:
                        if (name[0] == '.') or (name[0] == '~'):
                                continue
                        yield path.join(root,name)

def get_hash(file):
        with open(file, mode='rb') as f:
                hashe = hasher()
                data = f.read(256)
                while data:
                        hashe.update(data)
                        data = f.read(256)
                return hashe.hexdigest()

def group_files(top_dir):
        dict = collections.defaultdict(list)
        for file in all_files(top_dir):
                h = get_hash(file)
                dict[h].append(os.path.relpath(file,top_dir))
        return dict

def print_same(dict):
        for k, files in dict.items():
                if len(files) == 1:
                        continue
                print(':'.join(files))

if __name__ == "__main__":
        dir = parse_dir(sys.argv)
        dict = group_files(dir)
        print_same(dict)
