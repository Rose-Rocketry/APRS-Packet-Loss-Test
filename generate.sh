#!/usr/bin/bash

python generate.py | gen_packets -o packets.wav -
echo
echo
atest packets.wav | cat
