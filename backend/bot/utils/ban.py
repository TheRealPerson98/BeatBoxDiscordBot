import discord
from bot.db import add_punishment

async def perform_ban(context, user, reason="Not specified", silent=True):
    member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
    try:
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="User has administrator permissions.", color=0xE02B2B
            )
            await context.send(embed=embed, ephemeral=silent)
        else:
            embed = discord.Embed(
                description=f"**{member}** was banned by **{context.author}**!",
                color=0xBEBEFE,
            )
            embed.add_field(name="Reason:", value=reason)
            if not silent:
                await context.send(embed=embed, ephemeral=silent)
            try:
                if not silent:
                    await member.send(
                        f"You were banned by **{context.author}** from **{context.guild.name}**!\nReason: {reason}"
                    )
            except:
                pass  # Couldn't send a message in the private messages of the user
            add_punishment(user.id, context.author.id, "ban", reason)
            await member.ban(reason=reason)
    except:
        embed = discord.Embed(
            title="Error!",
            description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
            color=0xE02B2B,
        )
        await context.send(embed=embed, ephemeral=silent)
