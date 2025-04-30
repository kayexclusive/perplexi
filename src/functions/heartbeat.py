import discord
from discord.ext import commands, tasks
import datetime

class Heartbeat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.health_check.start()

    def cog_unload(self):
        self.health_check.cancel()

    @tasks.loop(minutes=5.0)
    async def health_check(self):
        now = datetime.datetime.utcnow()
        print(f"[{now}] 🔄 Heartbeat: Bot is alive. Latency: {round(self.bot.latency * 1000)}ms")

    @health_check.before_loop
    async def before_health_check(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Heartbeat(bot))