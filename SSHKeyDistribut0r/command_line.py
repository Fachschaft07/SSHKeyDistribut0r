# -*- coding: utf-8 -*-

import SSHKeyDistribut0r

import appdirs
import argparse
import os
from shutil import rmtree
import sys


TMP_DIR_PATH = '%s/tmp' % appdirs.user_data_dir()
CLEANUP_AFTER = True

def cleanup():
    if os.path.exists(TMP_DIR_PATH):
        rmtree(TMP_DIR_PATH)

def main():
    prog = 'SSHKeyDistribut0r'
    print
    print prog
    print '================='
    print 'Welcome to the world of key distribution!'
    print

    parser = argparse.ArgumentParser(
            description='A tool to automate key distribution with user authorization.')
    parser.add_argument('--dry-run', '-n', action='store_true',
            help='show pending changes without applying them')
    parser.add_argument('--keys', '-k',
            default='%s/%s/keys.yml' % (appdirs.user_config_dir(), prog),
            help="path to keys file\n(default: '%(default)s')")
    parser.add_argument('--server', '-s',
            default='%s/%s/servers.yml' % (appdirs.user_config_dir(), prog),
            help="path to server file (default: '%(default)s')")
    args = parser.parse_args()

    try:
        cleanup()
        os.makedirs(TMP_DIR_PATH)
        SSHKeyDistribut0r.main(args, TMP_DIR_PATH)
        if CLEANUP_AFTER:
            cleanup()
    except KeyboardInterrupt:
        sys.exit(1)
