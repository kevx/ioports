# coding=utf-8
"""
author: xz
date: 2014-09-22
"""

import sys
import os
import hashlib
from zipfile import ZipFile

_sh_enc = 'openssl enc -in %s -out %s -e -aes-256-cbc -k %s'
_sh_dec = 'openssl enc -in %s -out %s -d -aes-256-cbc -k %s'

_cmd = None
_opt = None
_passwd = None
_targets = {}

_tmpws = '/tmp/depvps'

def md5str(s):
    return hashlib.md5(s).hexdigest()

def init_targets():
    zpath = '/tmp/main_data.zip'
    f = open('map.lst', 'r')
    for line in f:
        line = line.strip()
        _targets[md5str(line)] = line
    f.close()

    z = ZipFile(zpath, 'r')
    z.extractall(_tmpws)
    z.close()

def debug():
    for k,v in _targets.items():
        print(k)

def main():
    init_targets()
    fpath = sys.argv[1]
    for k, v in _targets.items():
        if v == fpath: 
            os.system('nano %s/%s'%(_tmpws, k))

if __name__ == '__main__':
    main()