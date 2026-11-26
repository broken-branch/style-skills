#!/bin/bash
# House rules: checked temporary-file producer and scoped cleanup [BASH-MANUAL];
# quoted paths and preserved failures [SHELLCHECK]; documented CLI [GOOGLE-SHELL].
# Executable, Bash 5.2+ and GNU mktemp, sort, cat, rm. Sort text lines to stdout.
set -u -o pipefail

# Trap state outlives main's locals. Relative TMPDIR paths start with ./.
temp_file=''
temp_root=${TMPDIR:-/tmp}
if [[ "$temp_root" != /* ]]; then
  temp_root=./$temp_root
fi
readonly temp_root

# Args: original status; globals: reads temp_file, temp_root; stdin/stdout: none.
# Stderr: cleanup diagnostics. Returns the original failure, or 1 if only
# cleanup failed. Only removes the exact mktemp path in the selected root.
cleanup() {
  local status=$1
  if [[ -n "$temp_file" && "$temp_file" == "$temp_root"/style-example.* ]]; then
    if rm -- "$temp_file"; then
      :
    else
      printf '%s\n' 'could not remove temporary file' >&2
      if (( status == 0 )); then
        status=1
      fi
    fi
  fi
  return "$status"
}

trap 'cleanup "$?"; exit "$?"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

# Args: [--unique] -- FILE; globals: sets temp_file, reads temp_root.
# Stdin: unused; stdout: sorted lines; stderr: usage or utility diagnostics.
# Returns: 0 on success, 2 for usage, otherwise the failing utility's status.
main() {
  local -a options=()
  local status
  if [[ "${1-}" == '--unique' ]]; then
    options+=(--unique)
    shift
  fi
  if (( $# != 2 )) || [[ "$1" != '--' || "$2" == '-' ]]; then
    printf '%s\n' 'usage: sort_lines.sh [--unique] -- FILE (use ./- for dash)' >&2
    return 2
  fi
  if temp_file=$(mktemp -- "$temp_root/style-example.XXXXXXXXXX"); then
    :
  else
    status=$?
    printf '%s\n' 'could not create temporary file' >&2
    return "$status"
  fi
  if LC_ALL=C sort "${options[@]}" -- "$2" >"$temp_file"; then
    cat -- "$temp_file" || return "$?"
  else
    return "$?"
  fi
}

main "$@"
