import os
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from bot.utils.kick import perform_kick
from bot.utils.nickname import change_nickname
from bot.utils.ban import perform_ban
from bot.utils.warnings import warning_main, warning_add, warning_remove, warning_list
from bot.utils.purge import purge_messages
from bot.utils.hackban import hackban_user
from bot.utils.archive import archive_messages
from bot.utils.mute import perform_mute
from typing import List

class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="kick", description="Kick a user out of the server.")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @app_commands.describe(user="The user that should be kicked.", reason="The reason why the user should be kicked.")
    @app_commands.choices(silent=[
        app_commands.Choice(name="True", value="true"),
        app_commands.Choice(name="False", value="false"),
    ])
    async def kick(self, context: Context, user: discord.User, *, reason: str = "Not specified", silent: str = "true") -> None:
        silent_bool = True if silent == "true" else False
        await perform_kick(context, user, reason, silent_bool)

        
    @commands.hybrid_command(name="mute", description="Mute a user in the server.")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @app_commands.describe(user="The user that should be muted.", reason="The reason why the user should be muted.", duration="The duration of the mute in minutes.")
    @app_commands.choices(silent=[
        app_commands.Choice(name="True", value="true"),
        app_commands.Choice(name="False", value="false"),
    ])
    async def mute(self, interaction: discord.Interaction, user: discord.User, duration: int, reason: str = "Not specified", silent: str = "true"):
        # Convert the string back to boolean
        silent_bool = True if silent == "true" else False
        # Call your mute function here
        await perform_mute(interaction, user, duration, reason, silent_bool)
        
        

    @commands.hybrid_command(name="nick", description="Change the nickname of a user on a server.")
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @app_commands.describe(user="The user that should have a new nickname.", nickname="The new nickname that should be set.")
    @app_commands.choices(silent=[
        app_commands.Choice(name="True", value="true"),
        app_commands.Choice(name="False", value="false"),
    ])
    async def nick(self, context: Context, user: discord.User, *, nickname: str = None, silent: str = "true") -> None:
        silent_bool = True if silent == "true" else False
        await change_nickname(context, user, nickname, silent_bool)
        
    @commands.hybrid_command(name="ban", description="Bans a user from the server.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @app_commands.choices(silent=[
        app_commands.Choice(name="True", value="true"),
        app_commands.Choice(name="False", value="false"),
    ])
    @app_commands.describe(user="The user that should be banned.", reason="The reason why the user should be banned.")
    async def ban(self, context: Context, user: discord.User, *, reason: str = "Not specified", silent: str = "true") -> None:
        silent_bool = True if silent == "true" else False
        
        await perform_ban(context, user, reason, silent_bool)

    @commands.hybrid_group(name="warning", description="Manage warnings of a user on a server.")
    @commands.has_permissions(manage_messages=True)
    async def warning(self, context: Context) -> None:
        await warning_main(context)

    @warning.command(name="add", description="Adds a warning to a user in the server.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.choices(silent=[
        app_commands.Choice(name="True", value="true"),
        app_commands.Choice(name="False", value="false"),
    ])
    @app_commands.describe(user="The user that should be warned.",reason="The reason why the user should be warned.",)
    async def warning_add_command(self, context: Context, user: discord.User, *, reason: str = "Not specified", silent: str = "true") -> None:
        silent_bool = True if silent == "true" else False
        await warning_add(context, self.bot, user, reason, silent_bool)

    @warning.command(name="remove", description="Removes a warning from a user in the server.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.choices(silent=[
        app_commands.Choice(name="True", value="true"),
        app_commands.Choice(name="False", value="false"),
    ])
    @app_commands.describe(user="The user that should get their warning removed.", warn_id="The ID of the warning that should be removed.",)
    async def warning_remove_command(self, context: Context, user: discord.User, warn_id: int, silent: str = "true") -> None:
        silent_bool = True if silent == "true" else False
        await warning_remove(context, self.bot, user, warn_id, silent_bool)

    @warning.command(name="list", description="Shows the warnings of a user in the server.")
    @commands.has_guild_permissions(manage_messages=True)
    @app_commands.choices(silent=[
        app_commands.Choice(name="True", value="true"),
        app_commands.Choice(name="False", value="false"),
    ])
    @app_commands.describe(user="The user you want to get the warnings of.")
    async def warning_list_command(self, context: Context, user: discord.User, silent: str = "true") -> None:
        silent_bool = True if silent == "true" else False

        await warning_list(context, self.bot, user, silent_bool)

    @commands.hybrid_command(name="purge", description="Delete a number of messages.")
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @app_commands.describe(amount="The amount of messages that should be deleted.")
    async def purge(self, context: Context, amount: int) -> None:
        await purge_messages(context, amount)

    @commands.hybrid_command(name="hackban", description="Bans a user without the user having to be in the server.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @app_commands.choices(silent=[
        app_commands.Choice(name="True", value="true"),
        app_commands.Choice(name="False", value="false"),
    ])
    @app_commands.describe(user_id="The user ID that should be banned.", reason="The reason why the user should be banned.")
    async def hackban(self, context: Context, user_id: str, *, reason: str = "Not specified", silent: str = "true") -> None:
        silent_bool = True if silent == "true" else False
        await hackban_user(self.bot, context, user_id, reason, silent_bool)

    @commands.hybrid_command(name="archive", description="Archives in a text file the last messages with a chosen limit of messages.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(limit="The limit of messages that should be archived.")
    async def archive(self, context: Context, limit: int = 10) -> None:
        await archive_messages(context, limit)


        
async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))
