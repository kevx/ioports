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
_passwd = None
_targets = {}

def md5str(s):
    return hashlib.md5(s).hexdigest()


def walk_dir(d):
    for dirpath, dnames, fnames in os.walk(d):
        for f in fnames:
            fpath = '%s/%s'%(dirpath, f)
            _targets[md5str(fpath)] = fpath


def init_manifest():
    f = open('targets.lst', 'r')
    for line in f:
        line = line.strip()
        if os.path.isdir(line): walk_dir(line)
        elif os.path.isfile(line): 
            _targets[md5str(line)] = line
    f.close()


def debug():
    for k,v in _targets.items():
        print(k)


def main():
    tmpws = '/tmp/depvps'
    zpath = '/tmp/main_data.zip'
    zxpath = 'main_data.zip.x'
    cmd = ''
    init_manifest()
    if os.path.exists(zpath): os.remove(zpath)
    if _cmd == 'to':
        z = ZipFile(zpath, 'w')
        for k, v in _targets.items(): z.write(v, k)
        z.close()
        cmd = _sh_enc%(zpath, zxpath, _passwd)
        os.system(cmd)
        os.system('git add .')
        os.system('git commit -m coding')
        os.system('git push')

    elif _cmd == 'from':
        os.system('git pull')
        if not os.path.exists(zxpath):
            print('main_data not found!')
            return
        cmd = _sh_dec%(zxpath, zpath, _passwd)
        os.system(cmd)
        z = ZipFile(zpath, 'r')
        entries = z.namelist()
        for e in entries:
            if _targets.has_key(e):
                z.extract(e, _targets[e])
        z.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('invalid_params')
        exit()
    _cmd = sys.argv[1]
    _passwd = sys.argv[2]
    main()