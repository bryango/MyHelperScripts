#!/bin/bash
# Wrapper for Argos AQI Widget

# Don't bother when no network
if nmcli --get-values=STATE general status \
	| grep --quiet -E 'local only|disconnected|connecting'; then
		echo ""
		echo "---"
		exit 0
fi

# Update python path & tokens
# shellcheck disable=1090
source "$HOME/.shrc"
export TOKEN_AQICN TOKEN_OPENWEATHERMAP

IFS_BACKUP=$IFS
IFS=$'\n' && echo "${!ARGOS*}" \
	| while IFS= read -r var && [[ -n "$var" ]] || [[ -n "$var" ]]; do
		>&2 echo "# export ${var?}"
		export "${var?}"
	done
IFS=$IFS_BACKUP

if [[ -n $TOKEN_OPENWEATHERMAP ]] && [[ -n $LOCATION_OPENWEATHERMAP ]]; then
	weather=$(curl-openweather "q=$LOCATION_OPENWEATHERMAP")
	[[ -z $weather ]] && weather='🜁'
	printf %s "$weather"
fi

# Important: correct path
cd "$HOME/.config/argos/aqi" || exit 1
./widget.py

echo   "---"
printf "* Executed: %s\\\n" "$(date +'%m-%d %H:%M')"
echo   "* Customize: \`constants.py\` | \
font='Anka/Coder Condensed' size=8 \
href='file://$(dirname "$0")/aqi/constants.py'"
