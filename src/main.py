import discord
from discord.ext import commands
import json
import asyncio
import os

with open("config.json") as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a microwave heat up."))

    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    try:
        synced = await bot.tree.sync()
        print(f"🔧 Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

async def load_cogs():
    for folder in ("commands", "functions"):
        for filename in os.listdir(f"./{folder}"):
            if filename.endswith(".py"):
                await bot.load_extension(f"{folder}.{filename[:-3]}")
                print(f"📦 Loaded cog: {folder}/{filename}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(config["token"])

asyncio.run(main())