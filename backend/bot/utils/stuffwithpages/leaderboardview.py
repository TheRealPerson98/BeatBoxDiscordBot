import discord
from discord.ext import commands
from discord.ui import Button, View

class LeaderboardView(View):
    def __init__(self, bot, embeds):
        super().__init__(timeout=60)
        self.bot = bot
        self.embeds = embeds
        self.current_page = 0
        self.max_page = len(embeds) - 1

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def update_embed(self, interaction):
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.blurple)
    async def previous_button_callback(self, button, interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next_button_callback(self, button, interaction):
        if self.current_page < self.max_page:
            self.current_page += 1
            await self.update_embed(interaction)