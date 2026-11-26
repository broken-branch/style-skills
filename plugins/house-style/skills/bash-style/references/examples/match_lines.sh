#!/bin/bash
# House rules: negative-result versus command-failure statuses [GOOGLE-SHELL];
# literal patterns, quoted operands and exact status capture [SHELLCHECK].
# Executable, Bash 5.2+ and GNU grep. Usage: match_lines.sh PATTERN FILE.
set -u -o pipefail

# Args: literal pattern, file path; globals: none; stdin: unused.
# Stdout: matching lines; stderr: usage or grep diagnostics.
# Returns: 0 for matches OR no matches, 2 for usage, grep's status on failure.
main() {
  local status
  if (( $# != 2 )); then
    printf '%s\n' 'usage: match_lines.sh PATTERN FILE' >&2
    return 2
  fi
  if [[ "$2" == '-' ]]; then
    printf '%s\n' 'use ./- for a file named dash; stdin is unsupported' >&2
    return 2
  fi
  if grep -F -- "$1" "$2"; then
    return 0
  else
    status=$?
    case "$status" in
      1) return 0 ;;
      *) return "$status" ;;
    esac
  fi
}

main "$@"
