#!/bin/env bash
set -Eeuo pipefail

source=/source
target=/target

function main() {
	readarray -td: excludes <<<"${EXCLUDE:-}:"
	unset 'excludes[-1]'
	local arguments=()
	for pattern in "${excludes[@]}"; do
		arguments+=(--exclude="$pattern")
	done
	rsync --recursive --times --verbose --delete \
		"${arguments[@]}" \
		--exclude='.sync-backup/' \
		--backup --backup-dir="$2/.sync-backup" --suffix=~$(date +%F-%T | sed 's/:/-/g') \
		"$1/" "$2/" 2>&1
}

function is_samba_path() {
	if [[ "$1" == //* ]]; then
		return 0
	fi
	return 1
}

function mount_samba() {
	if [ ! -f "$1" ]; then
		echo "Credentials file not found: $1"
		exit 1
	fi
	if ! mount -t cifs -o credentials="$1",noexec,cache=strict,uid=0,noforceuid,gid=0,noforcegid,iocharset=utf8,nocase,echo_interval=5 "$2" "$3"; then
		echo "Can't mount smb: $2"
		exit 2
	fi
}

function cleanup() {
	while pkill -0 rsync; do
		sleep 1
	done
	while pkill -0 mount; do
		sleep 1
	done
}

trap cleanup exit

if is_samba_path "$1"; then
	mkdir "$source"
	mount_samba "$SOURCE_CREDENTIALS" "$1" "$source"
fi

if is_samba_path "$2"; then
	mkdir "$target"
	mount_samba "$TARGET_CREDENTIALS" "$2" "$target"
fi

main "$source" "$target"
