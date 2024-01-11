#!/usr/bin/python3

import os
import subprocess
import argparse
from urllib.parse import urlparse, parse_qs


class Path:
    def __init__(self, arg):
        url = urlparse(arg)
        qs = parse_qs(url.query)
        self.scheme = url.scheme if url.scheme else None
        self.host = url.hostname
        self.port = url.port
        self.path = url.path if url.path else None
        self.user = url.username
        self.password = url.password
        self.credentials = qs["credentials"][0] if "credentials" in qs else None

    def validate(self) -> list[str]:
        warnings = []
        if self.scheme not in (None, "smb", "ssh"):
            warnings.append("Only smb and ssh scheme supported")
        if self.scheme == None:
            if not self.path:
                warnings.append("Path required if no schema exists")
            else:
                result = subprocess.run(
                    ["df", self.path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                if result.returncode != 0:
                    warnings.append("Path '%s' not binded" % (self.path))
        return warnings


class Arguments:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="", description="Sync folders/files with rsync", usage="Examples:"
        )
        parser.add_argument("source", nargs=1)
        parser.add_argument("destination", nargs=1)
        args = parser.parse_args()
        self.source = Path(args.source[0])
        self.destination = Path(args.destination[0])

    def validate(self):
        sourceWarnings = self.source.validate()
        destinationWarnings = self.destination.validate()
        if len(sourceWarnings):
            showWarnings("Source", sourceWarnings)
        if len(destinationWarnings):
            showWarnings("Destination", destinationWarnings)
        return not (len(sourceWarnings) or len(destinationWarnings))


def main():
    arguments = Arguments()
    if not arguments.validate():
        exit(1)

    print(vars(arguments.source), vars(arguments.destination))


def showWarnings(header: str, warnings: list[str]):
    print("%s:" % (header))
    for warning in warnings:
        print("\t%s" % (warning))


def getRsyncPath(path: Path):
    match path.scheme:
        case None:
            return path.path
        case "ssh":
            return 


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
