#!/usr/bin/env bash

now=$((10#$(date +%-H%M)))
sleeplen='8 hours 30 minutes'

markup="trim=false font='Anka/Coder Condensed'"
pre_style="<span color='white' background='grey' weight='bold'><tt>"
post_style="</tt></span>"

getup=$(date +%-H:%M -d "+ $sleeplen")
if [[ "$now" -gt 2100 ]] || [[ "$now" -lt 300 ]]; then
	echo "🌙 $getup|trim=false"
else
	echo ""
fi

echo "---"
echo "If you go to sleep NOW,|$markup"
echo " ... and sleep for $pre_style $sleeplen $post_style|$markup"
echo " ... you will wake up @ $pre_style $getup $post_style|$markup"
