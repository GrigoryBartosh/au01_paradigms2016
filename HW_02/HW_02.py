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
                        file = path.join(root,name)
                        if os.path.islink(file):
                                continue
                        yield file

def get_hash(file):
        with open(file, mode='rb') as f:
                hashe = hasher()
                data = f.read(256)
                while data:
                        hashe.update(data)
                        data = f.read(256)
                return hashe.hexdigest()

def group_files(top_dir):
        files_dict = collections.defaultdict(list)
        for file in all_files(top_dir):
                h = get_hash(file)
                files_dict[h].append(os.path.relpath(file,top_dir))
        return files_dict

def print_same(files_dict):
        for k, files in files_dict.items():
                if len(files) == 1:
                        continue
                print(':'.join(files))

if __name__ == "__main__":
        top_dir = parse_dir(sys.argv)
        files_dict = group_files(top_dir)
        print_same(files_dict)
