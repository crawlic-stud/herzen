#!/bin/bash

key=$1

if [ $# -eq 0 ]
then
    echo "please provide Telegram API key"
else 
    pip install -r requirements.txt
    touch ./src/api_token.py
    echo "API_TOKEN = '${key}'" > ./src/api_token.py
    touch ./src/firebase_key.json
    echo "bot setup done"
fi
