import discord

async def purge_messages(context, amount: int):
    await context.send("Deleting messages...")
    purged_messages = await context.channel.purge(limit=amount + 1)
    embed = discord.Embed(
        description=f"**{context.author}** cleared **{len(purged_messages)-1}** messages!",
        color=0xBEBEFE,
    )
    await context.channel.send(embed=embed)
