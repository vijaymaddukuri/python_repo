#!/bin/sh
pip install flask
pip install robotframework
pip install requests
cd app/
python bing_bang_boom_server.py
echo "You're all set to play the BingBangBoom API based game"