#!/bin/bash
# Omarchy rules: unquoted test variables [omarchy-style:4], numeric tests
# [omarchy-style:5], explicit alternatives [omarchy-style:6].
# Print a label for brief or full mode; exit 2 for any other invocation.

if (( $# != 1 )); then
  printf '%s\n' 'usage: choose_label.sh brief|full' >&2
  exit 2
else
  mode=$1
  if [[ $mode == "brief" ]]; then
    printf '%s\n' 'Ready'
  elif [[ $mode == "full" ]]; then
    printf '%s\n' 'Ready to continue'
  else
    printf 'unknown mode: %s\n' "$mode" >&2
    exit 2
  fi
fi
