#!/bin/bash
PORT=8080
python server.py $PORT &
python game.py localhost $PORT &
python game.py localhost $PORT &