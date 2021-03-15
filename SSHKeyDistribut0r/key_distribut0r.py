# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import io
import json
import logging
import os
import re
import socket
import sys
import csv

import paramiko
import scp
import yaml

logging.raiseExceptions = False

TIMEOUT_ON_CONNECT = 2  # in seconds

# Colors for console outputs
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_END = '\033[0m'

# File extension regex
YAML_EXT = re.compile("^\\.ya?ml$")
JSON_EXT = re.compile("^\\.json$")

ERROR_STATUS = 'Error'
SUCCESS_STATUS = 'Success'


def remove_special_chars(original_string):
    return ''.join(e for e in original_string if e.isalnum())


def error_log(message):
    print(u'%s✗ Error: %s%s' % (COLOR_RED, message, COLOR_END))


def server_error_log(ip, comment, message):
    error_log('%s/%s - %s' % (ip, comment, message))


def info_log(message):
    print(u'%s✓ %s%s' % (COLOR_GREEN, message, COLOR_END))


def server_info_log(ip, comment, users):
    info_log('%s/%s - %s' % (ip, comment, users))


def read_config(config_file):
    ext = os.path.splitext(config_file)[-1]
    try:
        if YAML_EXT.match(ext):
            return yaml.load(open(config_file))
        elif JSON_EXT.match(ext):
            return json.load(open(config_file))
        else:
            error_log("Configuration file extension '%s' not supported." \
                      " Please use .json or .yml." % ext)
            sys.exit(1)
    except (ValueError, yaml.scanner.ScannerError):
        error_log('Cannot parse malformed configuration file.')
        sys.exit(1)


def get_maximum_column_lengths(messages):
    column_count = len(messages[0])
    column_max_lens = {i: max(len(message[i]) for message in messages) for i in range(column_count)}
    return column_max_lens


def print_table_log(messages):

    messages.sort(key=lambda m: m[0] == ERROR_STATUS)

    max_column_lens = get_maximum_column_lengths(messages)

    def print_borderline():
        column_count = len(messages[0])
        empty_columns = ('' for _ in range(column_count))
        print("+{:-^{lens[0]}}+{:-^{lens[1]}}+{:-^{lens[2]}}+{:-^{lens[3]}}+".format(*empty_columns,
                                                                                     lens=max_column_lens))
    print()
    print_borderline()
    for message in messages[1:]:
        color_on = COLOR_RED if message[0] == ERROR_STATUS else COLOR_GREEN
        clear_message = (re.sub(r'\s+', ' ', col) for col in message)
        print("|{color_on}{:^{lens[0]}}{color_off}"
              "|{:^{lens[1]}}|{:^{lens[2]}}"
              "|{:^{lens[3]}}|".format(*clear_message, color_on=color_on, color_off=COLOR_END, lens=max_column_lens))
        print_borderline()


def export_to_csv(path, messages):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerows(messages)
    except OSError as e:
        print(e)


def main(args):
    # Load config files
    servers = read_config(args.server)
    keys = read_config(args.keys)
    messages = [('Status', 'Ip', 'Comment', 'Description')]

    for server in servers:
        if server['authorized_users']:
            # Generate key file for this server
            # key_stream = io.BytesIO()
            key_stream = io.StringIO()
            server_users = []

            # Write all keys of users with permissions for this server
            for authorized_user in server['authorized_users']:
                # user_name = '%s (%s)' % (keys[authorized_user]['fullname'], authorized_user)
                user_name = authorized_user
                server_users.append(user_name)
                if authorized_user in list(keys.keys()):
                    for key in keys[authorized_user]['keys']:
                        key_stream.write('%s\n' % key)
                else:
                    error_log("Cannot find user '%s' in the key configuration file" \
                              " for '%s/%s'." % (authorized_user, server['ip'], server['comment']))
                    sys.exit(1)

            if args.dry_run:
                msg = server['ip'], server['comment'], ', '.join(server_users)
                server_info_log(*msg)
                messages.append((SUCCESS_STATUS, *msg))
            else:
                # Configure SSH client
                ssh_client = paramiko.SSHClient()
                ssh_client.load_system_host_keys()  # Load host keys to check whether they are matching
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Add missing host keys automatically
                try:
                    # Establish connection
                    ssh_client.connect(server['ip'], port=server['port'], username=server['user'],
                                       timeout=TIMEOUT_ON_CONNECT)

                    # Upload key file
                    with scp.SCPClient(ssh_client.get_transport()) as scp_client:
                        key_stream.seek(0)
                        scp_client.putfo(key_stream, '.ssh/authorized_keys')

                    key_stream.close()
                    msg = server['ip'], server['comment'], ', '.join(server_users)
                    server_info_log(*msg)
                    messages.append((SUCCESS_STATUS, *msg))

                except paramiko.ssh_exception.PasswordRequiredException:
                    msg = server['ip'], \
                          server['comment'], \
                          'The private key file is protected by a passphrase, which is currently not supported.'
                    server_error_log(*msg)
                    messages.append((ERROR_STATUS, msg))
                except paramiko.ssh_exception.AuthenticationException:
                    msg = server['ip'],\
                          server['comment'], \
                          'Cannot connect to server because of an authentication problem.'
                    server_error_log(*msg)
                    messages.append((ERROR_STATUS, *msg))
                except scp.SCPException:
                    msg = server['ip'], server['comment'], 'Cannot send file to server.'
                    server_error_log(*msg)
                    messages.append((ERROR_STATUS, *msg))
                except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.SSHException):
                    msg = server['ip'], server['comment'], 'Cannot connect to server.'
                    server_error_log(*msg)
                    messages.append((ERROR_STATUS, *msg))
                except socket.timeout:
                    msg = server['ip'], server['comment'], 'Cannot connect to server because of a timeout.'
                    server_error_log(*msg)
                    messages.append((ERROR_STATUS, *msg))
        else:
            msg = server['ip'], server['comment'], 'No user mentioned in configuration file!'
            server_error_log(*msg)
            messages.append((ERROR_STATUS, *msg))
    print_table_log(messages)
    if args.export_csv_path:
        export_to_csv(args.export_csv_path, messages)

