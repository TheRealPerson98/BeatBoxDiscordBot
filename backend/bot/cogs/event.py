import discord
from discord import app_commands, Embed, ButtonStyle, ui
from discord.ext import commands
from bot.db import add_event, get_events, delete_event
from discord.ext.commands import Context
from datetime import datetime, timedelta
import pytz  
import asyncio
from discord.ui import Button
import json
from discord.ext import commands
from bot.utils.stuffwithpages.showqueueview import QueueView
from bot.utils.buttons.eventrolebutton import RoleButton

with open('bot/config.json', encoding='utf-8') as f:
    config = json.load(f)

    
class Event(commands.Cog, name="event"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_group(name="event", description="Event management commands.")
    @commands.has_permissions(manage_messages=True)
    async def event(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`register` - Register a new event.\n`stop` - Stop an event.",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=True)

    @event.command(name="register", description="Register a new event.")
    @commands.has_permissions(manage_messages=True)
    async def register_event_command(self, context: commands.Context) -> None:
        user = context.author
        dm_channel = await user.create_dm()

        # Send an ephemeral message in the guild to let the user know that the bot messaged them for the event setup
        embed = discord.Embed(
            title="📬 Check your Direct Messages",
            description="I've sent you a DM to guide you through the event setup process.",
            color=0x5CDBF0,
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

        await context.send(embed=embed, ephemeral=True)

        def check(m):
            return m.author == user and m.channel == dm_channel

        embed = discord.Embed(
            title="Event Registration",
            description="Let's get started with registering your event. What's the name of the event?",
            color=0x5CDBF0,
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

        await dm_channel.send(embed=embed)

        try:
            name_msg = await self.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="⏰ Time's Up!",
                description="You took too long to respond. Please start the registration process again.",
                color=0xE02B2B,
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

            await dm_channel.send(embed=embed)
            return
        name = name_msg.content

        date = ""
        time = ""
        while True:
            embed = discord.Embed(
                title="Event Date",
                description="Great! Now, what's the date of the event? Please use the format MM/DD/YYYY.",
                color=0x5CDBF0,
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await dm_channel.send(embed=embed)

            try:
                date_msg = await self.bot.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title="⏰ Time's Up!",
                    description="You took too long to respond. Please start the registration process again.",
                    color=0xE02B2B,
                )
                embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

                await dm_channel.send(embed=embed)
                return
            date = date_msg.content

            embed = discord.Embed(
                title="Event Time",
                description="Got it! Now, what's the time of the event? Please use the format HH:MM AM/PM.",
                color=0x5CDBF0,
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await dm_channel.send(embed=embed)

            try:
                time_msg = await self.bot.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title="⏰ Time's Up!",
                    description="You took too long to respond. Please start the registration process again.",
                    color=0xE02B2B,
                )
                embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

                await dm_channel.send(embed=embed)
                return
            time = time_msg.content

            try:
                dt = datetime.strptime(f"{date} {time}", "%m/%d/%Y %I:%M %p")
                break
            except ValueError as e:
                embed = discord.Embed(
                    title="🛑 Error",
                    description=f"Looks like there was an error with the date and time format. Please use the format MM/DD/YYYY for the date and HH:MM AM/PM for the time.",
                    color=0xE02B2B,
                )
                embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

                await dm_channel.send(embed=embed)
                continue

        embed = discord.Embed(
            title="Event Reward",
            description="Almost there! What's the reward for the event?",
            color=0x5CDBF0,
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

        await dm_channel.send(embed=embed)

        try:
            reward_msg = await self.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="⏰ Time's Up!",
                description="You took too long to respond. Please start the registration process again.",
                color=0xE02B2B,
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

            await dm_channel.send(embed=embed)
            return
        reward = reward_msg.content

        date_and_time = dt.strftime("%m/%d/%Y %I:%M %p")
        role = await context.guild.create_role(name=name)
        add_event(name, date_and_time, reward, 'US/Eastern', role.id)

        embed = discord.Embed(
            title="🎉 Event Registered!",
            description=f"Your event has been successfully registered.\n\n**Event Name:** {name}\n**Date:** {date_and_time}\n**Reward:** {reward}",
            color=0x5CDBF0,
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        await dm_channel.send(embed=embed)







    @event.command(name="delete", description="Delete an event.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.choices(
        name=[app_commands.Choice(name=event[1], value=event[1]) for event in get_events()],
    )
    @app_commands.describe(name="The name of the event to delete.")
    async def delete_event_command(self, context: commands.Context, name: str) -> None:
        role_id = delete_event(name)
        role = context.guild.get_role(role_id)
        if role:
            await role.delete()
        embed = discord.Embed(
            title="🗑️ Event Deleted!",
            description=f"The event **{name}** has been successfully deleted.",
            color=0x5CDBF0,  # Light blue color
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

        await context.send(embed=embed, ephemeral=True)

    @event.command(name="list", description="List all events.")
    @commands.has_permissions(manage_messages=True)
    async def list_events_command(self, context: commands.Context) -> None:
        events = get_events()  # Get all events from the database
        if not events:
            embed = discord.Embed(
                title="No Events",
                description="There are no events registered.",
                color=0xE02B2B,  # Red color
            )
            await context.send(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(
            title="📅 Upcoming Events",
            color=0x5CDBF0,  # Light blue color
        )
        for event_id, name, date_and_time, reward, timezone, role_id in events:
            # Convert date and time to Unix timestamp for Discord timestamp styling
            unix_timestamp = int(datetime.strptime(date_and_time, "%m/%d/%Y %I:%M %p").timestamp())
            
            role = context.guild.get_role(role_id)
            role_mention = role.mention if role else "Role not found"
            embed.add_field(name=name, value=f"**Time:** <t:{unix_timestamp}:f> (<t:{unix_timestamp}:R>)\n**Reward:** {reward}\n**Role:** {role_mention}", inline=False)
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])

        await context.send(embed=embed, ephemeral=True)



    @event.command(name="announce", description="Announce an event.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.choices(
        event_name=[app_commands.Choice(name=event[1], value=event[1]) for event in get_events()],
        mention=[
            app_commands.Choice(name="@everyone", value="everyone"),
            app_commands.Choice(name="@here", value="here"),
        ],
    )
    @app_commands.describe(event_name="The name of the event to announce.", mention="Who to mention in the announcement.", title="The title of the announcement.", description="The description of the announcement.", image="The image to include in the announcement.", include_buttons="Whether to include the Join and Leave Queue buttons.")
    async def announce_event_command(self, context: commands.Context, event_name: str, mention: str, title: str, description: str, image: discord.Attachment, include_buttons: bool) -> None:
        events = get_events()
        event = next((e for e in events if e[1] == event_name), None)
        if event is None:
            embed = discord.Embed(
                title="🛑 Event Not Found",
                description="The event you are trying to announce could not be found. Please check the event name and try again.",
                color=0xE02B2B,  # Red color
            )
            await context.send(embed=embed, ephemeral=True)
            return
        
        _, _, date_and_time, reward, _, role_id = event
        
        # Convert date and time to Unix timestamp for Discord timestamp styling
        unix_timestamp = int(datetime.strptime(date_and_time, "%m/%d/%Y %I:%M %p").timestamp())
        
        mention_str = "@everyone" if mention == "everyone" else "@here"
        embed = discord.Embed(
            title=f"📢 {title}",
            description=f"{description}\n\n**Date and Time:** <t:{unix_timestamp}:f> (<t:{unix_timestamp}:R>)\n**Reward:** {reward}",
            color=0x5CDBF0,  # Light blue color
        )
        embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
        embed.set_image(url=image.url)
        
        msg = await context.send(f"{mention_str}")
        await asyncio.sleep(1)  # Wait for 1 second before deleting the mention message
        await msg.delete()
        
        if include_buttons:
            await context.send(embed=embed, view=RoleButton(role_id))
        else:
            await context.send(embed=embed)
            
            
    @event.command(name="showqueue", description="Show the queue for an event.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.choices(
        event_name=[app_commands.Choice(name=event[1], value=event[1]) for event in get_events()],
    )
    @app_commands.describe(event_name="The name of the event.", silent="Whether to show the queue silently.")
    async def show_queue_command(self, context: commands.Context, event_name: str, silent: bool) -> None:
        events = get_events()
        event = next((e for e in events if e[1] == event_name), None)
        if event is None:
            embed = discord.Embed(
                title="🛑 Event Not Found",
                description="The event you are trying to announce could not be found. Please check the event name and try again.",
                color=0xE02B2B,  # Red color
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await context.send(embed=embed, ephemeral=True)
            return
        
        _, _, _, _, _, role_id = event
        role = context.guild.get_role(role_id)
        if role is None:
            embed = discord.Embed(
                title="🛑 Role Not Found",
                description="The role for the event could not be found. Please check the event configuration.",
                color=0xE02B2B,  # Red color
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await context.send(embed=embed, ephemeral=True)
            return
        
        members = role.members
        if not members:
            embed = discord.Embed(
                title="Queue is Empty",
                description="There are no members in the queue for this event.",
                color=0xE02B2B,  # Red color
            )
            embed.set_footer(text=config['bot_name'], icon_url=config['bot_icon_url'])
            await context.send(embed=embed, ephemeral=silent)
            return
        
        pages = []
        for i in range(0, len(members), 25):
            embed = discord.Embed(
                title=f"Queue for {event_name}",
                color=0x5CDBF0,  # Light blue color
            )
            page_members = members[i:i + 25]
            member_mentions = "\n".join(member.mention for member in page_members)
            embed.description = member_mentions
            pages.append(embed)
        
        view = QueueView(self.bot, pages)
        message = await context.send(embed=pages[0], view=view, ephemeral=silent)
        view.message = message


        
        
        
async def setup(bot) -> None:
    await bot.add_cog(Event(bot))
