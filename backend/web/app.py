from flask import Flask, request, jsonify, make_response, redirect
import discordoauth2
from bot.db import fetch_members, add_to_ban_queue
from config import logger
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS
import json

load_dotenv()
with open('bot/config.json', encoding='utf-8') as f:
    config = json.load(f)
    
# Define your constants here
CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
FRONTEND_URI = os.getenv("FRONTEND_URI")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(config['DISCORD_GUILD_ID'])
# Add the BOT_TOKEN for Discord

client = discordoauth2.Client(CLIENT_ID, secret=SECRET, redirect=REDIRECT_URI)

app = Flask(__name__)
CORS(app)


@app.route('/auth/discord')
def discord_auth():
    url = client.generate_uri(scope=["identify", "guilds", "guilds.members.read"])
    print(f"Redirecting to: {url}")  # Log the URL
    return redirect(url)

@app.route("/oauth2/callback")
def oauth2_callback():
    code = request.args.get("code")
    logger.info(f"Exchange Code: {code}")
    access = client.exchange_code(code)
    identify = access.fetch_identify()
    logger.info(f"Identify Response: {identify}")
    guilds = access.fetch_guilds()

    my_guild = next((g for g in guilds if g["id"] == str(GUILD_ID)), None)  # Note the conversion to string here
    
    if not my_guild:
        logger.error("User is not part of the expected guild.")
        return redirect(FRONTEND_URI)

    member_info = fetch_guild_member(access.token, str(GUILD_ID))
    roles = member_info.get("roles", [])
    logger.info(f"Roles: {roles}")

    # Save roles to cookies and redirect to frontend
    resp = make_response(redirect(FRONTEND_URI))
    for role_id in roles:
        role_name = get_role_name(role_id)
        resp.set_cookie(f'role_{role_name}', role_id, httponly=False, samesite='Lax')
    return resp

@app.route('/members')
def get_members():
    members_list = fetch_members()
    return jsonify(members_list)

def fetch_guild_member(token, guild_id):
    response = requests.get(f"https://discord.com/api/v10/users/@me/guilds/{guild_id}/member", headers={
        "authorization": f"Bearer {token}"
    })
    return response.json() if response.ok else {}

@app.route('/mute', methods=['POST'])
def mute():
    # Logic for muting a member
    # TODO: Add your logic here
    return jsonify({"status": "success", "message": "Member muted"})

@app.route('/ban', methods=['POST'])
def ban():
    user_id = request.json.get('user_id')
    reason = request.json.get('reason', 'Not specified')
    
    if not user_id:
        return jsonify({"status": "fail", "message": "User ID is required"})
    
    print("Received user ID from client:", user_id)  # Log the user ID
    add_to_ban_queue(user_id, reason)
    
    return jsonify({"status": "success", "message": "Member added to ban queue"})







@app.route('/kick', methods=['POST'])
def kick():
    # Logic for kicking a member
    # TODO: Add your logic here
    return jsonify({"status": "success", "message": "Member kicked"})

def fetch_guild_roles():
    """Fetches all roles from the Discord server."""
    headers = {
        "Authorization": f"Bot {TOKEN}"
    }
    print(headers)
    response = requests.get(f"https://discord.com/api/v10/guilds/1152659783439097966/roles", headers=headers)
    print(response)
    return response.json() if response.ok else []

def get_role_name(role_id):
    """Given a role ID, fetches the role name."""
    roles = fetch_guild_roles()
    for role in roles:
        if role['id'] == role_id:
            return role['name']
    return ''

def run_flask():
    try:
        app.run(port=5000)
    except Exception as e:
        logger.error(f"Error in Flask: {e}")

if __name__ == "__main__":
    run_flask()
