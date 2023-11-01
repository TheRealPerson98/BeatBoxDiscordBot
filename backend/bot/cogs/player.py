import discord
from discord import app_commands
from discord.ext import commands
from bot.db import add_coins, get_daily_usage, set_daily_usage, get_level, get_level_and_xp, get_coins, get_message_count
from bot.utils.level_utils import LevelUtils
from discord.ext.commands import Context
from bot.db import get_leaderboard
from bot.utils.leaderboardview import LeaderboardView
from random import choice
import asyncio
from discord.ext import commands
import discord
from datetime import datetime, timedelta
from pytz import utc
import json

# Load configuration from config.json
with open('bot/config.json', encoding='utf-8') as f:
    config = json.load(f)

    
class Player(commands.Cog, name="player"):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @commands.hybrid_command(name="daily", description="Claim daily coins.")
    async def daily_command(self, context: commands.Context) -> None:
        user_id = context.author.id
        last_used = get_daily_usage(user_id)
        now = datetime.utcnow()  # Use UTC time for consistency

        if last_used is not None:
            last_used = datetime.strptime(last_used, '%Y-%m-%d %H:%M:%S')  # Timestamp is already in UTC
            next_claim = last_used + timedelta(days=1)

            if now < next_claim:
                time_remaining = next_claim - now
                hours, remainder = divmod(time_remaining.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                embed = discord.Embed(
                    title="⏰ Daily Reward",
                    description=f"You have already claimed your Daily Rewards. You can claim again in {time_remaining.days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.",
                    color=0xE02B2B,
                )
                embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
                await context.send(embed=embed, ephemeral=True)
                return
        
        daily_coins = 100  # Amount of daily coins to give
        add_coins(user_id, daily_coins)
        old_level = get_level(user_id)
        new_level = LevelUtils.add_xp(user_id, daily_coins)  # Added XP when daily coins are claimed
        set_daily_usage(user_id)
        embed = discord.Embed(
            title="💰 Daily Coins",
            description=f"You claimed {daily_coins} daily coins. Come back tomorrow for more!",
            color=0x5CDBF0,
        )
        if new_level > old_level:
            embed.add_field(name="🎉 Level Up!", value=f"Congratulations! You've reached level {new_level}.", inline=False)
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

        await context.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="stats", description="View your stats or another player's stats.")
    async def stats_command(self, ctx, user: discord.User = None):
        if isinstance(ctx, commands.Context):
            if user is None:
                user = ctx.author
        elif isinstance(ctx, discord.Interaction):
            if user is None:
                user = ctx.user

        user_id = user.id
        level, xp = get_level_and_xp(user_id)
        next_level_xp = 100 * (1.1 ** (level - 1))
        xp_progress = int((xp / next_level_xp) * 100)

        last_used = get_daily_usage(user_id)
        now = datetime.now().astimezone()

        coin_balance = get_coins(user_id)
        message_count = get_message_count(user_id)
        if last_used is not None:
            last_used = datetime.strptime(last_used, '%Y-%m-%d %H:%M:%S').replace(tzinfo=utc)
            next_claim = last_used + timedelta(days=1)

            if now < next_claim:
                time_remaining = next_claim - now
                hours, remainder = divmod(time_remaining.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_until_next_daily = f"{time_remaining.days}d, {hours}h, {minutes}m, and {seconds}s"
            else:
                time_until_next_daily = "available now!"
        else:
            time_until_next_daily = "available now!"

        progress_bar_notches = 10
        filled_notches = int((xp_progress / 100) * progress_bar_notches)
        empty_notches = progress_bar_notches - filled_notches
        progress_bar = f"`[{'🟩' * filled_notches}{' ' * empty_notches}]`{xp_progress}%"

        embed = discord.Embed(
            title=f"📊 Stats for {user.display_name}",
            color=0x77DD77,  # changed the color to a light green
        )
        embed.set_thumbnail(url=user.avatar.url)  # added user's avatar as thumbnail
        embed.add_field(name="🧗‍♂️ Level", value=level, inline=True)
        embed.add_field(name="⚡ XP", value=f"{xp}/{int(next_level_xp)}", inline=True)
        embed.add_field(name="📊 Progress", value=progress_bar, inline=True)
        embed.add_field(name="🎁 Next Daily Reward", value=time_until_next_daily, inline=True)
        embed.add_field(name="💰 Coin Balance", value=coin_balance, inline=True)
        embed.add_field(name="💌 Total Messages Sent", value=message_count, inline=True)
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

        if isinstance(ctx, commands.Context):
            await ctx.send(embed=embed)
        elif isinstance(ctx, discord.Interaction):
            await ctx.response.send_message(embed=embed)



        
           
async def setup(bot) -> None:
    await bot.add_cog(Player(bot))
