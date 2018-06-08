#!/bin/bash

(command -v python3 >/dev/null 2>&1 &&
python3 -c 'import sys; sys.exit(sys.hexversion < 0x0306000)') || {
	echo >&2 "Python 3.6 or later not found."
	echo >&2 "If you have python, use it to run bot.py."
	exit 1; }

cd "$(dirname "$BASH_SOURCE")"
python3 bot.py

