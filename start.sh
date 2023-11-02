#!/bin/bash

# Start the bot
gnome-terminal -- bash -c "cd backend && python main.py; exec bash"

# Start the web app
gnome-terminal -- bash -c "cd backend && python -m web.app; exec bash"

# Start the React app
gnome-terminal -- bash -c "cd frontend && npm start; exec bash"
