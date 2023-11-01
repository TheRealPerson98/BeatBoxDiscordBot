import discord
from discord.ext import commands

async def perform_kick(context, user, reason="Not specified", silent=True):
    member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
    if member.guild_permissions.administrator:
        embed = discord.Embed(description="User has administrator permissions.", color=0xE02B2B)
        await context.send(embed=embed, ephemeral=silent)
    else:
        try:
            embed = discord.Embed(
                description=f"**{member}** was kicked by **{context.author}**!",
                color=0xBEBEFE,
            )
            embed.add_field(name="Reason:", value=reason)
            if not silent:
                await context.send(embed=embed)
            try:
                if not silent:
                    await member.send(
                        f"You were kicked by **{context.author}** from **{context.guild.name}**!\nReason: {reason}"
                    )
            except:
                pass  # Couldn't send a message in the private messages of the user
            await member.kick(reason=reason)
        except:
            embed = discord.Embed(
                description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=silent)
