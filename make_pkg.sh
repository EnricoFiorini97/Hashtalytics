#!/bin/bash

gcc -o launcher_bin launcher.c
if [[ -f "./launcher_bin" ]]
then
	./launcher_bin
else
	echo "Compilation failed - Mv to Linux!"
fi
