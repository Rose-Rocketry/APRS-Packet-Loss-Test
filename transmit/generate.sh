#!/usr/bin/bash

python3 generate.py | gen_packets -o packets.wav -
echo
echo
atest packets.wav | cat
