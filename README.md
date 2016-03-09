SSHKeyDistribut0r has been written to make SSH key distribution easier for sysop teams.

![Screenshot](http://i.imgur.com/qoKm9dl.png)

# How to use
## Install dependencies
```
pip install -r requirements.txt
```

## Create configuration files
```
cp keys.sample.json keys.json
cp servers.sample.json servers.json
```
The keys.json file has to contain all users which are used in the
servers.json file. Every entry in the JSON dictionary requires the
following attributes:
The `fullname` is a string value to mention the full name of the person.
`keys` is a list of SSH keys in the format `ssh-rsa <KEY> <comment>`.
The dictionary keys are used to declare the username.

The servers.json file contains all servers with the specified user
permissions. It consists of a list of dictionaries with the following
attributes:
* `ip`: String value in the format `XXX.XXX.XXX.XXX`
* `port`: Integer value which specifies the SSH port
* `user`: String value which specifies the system user to log in.
* `comment`: String value to describe the system
* `authorized_users`: List of strings which specify a user. Every user
    has to be declared in the keys.json file as a key.

## Execute SSHKeyDistribut0r
```
python key_distribut0r.py
```
