import discord
import os
from datetime import datetime

async def archive_messages(context, limit: int = 10):
    log_file = f"{context.channel.id}.log"
    with open(log_file, "w", encoding="UTF-8") as f:
        f.write(
            f'Archived messages from: #{context.channel} ({context.channel.id}) in the guild "{context.guild}" ({context.guild.id}) at {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n'
        )
        async for message in context.channel.history(
            limit=limit, before=context.message
        ):
            attachments = []
            for attachment in message.attachments:
                attachments.append(attachment.url)
            attachments_text = (
                f"[Attached File{'s' if len(attachments) >= 2 else ''}: {', '.join(attachments)}]"
                if len(attachments) >= 1
                else ""
            )
            f.write(
                f"{message.created_at.strftime('%d.%m.%Y %H:%M:%S')} {message.author} {message.id}: {message.clean_content} {attachments_text}\n"
            )
    f = discord.File(log_file)
    await context.send(file=f)
    os.remove(log_file)
