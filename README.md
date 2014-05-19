# Installation

## On Ubuntu/Debian:

Use the [daily builds PPA](https://launchpad.net/~lookit/+archive/daily).

```bash
sudo add-apt-repository ppa:lookit/daily
sudo apt-get update
sudo apt-get install lookit
```

## On Arch
Install the following Packages:
- extra/python2-notify
- extra/python2-gconf
- aur/python2-keyring
- extra/python2-xdg
- aur/libappindicator

### SFTP/SSH
- community/_python2-paramiko_

### HTTP
- extra/python2-pycurl

## Xfce4
To add the Keyboard-Shortcuts you like
- Go to your Keyboard-Settings
- Shortcuts
- Add a shortcut for every thing you would do
    - lookit --capture-area
    - lookit --capture-window
    - lookit --capture-screen
    - lookit --preferences

If you want notifications you probably need:
- extra/xfce4-notifyd

## From source:

Source tarballs are available on the [download page](http://github.com/zachtib/lookit/downloads).

Extract the tarball and run (as root):

```bash
python setup.py install
```
