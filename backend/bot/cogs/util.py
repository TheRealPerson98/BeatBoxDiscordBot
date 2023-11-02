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
                description=config['timer']['subcommand_description'],
                color=int(config['colors']['error'], 16),
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
            title=config['timer']['add']['title'],
            description=config['timer']['add']['description'].format(timer_id=timer_id, duration=duration),
            color=int(config['colors']['success'], 16),
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await context.send(embed=embed)

        for i in range(duration, 0, -1):
            if i in config['timer']['highlighted_times']:
                embed = discord.Embed(
                    title=config['timer']['highlight']['title'],
                    description=config['timer']['highlight']['description'].format(time=i),
                    color=int(config['colors']['highlight'], 16),
                )
                embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
                await context.send(embed=embed)
            elif i <= 10:
                embed = discord.Embed(
                    title=config['timer']['countdown']['title'],
                    description=str(i),
                    color=int(config['colors']['countdown'], 16),
                )
                embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
                await context.send(embed=embed)
            await asyncio.sleep(1)

        embed = discord.Embed(
            title=config['timer']['up']['title'],
            description=config['timer']['up']['description'],
            color=int(config['colors']['error'], 16),
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await context.send(embed=embed)

    @timer.command(name="delete", description="Delete a timer.")
    @app_commands.describe(id="The ID of the timer.")
    async def timer_delete(self, context: Context, id: int) -> None:
        timer = next((t for t in self.timers if t.id == id and t.user_id == context.author.id), None)
        if timer is None:
            embed = discord.Embed(
                title=config['timer']['delete']['not_found_title'],
                description=config['timer']['delete']['not_found_description'],
                color=int(config['colors']['error'], 16),
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await context.send(embed=embed)
            return

        self.timers.remove(timer)

        embed = discord.Embed(
            title=config['timer']['delete']['title'],
            description=config['timer']['delete']['description'].format(id=id),
            color=int(config['colors']['success'], 16),
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await context.send(embed=embed)

    @timer.command(name="view", description="View a timer.")
    @app_commands.describe(id="The ID of the timer.")
    async def timer_view(self, context: Context, id: int) -> None:
        timer = next((t for t in self.timers if t.id == id and t.user_id == context.author.id), None)
        if timer is None:
            embed = discord.Embed(
                title=config['timer']['view']['not_found_title'],
                description=config['timer']['view']['not_found_description'],
                color=int(config['colors']['error'], 16),
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await context.send(embed=embed)
            return

        embed = discord.Embed(
            title=config['timer']['view']['title'],
            description=config['timer']['view']['description'].format(id=id, duration=timer.duration),
            color=int(config['colors']['success'], 16),
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Util(bot))
