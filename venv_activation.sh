#!/bin/sh

VENV_DIR="v"

if [ "$1" = "on" ]; then
	if [ -f "$VENV_DIR/bin/activate" ]; then
		. "$VENV_DIR/bin/activate"
		echo "Virtual environment activated."
	else
		echo "ERROR: $VENV_DIR/bin/activate was not found."
	fi
elif [ "$1" = "off" ]; then
	if [ -n "$VIRTUAL_ENV" ]; then
		deactivate
		echo "Virtual environment deactivated."
	else
		echo "Virtual environment is not active."
	fi
else
	echo "Usage: . ./venv_activation [on|off]"
fi
