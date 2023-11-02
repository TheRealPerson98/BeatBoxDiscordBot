# help.py
from discord.ext import commands
from discord.ui import Button, View
import discord
import json

# Load configuration from config.json
with open('bot/config.json', encoding='utf-8') as f:
    config = json.load(f)

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="AHHHHHHHHHH DADDY HELP ME.",
    )
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="Help",
            description="Click a button to see commands for each category.",
            color=0x5CDBF0,
        )

        view = View()

        categories = ["Util", "Eco", "Event", "Moderation", "Player"]
        for category in categories:
            button = Button(label=category)
            button.callback = self.create_callback(category)
            view.add_item(button)
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await ctx.send(embed=embed, view=view, ephemeral=True)

    def create_callback(self, category):
        async def callback(interaction):
            embed = discord.Embed(
                title=f"{category} Commands",
                description="Here are the commands for the " + category.lower() + " category.",
                color=0x5CDBF0,
            )

            if category == "Util":
                embed.add_field(name="/timer add", value="Add a timer.", inline=False)
                embed.add_field(name="/timer delete", value="Delete a timer.", inline=False)
                embed.add_field(name="/timer list", value="List all timers.", inline=False)
                embed.add_field(name="/timer view", value="View a timer.", inline=False)
            elif category == "Eco":
                embed.add_field(name="/eco add", value="Add coins to a user's balance.", inline=False)
                embed.add_field(name="/eco remove", value="Remove coins from a user's balance.", inline=False)
                embed.add_field(name="/eco balance", value="Show the coin balance of a user.", inline=False)
                embed.add_field(name="/eco leaderboard", value="Show the coin leaderboard.", inline=False)
                embed.add_field(name="/coinflip", value="Flip a coin.", inline=False)
            elif category == "Event":
                embed.add_field(name="/event register", value="Register for an event.", inline=False)
                embed.add_field(name="/event delete", value="Delete an event.", inline=False)
                embed.add_field(name="/event announce", value="Announce an event.", inline=False)
                embed.add_field(name="/event showqueue", value="Show the event queue.", inline=False)
            elif category == "Moderation":
                embed.add_field(name="/kick", value="Kick a user from the server.", inline=False)
                embed.add_field(name="/mute", value="Mute a user in the server.", inline=False)
                embed.add_field(name="/nick", value="Change a user's nickname.", inline=False)
                embed.add_field(name="/ban", value="Ban a user from the server.", inline=False)
                embed.add_field(name="/warning add", value="Add a warning to a user.", inline=False)
                embed.add_field(name="/warning remove", value="Remove a warning from a user.", inline=False)
                embed.add_field(name="/warning list", value="List all warnings for a user.", inline=False)
                embed.add_field(name="/purge", value="Purge messages in a channel.", inline=False)
                embed.add_field(name="/hackban", value="Ban a user without them being in the server.", inline=False)
                embed.add_field(name="/archive", value="Archive messages in a text file.", inline=False)
            elif category == "Player":
                embed.add_field(name="/daily", value="Claim daily coins and xp.", inline=False)
                embed.add_field(name="/stats", value="Show a user's stats.", inline=False)
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await interaction.response.send_message(embed=embed, ephemeral=True)

        return callback

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
