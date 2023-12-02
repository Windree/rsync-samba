# Rsync with samba support

## Requires
1. Bash
1. Docker 

## Usage
```
./app.sh [OPTIONS]
```
### Options
**-s, --source** (required) source samba UNC/director. i.e. //server/share, /var/log

**-sc, --source-credentials** (required if source is samba share) source samba credentials file

**-t, --target** (required) target samba UNC/director. i.e. //server/share, /var/log

**-tc, --target-credentials** (required if target is samba share) target samba credentials file

### Samba credentials file example
```
username=Administator
password=dZ041936814Ga
```