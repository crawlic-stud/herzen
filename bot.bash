#!/bin/bash

if [ $1 = build ]
then
    pip install -r requirements.txt
    echo "bot setup done"
elif [ $1 = run ] 
then
    python3 ./src/main.py > /dev/null &
    echo "bot started"
elif [ $1 = stop ]
then
    pkill -f ./src/main.py
    echo "bot stopped"
else
    echo $1 - "unknown command"
fi