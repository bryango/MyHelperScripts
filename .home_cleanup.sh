#!/bin/bash
# Clean up workspace
# shellcheck disable=SC2016

if [[ "$(git rev-parse --show-toplevel)" = "$HOME" ]]; then
	>&2 echo '# You are at $HOME, DANGER! Exiting ...'
	exit 1
fi

>&2 echo   '# This will clean up the workspace, ALL WILL BE LOST!'
>&2 printf '# ... Are you sure? If so, type `yes`: '

read -r affirm
if [[ "$affirm" = 'yes' ]]; then
	git checkout -- .
	git clean -dfx
fi

# vim: set noexpandtab:
