#!/bin/bash
# Wrapper for Argos AQI Widget

# Update python path & tokens
source "$HOME/.shrc"
export TOKEN_AQICN

# Important: correct path
cd "$HOME/.config/argos/aqi"
./widget.py

