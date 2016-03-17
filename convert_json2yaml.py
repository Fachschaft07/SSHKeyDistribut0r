# -*- coding: utf-8 -*-

import json

KEYS_FILE_NAME_JSON = 'keys.json'
KEYS_FILE_NAME_YAML = 'keys.yml'

SERVERS_FILE_NAME_JSON = 'servers.json'
SERVERS_FILE_NAME_YAML = 'servers.yml'

# Generate keys.yml
source_json = json.load(open(KEYS_FILE_NAME_JSON))

result = '---\n'
for user, user_data in source_json.iteritems():
    result += user + ':\n'
    result += '  fullname: %s\n' % user_data['fullname']
    result += '  keys:\n'
    for key in user_data['keys']:
        result += '    - %s\n' % key
result += '...\n'

dest_yaml = open(KEYS_FILE_NAME_YAML, 'w+')
dest_yaml.write(result.encode('utf-8'))
dest_yaml.close()

print '%s --> %s' % (KEYS_FILE_NAME_JSON, KEYS_FILE_NAME_YAML)


# Generate servers.yml
source_json = json.load(open(SERVERS_FILE_NAME_JSON))

result = '---\n'
for server in source_json:
    result += '- ip: %s\n' % server['ip']
    result += '  port: %s\n' % server['port']
    result += '  user: %s\n' % server['user']
    result += '  comment: %s\n' % server['comment']
    result += '  authorized_users: [%s]\n' % ', '.join(server['authorized_users'])
result += '...\n'

dest_yaml = open(SERVERS_FILE_NAME_YAML, 'w+')
dest_yaml.write(result.encode('utf-8'))
dest_yaml.close()

print '%s --> %s' % (SERVERS_FILE_NAME_JSON, SERVERS_FILE_NAME_YAML)
