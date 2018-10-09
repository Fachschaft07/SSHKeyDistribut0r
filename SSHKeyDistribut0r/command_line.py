# -*- coding: utf-8 -*-

from __future__ import print_function
import SSHKeyDistribut0r

import appdirs
import argparse
import sys


def main():
    prog = 'SSHKeyDistribut0r'
    print()
    print(prog)
    print('=================')
    print('Welcome to the world of key distribution!')
    print()

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
        SSHKeyDistribut0r.main(args)
    except KeyboardInterrupt:
        sys.exit(1)
