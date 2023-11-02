from discord.ext import commands
from discord.ext.commands import Context
import discord
from discord import app_commands
import asyncio
import json

with open('bot/config.json', encoding='utf-8') as f:
    config = json.load(f)

class Timer:
    def __init__(self, id, duration, user_id):
        self.id = id
        self.duration = duration
        self.user_id = user_id

class Util(commands.Cog, name="util"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.timers = []
        self.timer_id = 0

    @commands.hybrid_group(name="timer", description="Timer commands.")
    async def timer(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add a timer.\n`delete` - Delete a timer.\n`view` - View a timer.",
                color=0xE02B2B,
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await context.send(embed=embed, ephemeral=True)

    @timer.command(name="add", description="Add a timer.")
    @app_commands.describe(duration="The duration of the timer in seconds.")
    async def timer_add(self, context: Context, duration: int) -> None:
        timer_id = self.timer_id
        self.timer_id += 1
        timer = Timer(timer_id, duration, context.author.id)
        self.timers.append(timer)

        embed = discord.Embed(
            title="🕰️ Timer Added",
            description=f"Timer ID: {timer_id}\nDuration: {duration} seconds",
            color=0x5CDBF0,
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await context.send(embed=embed)

        await asyncio.sleep(duration - 10)

        embed = discord.Embed(
            title="⏰ Timer Countdown",
            description=f"Timer ID: {timer_id}\nTime remaining: 10 seconds",
            color=0xF0E05C,
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await context.send(embed=embed)

        await asyncio.sleep(10)

        embed = discord.Embed(
            title="🔔 Timer Up",
            description=f"Timer ID: {timer_id}\nTime's up!",
            color=0xE02B2B,
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await context.send(embed=embed)

    @timer.command(name="delete", description="Delete a timer.")
    @app_commands.describe(id="The ID of the timer.")
    async def timer_delete(self, context: Context, id: int) -> None:
        timer = next((t for t in self.timers if t.id == id and t.user_id == context.author.id), None)
        if timer is None:
            embed = discord.Embed(
                title="🛑 Timer Not Found",
                description="No timer found with the given ID.",
                color=0xE02B2B,
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await context.send(embed=embed)
            return

        self.timers.remove(timer)

        embed = discord.Embed(
            title="🗑️ Timer Deleted",
            description=f"Timer ID: {id} has been deleted.",
            color=0x5CDBF0,
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await context.send(embed=embed)

    @timer.command(name="view", description="View a timer.")
    @app_commands.describe(id="The ID of the timer.")
    async def timer_view(self, context: Context, id: int) -> None:
        timer = next((t for t in self.timers if t.id == id and t.user_id == context.author.id), None)
        if timer is None:
            embed = discord.Embed(
                title="🛑 Timer Not Found",
                description="No timer found with the given ID.",
                color=0xE02B2B,
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await context.send(embed=embed)
            return

        embed = discord.Embed(
            title="⏲️ Timer Details",
            description=f"Timer ID: {id}\nDuration: {timer.duration} seconds",
            color=0x5CDBF0,
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Util(bot))
