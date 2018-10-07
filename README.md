[![CC BY](http://mirrors.creativecommons.org/presskit/buttons/80x15/svg/by.svg)](http://creativecommons.org/licenses/by/4.0/)

SSHKeyDistribut0r has been written to make SSH key distribution easier
for sysop teams.

![Screenshot](http://i.imgur.com/qoKm9dl.png)

# How to use
## Install
```
pip install SSHKeyDistribut0r
```

## Create configuration files
First, copy the YAML sample files to your users config directory and customize them.

The sample files should be in
`$HOME/.local/share/SSHKeyDistribut0r/config_sample`,
`/usr/local/share/SSHKeyDistribut0r/config_sample` or
`/usr/share/SSHKeyDistribut0r/config_sample`

The config files need to be copied to `$USER_CONFIG_DIR/SSHKeyDistribut0r/`
(`$HOME/.config/...` on most Linux systems, check `SSHKeyDistribut0r -h` for
the location on your system)

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

## Usage
Run `SSHKeyDistribut0r` to distribute your SSH keys :)

### Options
- `--dry-run`/`-n`: To verify your configuration whithout actually applying those changes.
- `--keys`/`-k`: Custom path to keys file
- `--server`/`-s`: Custom path to server file
