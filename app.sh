#!/bin/env bash
set -Eeuo pipefail

while [ $# -gt 0 ]; do
  case "$1" in
  -s | --source)
    source="$2"
    ;;
  -sc | --source-credentials)
    source_credentials="$2"
    ;;
  -t | --target)
    target="$2"
    ;;
  -tc | --target-credentials)
    target_credentials="$2"
    ;;
  *)
    echo "Invalid argument '$1'"
    exit 1
    ;;
  esac
  shift
  shift
done

if [ -z ${source+x} ]; then
  echo "Source not specified"
  exit 1
fi

if [ -z ${target+x} ]; then
  echo "Target not specified"
  exit 1
fi

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
    if [ ! -f "$source_credentials" ]; then
      echo "No credentials file found for '$1'"
      exit 1
    fi
    source_arguments="-e SOURCE_CREDENTIALS=/source.cifs -v "$source_credentials:/source.cifs:ro""
  else
    source_arguments="-v "$source:/source""
  fi
  if is_samba_path "$target"; then
    if [ ! -f "$target_credentials" ]; then
      echo "No credentials file found for '$2'"
      exit 2
    fi
    target_arguments="-e TARGET_CREDENTIALS=/target.cifs -v "$target_credentials:/target.cifs:ro""
  else
    target_arguments="-v "$target:/target""
  fi
  build_image
  docker run --rm --privileged --cap-add SYS_ADMIN --cap-add DAC_READ_SEARCH $source_arguments $target_arguments "$image" "$source" "$target"
}

function is_samba_path() {
  if [[ "$1" == //* ]]; then
    return 0
  fi
  return 1
}

main
