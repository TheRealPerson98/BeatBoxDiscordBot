# guild_info.py

import json
import logging
import os
from dotenv import load_dotenv
from bot.db import update_members_db, create_tables, update_guild_name
import sys
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Load config.json
with open('bot/config.json', encoding='utf-8') as f:
    config = json.load(f)

GUILD_ID = int(config['DISCORD_GUILD_ID'])



# guild_info.py

async def update_guild_info(bot):
    guild = bot.get_guild(GUILD_ID)
    if guild:
        logger.info(f"Found guild: {guild.name}")

        members_data = []
        async for member in guild.fetch_members():
            if not member.bot:
                roles = [role.name for role in member.roles if role.name != "@everyone"]
                role_str = ', '.join(roles) if roles else None
                
                members_data.append((
                    member.id,
                    member.name,
                    member.nick,
                    role_str,
                    str(member.status),
                    str(member.joined_at),
                    str(member.created_at),
                    str(member.top_role.name)
                ))
                
        update_guild_name(guild.name)
        update_members_db(members_data)
    else:
        bot.logger.warning("Couldn't find the guild.")


