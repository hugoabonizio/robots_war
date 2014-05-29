#!/bin/bash
echo "Initializing server on port $1"
PORT=$1
python server.py $PORT &
python game.py localhost $PORT &
python game.py localhost $PORT &

read -p ">" && killall python