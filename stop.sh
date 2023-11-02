#!/bin/bash

# Stop the bot
pkill -f "python main.py"

# Stop the web app
pkill -f "python -m web.app"

# Stop the React app
pkill -f "npm start"
