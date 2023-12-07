#!/bin/env bash
set -Eeuo pipefail
source=
target=
source_credentials=
target_credentials=
exclude=

while [ $# -gt 0 ]; do
  if [[ $1 == -* ]]; then
    case "$1" in
    -sc | --source-credentials)
      source_credentials="${2:-}"
      ;;
    -tc | --target-credentials)
      target_credentials="${2:-}"
      ;;
    -e | --exclude)
      exclude="${2:-}"
      ;;
    *)
      echo "Invalid argument '$1'"
      exit 1
      ;;
    esac
    shift
    [ $# -gt 0 ] && shift
  else
    if [ -z ${source} ]; then
      source=$1
    elif [ -z ${target} ]; then
      target=$1
    else
      echo "Extra argument '$1'"
    fi
    shift
  fi
done

script=$(readlink -f -- "$0")
dir=$(dirname "$script")
image=$(basename "$dir")

function build_image() {
  if ! docker build --quiet "$dir/image" -t "$image" 2>/dev/null >/dev/null; then
    echo "Error build '$dir/image'"
    exit 1
  fi
}

function main() {
  local source_arguments=
  local target_arguments=
  if is_samba_path "$source"; then
    source_arguments="-e SOURCE_CREDENTIALS=/source.cifs -v "$source_credentials:/source.cifs:ro""
  else
    source_arguments="-v "$source:/source""
  fi
  if is_samba_path "$target"; then
    target_arguments="-e TARGET_CREDENTIALS=/target.cifs -v "$target_credentials:/target.cifs:ro""
  else
    target_arguments="-v "$target:/target""
  fi
  build_image
  docker run --rm --privileged --cap-add SYS_ADMIN --cap-add DAC_READ_SEARCH -e EXCLUDE="$exclude" $source_arguments $target_arguments "$image" "$source" "$target"
}

function is_samba_path() {
  if [[ "$1" == //* ]]; then
    return 0
  fi
  return 1
}

function validate() {
  local error=0

  if [ -z $source ]; then
    echo "Source not specified"
    error=1
  else
    if is_samba_path "$source"; then
      if [ ! -f "$source_credentials" ]; then
        echo "No credentials file '$source_credentials' found for $source"
        error=1
      fi
    fi
  fi

  if [ -z $target ]; then
    echo "Target not specified"
    error=1
  else
    if is_samba_path "$target"; then
      if [ ! -f "$target_credentials" ]; then
        echo "No credentials file '$target_credentials' found for $target"
        error=1
      fi
    fi
  fi

  if [ $error == 1 ]; then
    exit 1
  fi
}

validate
main
