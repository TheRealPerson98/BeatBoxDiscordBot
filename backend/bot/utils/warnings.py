import discord
from bot.db import add_warn, remove_warn, get_warns

async def warning_main(context):
    if context.invoked_subcommand is None:
        embed = discord.Embed(
            description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add a warning to a user.\n`remove` - Remove a warning from a user.\n`list` - List all warnings of a user.",
            color=0xE02B2B,
        )
        await context.send(embed=embed, ephemeral=True)

async def warning_add(context, bot, user, reason="Not specified", silent=True):
    member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
    add_warn(user.id, context.author.id, reason)
    warnings_list = get_warns(user.id)
    total = len(warnings_list)
    embed = discord.Embed(
        description=f"**{member}** was warned by **{context.author}**!\nTotal warns for this user: {total}",
        color=0xBEBEFE,
    )
    embed.add_field(name="Reason:", value=reason)
    await context.send(embed=embed, ephemeral=silent)
    try:
        await member.send(
            f"You were warned by **{context.author}** in **{context.guild.name}**!\nReason: {reason}"
        )
    except:
        await context.send(
            f"{member.mention}, you were warned by **{context.author}**!\nReason: {reason}"
        )

async def warning_remove(context, bot, user, warn_id, silent=True):
    member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
    remove_warn(warn_id)
    warnings_list = get_warns(user.id)
    total = len(warnings_list)
    embed = discord.Embed(
        description=f"I've removed the warning **#{warn_id}** from **{member}**!\nTotal warns for this user: {total}",
        color=0xBEBEFE,
    )
    await context.send(embed=embed, ephemeral=silent)

async def warning_list(context, bot, user, silent=True):
    warnings_list = get_warns(user.id)
    embed = discord.Embed(title=f"Warnings of {user}", color=0xBEBEFE)
    description = ""
    if not warnings_list:
        description = "This user has no warnings."
    else:
        for warning in warnings_list:
            description += f"• Warned by <@{warning[1]}>: **{warning[2]}** (at {warning[3]}) - Warn ID #{warning[0]}\n"
    embed.description = description
    await context.send(embed=embed, ephemeral=silent)
