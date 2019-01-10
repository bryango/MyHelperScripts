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

# Important: correct path
cd "$HOME/.config/argos/aqi"
./widget.py
