import discord
from discord import app_commands
from discord.ext import commands

class pingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="🤖 Check the bot's latency to Discord's servers.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'🏓 Pong! {round(self.bot.latency * 1000)}ms', 
                                                ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(pingCog(bot))