#!/usr/bin/env bash
# Spin down HDD - Argos Widget

echo "| iconName=media-removable"
echo "---"

fontset="font='Anka/Coder Condensed' size=11.5"
bashcmd="bash='gnome-terminal --maximize -- udisksctl-off' terminal=false"

if [ "$ARGOS_MENU_OPEN" == "true" ]; then

	export GREP_COLORS=ne
	drives_info=$(lsblk-more \
		| GREP_COLOR='01;33' grep -E --color=always '/run/media/|$' \
		| awk 1 ORS="\\\\n" \
		| sed -e 's/ *\\n/\\n/g' \
		| head -c -2)  # Remove trailing whitespace & the last newline

	echo "<span weight='bold'>$drives_info</span> | $fontset $bashcmd"

else
	echo "Loading... | $fontset $bashcmd"
fi
