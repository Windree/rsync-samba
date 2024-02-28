#!/usr/bin/python3

import argparse
from paths import Paths
from protocol import Protocol
from path import Path


def main():
    parser = argparse.ArgumentParser(
        prog="",
        description="Sync folders/files with rsync",
        usage="Examples:",
        allow_abbrev=False,
    )
    parser.add_argument("source", nargs=1)
    parser.add_argument("destination", nargs=1)
    parser.add_argument("rsync_arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    arguments = Paths(args.source, args.destination)
    if not arguments.validate():
        exit(1)
    print(vars(arguments.source), vars(arguments.destination))


def getRsyncArguments(path: Path, forceMount):
    arguments = []
    match path.scheme:
        case Protocol.ssh:
            arguments.append("-e")
            if path.port != None:
                arguments.append("ssh -p %s" % path.port)
            arguments.append("%s:%s" % (path.host, path.path))
        case Protocol.smb:
            print("mount smb")
        case _:
            arguments.append(path.path)
    return arguments


main()

# set -Eeuo pipefail

# source=/source
# target=/target

# function main() {
# 	readarray -td: excludes <<<"${EXCLUDE:-}:"
# 	unset 'excludes[-1]'
# 	local arguments=()
# 	for pattern in "${excludes[@]}"; do
# 		arguments+=(--exclude="$pattern")
# 	done
# 	rsync --recursive --times --verbose --delete \
# 		"${arguments[@]}" \
# 		--exclude='.sync-backup/' \
# 		--backup --backup-dir="$2/.sync-backup" --suffix=~$(date +%F-%T | sed 's/:/-/g') \
# 		"$1/" "$2/" 2>&1
# }

# function is_samba_path() {
# 	if [[ "$1" == //* ]]; then
# 		return 0
# 	fi
# 	return 1
# }

# function mount_samba() {
# 	if [ ! -f "$1" ]; then
# 		echo "Credentials file not found: $1"
# 		exit 1
# 	fi
# 	if ! mount -t cifs -o credentials="$1",noexec,cache=strict,uid=0,noforceuid,gid=0,noforcegid,iocharset=utf8,nocase,echo_interval=5 "$2" "$3"; then
# 		echo "Can't mount smb: $2"
# 		exit 2
# 	fi
# }

# function cleanup() {
# 	while pkill -0 rsync; do
# 		sleep 1
# 	done
# 	while pkill -0 mount; do
# 		sleep 1
# 	done
# }

# trap cleanup exit

# if is_samba_path "$1"; then
# 	mkdir "$source"
# 	mount_samba "$SOURCE_CREDENTIALS" "$1" "$source"
# fi

# if is_samba_path "$2"; then
# 	mkdir "$target"
# 	mount_samba "$TARGET_CREDENTIALS" "$2" "$target"
# fi

# main "$source" "$target"
