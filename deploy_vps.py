# coding=utf-8
"""
author: xz
date: 2014-09-22
"""

import sys
import os
import hashlib
import random
import shutil
from zipfile import ZipFile

_sh_enc = 'openssl enc -in %s -out %s -e -aes-256-cbc -k %s'
_sh_dec = 'openssl enc -in %s -out %s -d -aes-256-cbc -k %s'
_zpath = 'main_data.zip'

_cmd = None
_passwd = None
_targets = []

def md5str(s):
    return hashlib.md5(s).hexdigest()


def walk_dir(d):
    t = []
    for dirpath, dnames, fnames in os.walk(d):
        for f in fnames:
            fpath = '%s/%s'%(dirpath, f)
            t.append(fpath)
    return t

def init_manifest():
    f = open('manifest.lst', 'r')
    for line in f:
        line = line.strip()
        if os.path.isdir(line): _targets.extend(walk_dir(line))
        elif os.path.isfile(line):
            _targets.append(line)
    f.close()

def git_push():
    os.system('git add .')
    os.system('git commit -m coding')
    os.system('git push')

def git_pull_and_dec(zxpath, _zpath):
    os.system('git pull')
    if not os.path.exists(zxpath):
        print('main_data not found!')
        return
    cmd = _sh_dec%(zxpath, _zpath, _passwd)
    os.system(cmd)

def repack(tmp):
    z = ZipFile(_zpath, 'w')
    for dirpath, dnames, fnames in os.walk(tmp):
        for f in fnames:
            if f.endswith('.db'): continue
            fpath = '%s/%s'%(dirpath, f)
            z.write(fpath, fpath[9:])
    z.close()
    #shutil.rmtree(tmp)    

def main():
    zxpath = 'main_data.zip.x'
    cmd = ''
    init_manifest()
    if os.path.exists(_zpath): os.remove(_zpath)
    if _cmd == 'push-repack':
        repack('./secret')
        cmd = _sh_enc%(_zpath, zxpath, _passwd)
        os.system(cmd)
        git_push()

    elif _cmd == 'push':
        z = ZipFile(_zpath, 'w')
        for t in _targets:
            z.write(t)
        z.close()
        cmd = _sh_enc%(_zpath, zxpath, _passwd)
        os.system(cmd)
        git_push()

    elif _cmd == 'pull-ow': # pull and overwrite local files
        git_pull_and_dec(zxpath, _zpath)
        z = ZipFile(_zpath, 'r')
        entries = z.namelist()
        for e in entries:
            z.extract(e)
        z.close()

    elif _cmd == 'pull-ext': # pull and extract
        git_pull_and_dec(zxpath, _zpath)
        tmp = './secret/' #'/tmp/' + str(random.randint(1000,9999))
        z = ZipFile(_zpath, 'r')
        z.extractall(tmp)
        z.close()
        print('extracted to:%s'%tmp)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('invalid_params')
        exit()
    _cmd = sys.argv[1]
    _passwd = sys.argv[2]
    main()