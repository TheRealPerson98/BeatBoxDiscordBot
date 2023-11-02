#!/bin/bash

# Start the bot
cd backend
pip install -r requirements.txt
python main.py &

# Start the web app
cd backend
pip install -r requirements.txt
python -m web.app &

# Start the React app
cd frontend
npm install
npm start &
