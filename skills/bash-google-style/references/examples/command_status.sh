#!/bin/bash
# Google rules: separate local declaration [google-shell:93],
# command substitution [google-shell:60], function docs [google-shell:22].
# Resolve one command name using Bash's command builtin; do not execute it.

# Globals: PATH (read by command). Args: exactly one command name.
# Stdin: unused. Stdout: resolution. Stderr: usage or missing-command message.
# Returns: 2 for usage, command's status if lookup fails, printf's otherwise.
main() {
  if (( $# != 1 )); then
    printf '%s\n' 'usage: command_status.sh NAME' >&2
    return 2
  fi

  local resolved
  local status
  # A combined local declaration would hide the lookup's exit status.
  if resolved=$(command -v -- "$1"); then
    printf '%s\n' "${resolved}"
  else
    status=$?
    printf 'command not found: %s\n' "$1" >&2
    return "${status}"
  fi
}

main "$@"
