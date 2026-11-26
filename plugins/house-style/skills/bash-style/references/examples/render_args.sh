#!/bin/bash
# House rules: quoted arrays, explicit status handling and CLI parsing
# [GOOGLE-SHELL] [SHELLCHECK]; nounset and pipefail [BASH-MANUAL].
# Executable, Bash 5.2+; no external commands. Use -- before dash-leading data.
set -u -o pipefail

# Args: [--prefix TEXT] [--] VALUE...; globals: none; stdin: unused.
# Stdout: one prefixed line per argument; stderr: usage errors.
# Returns: 0 on success, 2 for usage, or printf's failure status.
main() {
  local prefix='' value
  while (( $# > 0 )); do
    case "$1" in
      --prefix)
        if (( $# < 2 )); then
          printf '%s\n' '--prefix requires a value' >&2
          return 2
        fi
        prefix=$2
        shift 2
        ;;
      --)
        shift
        break
        ;;
      -*)
        printf 'unknown option: %s\n' "$1" >&2
        return 2
        ;;
      *) break ;;
    esac
  done
  local -a values=("$@")
  for value in "${values[@]}"; do
    printf '%s%s\n' "$prefix" "$value" || return "$?"
  done
}

main "$@"
