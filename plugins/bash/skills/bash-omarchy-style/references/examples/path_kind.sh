#!/bin/bash
# Omarchy rules: fixed shebang [omarchy-style:8a], file tests [omarchy-style:3],
# quoted path arguments [omarchy-style:7], two-space indents [omarchy-style:2].
# Classify a path without opening it. Symlinks are classified before targets.

if (( $# != 1 )); then
  printf '%s\n' 'usage: path_kind.sh PATH' >&2
  exit 2
else
  path=$1
  if [[ -L $path ]]; then
    printf 'symlink: %s\n' "$path"
  elif [[ -d $path ]]; then
    printf 'directory: %s\n' "$path"
  elif [[ -f $path ]]; then
    printf 'file: %s\n' "$path"
  else
    printf 'unsupported or missing path: %s\n' "$path" >&2
    exit 1
  fi
fi
