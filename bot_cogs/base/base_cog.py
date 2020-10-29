from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import bot

from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, _bot: type(bot)):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("{} Cog has loaded in".format(self.__class__.__name__))