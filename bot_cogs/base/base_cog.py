import discord
from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("{} Cog has loaded in".format(self.__class__.__name__))