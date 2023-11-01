import discord

async def hackban_user(bot, context, user_id: str, reason: str, silent=True):
    try:
        await bot.http.ban(user_id, context.guild.id, reason=reason)
        user = bot.get_user(int(user_id)) or await bot.fetch_user(int(user_id))
        embed = discord.Embed(
            description=f"**{user}** (ID: {user_id}) was banned by **{context.author}**!",
            color=0xBEBEFE,
        )
        embed.add_field(name="Reason:", value=reason)
        await context.send(embed=embed, ephemeral=silent)
    except Exception:
        embed = discord.Embed(
            description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
            color=0xE02B2B,
        )
        await context.send(embed=embed, ephemeral=silent)
