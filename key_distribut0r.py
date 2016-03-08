# -*- coding: utf-8 -*-

import os
import json
import shutil
import socket

import paramiko
import scp


CLEANUP_AFTER = True
TMP_DIR_PATH = 'tmp'
KEYS_FILE_NAME = 'keys.json'
SERVERS_FILE_NAME = 'servers.json'
TIMEOUT_ON_CONNECT = 2  # in seconds

# Colors for console outputs
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_END = '\033[0m'


def cleanup():
    if os.path.exists(TMP_DIR_PATH):
        shutil.rmtree(TMP_DIR_PATH)


def remove_special_chars(original_string):
    return ''.join(e for e in original_string if e.isalnum())


def error_log(ip, comment, message):
    print u'%s✗ %s/%s - Error: %s%s' % (COLOR_RED, ip, comment, message, COLOR_END)


def info_log(ip, comment, users):
    print u'%s✓ %s/%s - Access granted for: %s%s' % (COLOR_GREEN, ip, comment, users, COLOR_END)


def main():
    # Cleanup
    cleanup()
    os.makedirs(TMP_DIR_PATH)

    # Load config files
    servers = json.load(open(SERVERS_FILE_NAME))
    keys = json.load(open(KEYS_FILE_NAME))

    for server in servers:
        if len(server['authorized_users']) > 0:
            # Generate key file for this server
            key_file_name = 'authorized_keys_%s' % remove_special_chars(server['comment'] + server['ip'])
            key_file = open('%s/%s' % (TMP_DIR_PATH, key_file_name), 'w+')
            server_users = []

            # Write all keys of users with permissions for this server
            for authorized_user in server['authorized_users']:
                user_name = '%s (%s)' % (keys[authorized_user]['fullname'], authorized_user)
                server_users.append(user_name)
                for key in keys[authorized_user]['keys']:
                    key_file.write('%s\n' % key)
            key_file.close()

            # Configure SSH client
            ssh_client = paramiko.SSHClient()
            ssh_client.load_system_host_keys()  # Load host keys to check whether they are matching
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Add missing host keys automatically
            try:
                # Establish connection
                ssh_client.connect(server['ip'], port=server['port'], username=server['user'],
                                   timeout=TIMEOUT_ON_CONNECT)
                scp_client = scp.SCPClient(ssh_client.get_transport())

                # Upload key file
                scp_client.put('%s/%s' % (TMP_DIR_PATH, key_file_name), remote_path='.ssh/authorized_keys')
                scp_client.close()

                info_log(server['ip'], server['comment'], ', '.join(server_users))

            except paramiko.ssh_exception.NoValidConnectionsError:
                error_log(server['ip'], server['comment'], 'Cannot connect to server.')
            except socket.timeout:
                error_log(server['ip'], server['comment'], 'Cannot connect to server because of a timeout.')
        else:
            error_log(server['ip'], server['comment'], 'No user mentioned in configuration file!')

    if CLEANUP_AFTER:
        cleanup()


if __name__ == '__main__':
    print
    print 'SSHKeyDistribut0r'
    print '================='
    print 'Welcome in the world of key distribution dude!'
    print
    try:
        main()
    except KeyboardInterrupt:
        exit()
