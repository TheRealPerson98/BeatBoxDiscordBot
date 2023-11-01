import discord

async def change_nickname(context, user, nickname=None, silent=True):
    member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
    try:
        await member.edit(nick=nickname)
        embed = discord.Embed(
            description=f"**{member}'s** new nickname is **{nickname}**!",
            color=0xBEBEFE,
        )
        await context.send(embed=embed, ephemeral=silent)
    except:
        embed = discord.Embed(
            description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
            color=0xE02B2B,
        )
        await context.send(embed=embed, ephemeral=silent)
