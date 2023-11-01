import discord
from discord import app_commands
from discord.ext import commands
from bot.db import add_coins, remove_coins, get_coins
from discord.ext.commands import Context
from bot.db import get_leaderboard
from bot.utils.leaderboardview import LeaderboardView
from random import choice
import asyncio
import json

# Load configuration from config.json
with open('bot/config.json', encoding='utf-8') as f:
    config = json.load(f)

    
class Economy(commands.Cog, name="economy"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_group(name="eco", description="Economy commands.")
    @commands.has_permissions(manage_messages=True)
    async def eco(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add coins to a user's balance.\n`remove` - Remove coins from a user's balance.\n`balance` - Show the coin balance of a user.",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=True)

    @eco.command(name="add", description="Adds coins to a user's balance.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(user="The user that should receive coins.", amount="The amount of coins to add.")
    async def add_coins_command(self, context: commands.Context, user: discord.User, amount: int) -> None:
        add_coins(user.id, amount)
        embed = discord.Embed(
            title="🎉 Success!",
            description=f"**Added {amount} coins** to **{user.name}'s** balance.",
            color=0x5CDBF0,  # Light blue color
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await context.send(embed=embed, ephemeral=True)

    @eco.command(name="remove", description="Removes coins from a user's balance.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(user="The user that should lose coins.", amount="The amount of coins to remove.")
    async def remove_coins_command(self, context: commands.Context, user: discord.User, amount: int) -> None:
        remove_coins(user.id, amount)
        embed = discord.Embed(
            title="💸 Coins Removed",
            description=f"**Removed {amount} coins** from **{user.name}'s** balance.",
            color=0xE02B2B,  # Red color
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        embed.set_thumbnail(url="https://i.imgur.com/uIb860p.png")
        await context.send(embed=embed, ephemeral=True)

    @eco.command(name="balance", description="Displays the coin balance of a user.")
    @app_commands.describe(user="The user you want to get the balance of.")
    async def balance_command(self, context: commands.Context, user: discord.User = None) -> None:
        if user is None:
            user = context.author
        coins = get_coins(user.id)
        embed = discord.Embed(
            title="💰 Coin Balance",
            description=f"**{user.name}'s** balance: **{coins} coins**.",
            color=0xF0E05C,  # Yellow color
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        embed.set_thumbnail(url="https://i.imgur.com/uIb860p.png")
        await context.send(embed=embed, ephemeral=True)



    @eco.command(name="leaderboard", description="Displays the server's coin leaderboard")
    async def leaderboard_command(self, context: commands.Context) -> None:
        leaderboard = get_leaderboard()  # Assume this function returns a list of tuples (user_id, coins)
        leaderboard_embeds = []

        for i in range(0, len(leaderboard), 10):
            embed = discord.Embed(
                title="🏆 Coin Leaderboard",
                color=0xFFD700,  # Gold color
            )
            page = leaderboard[i:i + 10]

            for idx, (user_id, coins) in enumerate(page, start=i + 1):
                user = self.bot.get_user(user_id) or (await self.bot.fetch_user(user_id))
                embed.add_field(name=f"{idx}. {user.name}", value=f"{coins} coins", inline=False)

            embed.set_footer(text=f"Page {i // 10 + 1} of {(len(leaderboard) - 1) // 10 + 1}")
            leaderboard_embeds.append(embed)

        if not leaderboard_embeds:
            embed = discord.Embed(
                title="🏆 Coin Leaderboard",
                description="No data available.",
                color=0xFFD700,  # Gold color
            )
            await context.send(embed=embed)
        else:
            view = LeaderboardView(self.bot, leaderboard_embeds)
            view.message = await context.send(embed=leaderboard_embeds[0], view=view)
            
            
            
    async def coinflip_challenge(self, context, challenger_id, challenged_id, amount):
        challenger = context.guild.get_member(challenger_id)
        challenged = context.guild.get_member(challenged_id)

        embed = discord.Embed(
            title="Coin Flip Challenge",
            description=f"{challenged.mention}, you have been challenged to a coin flip by {challenger.mention} for {amount} coins. Do you accept?",
            color=0xF0E05C,  # Yellow color
        )
        message = await context.send(embed=embed)

        def check(reaction, user):
            return user.id == challenged_id and str(reaction.emoji) in ["✅", "❌"]

        await message.add_reaction("✅")
        await message.add_reaction("❌")

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await context.send(f"{challenged.mention} did not respond in time. The challenge is cancelled.")
            return

        if str(reaction.emoji) == "✅":
            await context.send(f"{challenged.mention} accepted the challenge!")
            await self.coinflip(context, challenger_id, challenged_id, amount)
        else:
            await context.send(f"{challenged.mention} declined the challenge.")

    async def coinflip(self, context, user_id, opponent_id, amount):
        result = choice(["win", "lose"])
        if result == "win":
            add_coins(user_id, amount)
            remove_coins(opponent_id, amount)
            winner = context.guild.get_member(user_id)
            loser = context.guild.get_member(opponent_id)
            message = f"Congratulations {winner.mention}! You won {amount} coins from {loser.mention}!"
        else:
            add_coins(opponent_id, amount)
            remove_coins(user_id, amount)
            winner = context.guild.get_member(opponent_id)
            loser = context.guild.get_member(user_id)
            message = f"Sorry {loser.mention}! You lost {amount} coins to {winner.mention}."

        embed = discord.Embed(
            title="🎲 Coin Flip Result",
            description=message,
            color=0x5CDBF0 if result == "win" else 0xE02B2B,
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

        await context.send(embed=embed)

    @commands.hybrid_command(name="coinflip", description="Flip a coin and potentially double your money!")
    @app_commands.describe(member="The member to challenge", amount="The amount of coins to bet.")
    async def coinflip_command(self, context: commands.Context, amount: int, member: discord.Member = None) -> None:
        user_id = context.author.id
        user_balance = get_coins(user_id)

        if amount <= 0:
            embed = discord.Embed(
                title="Error",
                description="You must bet a positive amount of coins.",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=True)
            return

        if amount > user_balance:
            embed = discord.Embed(
                title="Error",
                description="You don't have enough coins for this bet.",
                color=0xE02B2B,
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

            await context.send(embed=embed, ephemeral=True)
            return

        if member is not None:
            if member.id == user_id:
                embed = discord.Embed(
                    title="Error",
                    description="You can't challenge yourself to a coin flip.",
                    color=0xE02B2B,
                )
                embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

                await context.send(embed=embed, ephemeral=True)
                return
            await self.coinflip_challenge(context, user_id, member.id, amount)
        else:
            await self.coinflip(context, user_id, user_id, amount)  # Self-challenge for a normal coin flip
            
            
            
            
            
            
async def setup(bot) -> None:
    await bot.add_cog(Economy(bot))
