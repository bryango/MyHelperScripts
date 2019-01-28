#!/bin/bash
# Wrapper for Argos AQI Widget

# Don't bother when no network
if nmcli --get-values=STATE general status \
	| grep --quiet -E 'local only|disconnected'; then
		echo ""
		echo "---"
		exit 0
fi

# Update python path & tokens
source "$HOME/.shrc"
export TOKEN_AQICN
IFS_BACKUP=$IFS
IFS=$'\n' && echo "${!ARGOS*}" \
	| while IFS= read -r var || [[ -n "$var" ]]; do
		export "${var?}";
	done
IFS=$IFS_BACKUP

# Important: correct path
cd "$HOME/.config/argos/aqi"
./widget.py

echo   "---"
printf "* Executed: $(date +'%m-%d %H:%M')\\\n"
echo   "* Customize: \`constants.py\` | \
font='Anka/Coder Condensed' size=8 \
href='file://$(dirname "$0")/aqi/constants.py'"
