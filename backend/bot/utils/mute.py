import discord
from discord.ext import commands
import asyncio

async def perform_mute(context, user, duration, reason="Not specified", silent=True):
    member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
    muted_role = discord.utils.get(context.guild.roles, name='Muted')  # Change 'Muted' to the name of your muted role
    if muted_role is None:
        await context.send('Muted role not found. Please create a role named "Muted" with appropriate permissions.')
        return
    
    if member.guild_permissions.administrator:
        embed = discord.Embed(description="User has administrator permissions.", color=0xE02B2B)
        await context.send(embed=embed, ephemeral=silent)
    else:
        try:
            embed = discord.Embed(
                description=f"**{member}** was muted by **{context.author}** for {duration} minutes!",
                color=0xBEBEFE,
            )
            embed.add_field(name="Reason:", value=reason)
            await context.send(embed=embed, ephemeral=silent)
            try:
                await member.send(
                    f"You were muted by **{context.author}** in **{context.guild.name}** for {duration} minutes!\nReason: {reason}"
                )
            except:
                pass  # Couldn't send a message in the private messages of the user
            
            await member.add_roles(muted_role, reason=reason)
            await asyncio.sleep(duration * 60)  # Wait for the specified duration in minutes
            await member.remove_roles(muted_role, reason='Mute duration expired.')
        except:
            embed = discord.Embed(
                description="An error occurred while trying to mute the user. Make sure my role is above the role of the user you want to mute.",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=silent)
