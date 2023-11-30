#!/bin/env bash
set -Eeuo pipefail

script=$(readlink -f -- "$0")
dir=$(dirname "$script")
image=$(basename "$dir")

function build_image(){
    if ! docker build --quiet "$dir/image" -t "$image" 2>/dev/null >/dev/null; then
        echo "Error build '$dir/image'"
        exit 1
    fi
}

function main(){
    local source_arguments=
    local target_arguments=
    if is_samba_path "$1"; then
        if [ ! -f "$2" ]; then
            echo "No credentials file found for '$1'"
            exit 1
        fi
        source_arguments="-e SOURCE_CREDENTIALS=/source.cifs -v "$2:/source.cifs:ro""
    else
        source_arguments="-v "$1:/source""
    fi
    if is_samba_path "$3"; then
        if [ ! -f "$4" ]; then
            echo "No credentials file found for '$2'"
            exit 2
        fi
        target_arguments="-e TARGET_CREDENTIALS=/target.cifs -v "$4:/target.cifs:ro""
    else
        target_arguments="-v "$3:/target""
    fi
    docker run --rm --privileged --cap-add SYS_ADMIN --cap-add DAC_READ_SEARCH $source_arguments $target_arguments "$image" "$1" "$2"
}

function is_samba_path(){
    if [[ "$1" == //* ]]; then
        return 0
    fi
    return 1
}

build_image
main "$1" "$2" "$3" "$4"
