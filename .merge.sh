#!/bin/bash
# Merge HOME to publish

if [[ "$(git rev-parse --abbrev-ref HEAD)" != "publish" ]]; then
	echo "# Not on publish branch! Aborted."
	exit 1
elif stats=$(git status -M --porcelain) && [[ -z "$stats" ]]; then
	git merge --squash --no-commit HOME
	git reset HEAD .
	echo "$stats" \
		| sed --quiet 's/^ *M *//p' \
		| while IFS= read -r line || [[ -n "$line" ]]; do
			git add "$line";
		done
else
	echo "# Workspace is not clean! Clean up first."
	exit 1
fi
