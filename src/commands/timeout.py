import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
import datetime
import re


class timeoutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parse_duration(self, duration: str) -> datetime.timedelta:
        time_regex = re.compile(r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?")
        match = time_regex.fullmatch(duration.lower().replace(" ", ""))
        if not match:
            raise ValueError("Invalid duration format. Use formats like '1d', '2h30m', '45s', etc.")

        days = int(match.group(1)) if match.group(1) else 0
        hours = int(match.group(2)) if match.group(2) else 0
        minutes = int(match.group(3)) if match.group(3) else 0
        seconds = int(match.group(4)) if match.group(4) else 0

        total_duration = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        if total_duration.total_seconds() == 0:
            raise ValueError("Duration must be greater than 0.")
        if total_duration.total_seconds() < 0:
            raise ValueError("Duration must be greater than 0.")
        if total_duration > datetime.timedelta(days=28):
            raise ValueError("Duration cannot exceed 28 days.")
        return total_duration

    @app_commands.command(name="timeout", description="Timeout a specific member in the server.")
    @app_commands.describe(member="The member you would like to timeout.",
                           reason="The reason you would like to timeout the member",
                           duration="The duration you would like to timeout the member")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member,
                      duration: str, reason: str = "No reason provided."):

        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message(
                "You don't have the correct permissions timeout members.", ephemeral=True
            )

        if not interaction.guild.me.guild_permissions.moderate_members:
            return await interaction.response.send_message(
                "I don't have the correct permissions to timeout members.", ephemeral=True
            )

        if member.id == interaction.user.id:
            return await interaction.response.send_message(
                "lol no", ephemeral=True
            )

        if member.id == interaction.client.user.id:
            return await interaction.response.send_message(
                "lol no.", ephemeral=True
            )

        if member.id == interaction.guild.owner.id:
            return await interaction.response.send_message(
                "lol no.", ephemeral=True
            )

        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            return await interaction.response.send_message(
                "You cannot timeout someone with an equal or higher role to yourself.",
                ephemeral=True
            )

        if member.top_role >= interaction.guild.me.top_role:
            return await interaction.response.send_message(
                "I cannot timeout someone with an equal or higher role to my own.",
                ephemeral=True
            )

        try:
            until = discord.utils.utcnow() + self.parse_duration(duration)
            await member.timeout(until, reason=reason)
            await interaction.response.send_message(
                f"{member.mention} - {member.id} has been timed out for `{duration}`. \n ***Reason:*** `{reason}`")

        except discord.Forbidden:
            return await interaction.response.send_message(
                "I do not have the correct permissions to timeout this member.",
                ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Whoops... I encountered an error: {e}",
                                                    ephemeral=True)


async def setup(bot):
    await bot.add_cog(timeoutCog(bot))