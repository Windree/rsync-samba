#!/bin/env bash
set -Eeuo pipefail

while [ $# -gt 0 ]; do
  if [[ $1 == -* ]]; then
    case "$1" in
    -sc | --source-credentials)
      shift
      if [[ -v 1 ]]; then
        source_credentials=$1
        shift
      fi
      ;;
    -tc | --target-credentials)
      shift
      if [[ -v 1 ]]; then
        target_credentials=$1
        shift
      fi
      ;;
    -e | --exclude)
      shift
      if [[ -v 1 ]]; then
        exclude=$1
        shift
      fi
      ;;
    *)
      echo "Invalid argument '$1'"
      exit 1
      ;;
    esac
    continue
  fi

  if [ ! -v source ]; then
    source=$1
    shift
  elif [ ! -v target ]; then
    target=$1
    shift
  else
    echo "Two arguments required only"
    exit 1
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
  local arguments=()
  if is_samba_path "$source"; then
    arguments+=(-e SOURCE_CREDENTIALS=/source.cifs -v "$source_credentials:/source.cifs:ro")
  else
    arguments+=(-v "$source:/source")
  fi
  if is_samba_path "$target"; then
    arguments+=(-e TARGET_CREDENTIALS=/target.cifs -v "$target_credentials:/target.cifs:ro")
  else
    arguments+=(-v "$target:/target")
  fi
  if [ -v exclude ]; then
    arguments+=(-e EXCLUDE="$exclude")
  fi
  build_image
  docker run --rm --privileged --cap-add SYS_ADMIN --cap-add DAC_READ_SEARCH "${arguments[@]}" "$image" "$source" "$target"
}

function is_samba_path() {
  if [[ "$1" == //* ]]; then
    return 0
  fi
  return 1
}

function validate() {
  local error=0

  if [ ! -v source ]; then
    echo "Source not specified"
    error=1
  else
    if is_samba_path "$source"; then
      if [ ! -v source_credentials ]; then
        echo "No credentials file specified for $source"
        error=1
      elif [ ! -f "$source_credentials" ]; then
        echo "No credentials file '$source_credentials' found for $source"
        error=1
      fi
    fi
  fi

  if [ ! -v target ]; then
    echo "Target not specified"
    error=1
  else
    if is_samba_path "$target"; then
      if [ ! -v target_credentials ]; then
        echo "No credentials file specified for $target"
        error=1
      elif [ ! -f "$target_credentials" ]; then
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
