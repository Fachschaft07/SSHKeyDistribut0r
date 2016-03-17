[![CC BY](http://mirrors.creativecommons.org/presskit/buttons/80x15/svg/by.svg)](http://creativecommons.org/licenses/by/4.0/)

SSHKeyDistribut0r has been written to make SSH key distribution easier
for sysop teams.

![Screenshot](http://i.imgur.com/qoKm9dl.png)

# How to use
## Install dependencies
```
pip install -r requirements.txt
```

## Create configuration files
First, copy the YAML files and customize them. Use the corresponding
.json files if you prefer the JSON structure.
```
cp keys.sample.yml keys.yml
cp servers.sample.yml servers.yml
```
The keys.yml file has to contain all users which are used in the
servers.yml file. Every entry in the YML structure requires the
following attributes:
The `fullname` is a string value to mention the full name of a person.
`keys` is a list of SSH keys in the format `ssh-rsa <KEY> <comment>`.

The servers.yml file contains all servers with the specified user
permissions. It consists of a list of dictionaries with the following
attributes:
* `ip`: String value in the format `XXX.XXX.XXX.XXX`
* `port`: Integer value which specifies the SSH port
* `user`: String value which specifies the system user to log in.
* `comment`: String value to describe the system
* `authorized_users`: List of strings which specify a user. Every user
    has to be declared in the keys.yml file as a key.

## Execute SSHKeyDistribut0r
```
python key_distribut0r.py
```
