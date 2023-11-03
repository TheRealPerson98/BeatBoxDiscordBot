import json
import logging
import os
import platform
import random
import sys

from bot.utils.level_utils import LevelUtils

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv
from bot.db import create_tables, get_last_message_time, set_last_message_time, update_message_count, get_level,get_ban_queue, remove_from_ban_queue, remove_from_members
from bot.utils.ban import perform_ban_web
from config import logger
from bot.utils.guild_info import update_guild_info
import asyncio
from datetime import datetime
from pytz import utc
from datetime import timezone

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json", encoding='utf-8') as file:
        config = json.load(file)

# Discord Bot setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=intents,
            help_command=None,
        )
        """
        This creates custom bot variables so that we can access these variables in cogs more easily.

        For example, The config is available using the following code:
        - self.config # In this class
        - bot.config # In this file
        - self.bot.config # In cogs
        """
        self.logger = logger
        self.guild = None

    async def load_cogs(self) -> None:
        """
        The code in this function is executed whenever the bot will start.
        """
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"bot.cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    @tasks.loop(minutes=1.0)
    async def update_members_task(self) -> None:
        await update_guild_info(bot)
        

            
    @update_members_task.before_loop
    async def before_status_task(self) -> None:
        """
        Before starting the status changing task, we make sure the bot is ready
        """
        await self.wait_until_ready()
            
    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        statuses = ["Fuck You", "EAT ME", "your dad"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        """
        Before starting the status changing task, we make sure the bot is ready
        """
        await self.wait_until_ready()
        
        
    @tasks.loop(minutes=0.1)
    async def ban_task(self) -> None:
        """
        Ban users from the ban queue.
        """
        self.logger.info("Doing bans")
        if self.guild is None:
            self.logger.error("Guild is None!")
            return  # Exit early if guild is None
        
        queue = get_ban_queue()  # Function to get the ban queue from the database
        self.logger.info(queue)
        for user_id, reason in queue:
            await perform_ban_web(self, user_id, reason)  # Function to ban the user
            remove_from_ban_queue(user_id)  # Function to remove the user from the ban queue
            remove_from_members(user_id)  # Function to remove the user from the members table




    @ban_task.before_loop
    async def before_status_task(self) -> None:
        """
        Before starting the ban task, we make sure the bot is ready.
        """
        await self.wait_until_ready()
        
        
    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        create_tables()
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info("-------------------")
        
        await self.load_cogs()
        self.status_task.start()
        self.update_members_task.start()
        self.ban_task.start()

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return

        update_message_count(message.author.id)

        last_message_time = get_last_message_time(message.author.id)
        now = datetime.utcnow().replace(tzinfo=timezone.utc)  # make the datetime object timezone-aware

        if last_message_time:
            try:
                last_message_time = datetime.strptime(last_message_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
                time_difference = now - last_message_time

                if time_difference.total_seconds() > 30:  # 30 seconds threshold
                    old_level = get_level(message.author.id)
                    LevelUtils.add_xp(message.author.id, 5)  # 5 XP per message
                    new_level = get_level(message.author.id)

                    if new_level > old_level:
                        # Load configuration from config.json
                        with open('config.json') as f:
                            config = json.load(f)

                        # Channel where the level up message will be sent
                        channel = message.guild.get_channel(int(config['level_up_channel_id']))

                        if channel is not None:
                            embed = discord.Embed(
                                title=config['level_up_title'],
                                description=config['level_up_message'].format(mention=message.author.mention, level=new_level),
                                color=int(config['level_up_color'], 16),
                            )
                            embed.set_thumbnail(url=message.author.avatar.url)
                            embed.set_footer(text=f"User ID: {message.author.id}")

                            await channel.send(embed=embed)

                    set_last_message_time(message.author.id, now.strftime('%Y-%m-%d %H:%M:%S'))
            except ValueError:
                print(f"Invalid last_message_time format: {last_message_time}")
        else:
            set_last_message_time(message.author.id, now.strftime('%Y-%m-%d %H:%M:%S'))

        await self.process_commands(message)

    async def on_ready(self):
        # When the bot is ready, set the guild attribute to the appropriate value
        guild_id = int(config['DISCORD_GUILD_ID'])  # Convert guild ID to integer
        self.guild = self.get_guild(guild_id)
        if self.guild is None:
            self.logger.error("Guild not found!")
        else:
            self.logger.info("Guild found: %s", self.guild.name)


    async def on_member_join(self, member):
        await update_guild_info(bot)

        # Load configuration from config.json
        with open('config.json') as f:
            config = json.load(f)

        # Channel where the welcome message will be sent
        channel = member.guild.get_channel(int(config['welcome_channel_id']))

        if channel is not None:
            embed = discord.Embed(
                title=f"Welcome to {member.guild.name}!",
                description=config['welcome_message'].format(
                    mention=member.mention,
                    rules_channel_id=config['rules_channel_id'],
                    announcements_channel_id=config['announcements_channel_id'],
                    introductions_channel_id=config['introductions_channel_id']
                ),
                color=int(config['welcome_color'], 16),
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            embed.set_footer(text=f"User ID: {member.id} • Joined on {member.joined_at.strftime('%B %d, %Y')}")

            await channel.send(embed=embed)
            
    async def on_member_remove(self, member):
        self.logger.info(f"Member {member} has left the server.")
        remove_from_members(str(member.id))  # Remove the member from the members table


    async def on_command_completion(self, context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed.

        :param context: The context of the command that has been executed.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
            )

    async def on_command_error(self, context: Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error.

        :param context: The context of the normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description="You are not the owner of the bot!", color=0xE02B2B
            )
            await context.send(embed=embed, ephemeral=True)
            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot."
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code and they are the first word in the error message.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=True)
        else:
            raise error

load_dotenv()

bot = DiscordBot()
bot.run((TOKEN))

