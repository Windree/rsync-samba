# Rsync with samba support

## Requires
1. Bash
1. Docker 

## Usage
```
./app.sh [OPTIONS] source target
```
### Options
**source** (required) source samba UNC/director. i.e. //server/share, /var/log

**target** (required) target samba UNC/director. i.e. //server/share, /var/log

**-sc, --source-credentials** (required if source is samba share) source samba credentials file

**-tc, --target-credentials** (required if target is samba share) target samba credentials file

**-e, --exclude** exclude locations from backup. Separate multipile values with :


### Samba credentials file example
```
username=Administator
password=dZ041936814Ga
```

## Examples

```
./app.sh -sc "/root/cifs.my-computer.conf" -e "\$RECYCLE.BIN/:System Volume Information/" //192.168.1.2/D "/backups/my-computer-d"
```

```
./app.sh -sc "/root/cifs.my-computer.conf" -tc "/root/cifs.backup-server-creds.conf" -e "\$RECYCLE.BIN/:System Volume Information/" //192.168.1.2/D "//192.168.1.252/backups/my-computer-d"
```

