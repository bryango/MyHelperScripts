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
# shellcheck disable=1090
source "$HOME/.shrc"
export TOKEN_AQICN
IFS_BACKUP=$IFS
IFS=$'\n' && echo "${!ARGOS*}" \
	| while IFS= read -r var || [[ -n "$var" ]]; do
		export "${var?}";
	done
IFS=$IFS_BACKUP

if [[ -n $TOKEN_OPENWEATHERMAP ]] && [[ -n $LOCATION_OPENWEATHERMAP ]]; then
	weather=$(
	curl --silent "https://api.openweathermap.org/data/2.5/weather?\
appid=$TOKEN_OPENWEATHERMAP\
&q=$LOCATION_OPENWEATHERMAP\
&units=metric&lang=zh_cn" \
\
		| tr ',{}[]' '\n' \
		| grep 'description' \
		| tr -d '"' \
		| sed -E 's/description://g'
	)
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
