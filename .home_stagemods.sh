#!/bin/bash
# Selectively stage HOME to publish

function gstats { git status -M --porcelain; }

if [[ "$(git rev-parse --abbrev-ref HEAD)" != "publish" ]]; then
	echo "# Not on publish branch! Aborted."
	exit 1
elif git merge HEAD &>/dev/null; then
	git reset HEAD .
	gstats \
		| sed --quiet 's/^ *M *//p' \
		| while IFS= read -r line || [[ -n "$line" ]]; do
			git add "$line";
		done
else
	echo "# Still merging! Resolve conflicts first."
	exit 1  # https://stackoverflow.com/a/30781568/10829731
fi
