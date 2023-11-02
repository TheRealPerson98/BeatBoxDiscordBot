import discord

class RoleButton(discord.ui.View):
    def __init__(self, role_id: int):
        super().__init__()
        self.role_id = role_id
        
    @discord.ui.button(label="Join Queue", style=discord.ButtonStyle.green, custom_id="join_queue")
    async def join_queue(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.role_id)
        if role is None:
            print(f"Role not found with ID: {self.role_id}")
            embed = discord.Embed(
                title="Error",
                description="Role not found.",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.user.add_roles(role)
        embed = discord.Embed(
            title="Joined Queue",
            description="You have successfully joined the queue.",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @discord.ui.button(label="Leave Queue", style=discord.ButtonStyle.red, custom_id="leave_queue")
    async def leave_queue(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.role_id)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = discord.Embed(
                title="Left Queue",
                description="You have successfully left the queue.",
                color=discord.Color.green(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="Not in Queue",
                description="You are not in the queue.",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
