#!/bin/bash
# Clean up workspace
# shellcheck disable=SC2016

echo   '# This will clean up the workspace, ALL WILL BE LOST!'
printf '# ... Are you sure? If so, type `yes`: '

read -r affirm
if [[ "$affirm" = 'yes' ]]; then
	git checkout -- .
	git clean -dfx
fi
