#!/bin/bash
# Google rules: arrays [google-shell:69], quoting [google-shell:57],
# function layout and argument forwarding [google-shell:96] [google-shell:98].
# Print arguments starting with a literal prefix. Requires Bash; no utilities.

# Globals: none. Args: prefix, then any number of strings. Stdin: unused.
# Stdout: matching strings, one per line. Stderr: usage on missing prefix.
# Returns: 2 for usage; otherwise the final output operation's status, or 0.
main() {
  if (( $# == 0 )); then
    printf '%s\n' 'usage: filter_prefix.sh PREFIX [STRING ...]' >&2
    return 2
  fi

  local prefix="$1"
  shift
  local item
  local -a matches=()
  for item in "$@"; do
    if [[ "${item}" == "${prefix}"* ]]; then
      matches+=("${item}")
    fi
  done

  if (( ${#matches[@]} > 0 )); then
    printf '%s\n' "${matches[@]}"
  else
    return 0
  fi
}

main "$@"
