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