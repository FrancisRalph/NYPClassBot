from typing import Union
import asyncio

import discord
from discord.ext import commands

from bot_cogs.base.base_cog import BaseCog


class TimeTable(BaseCog):
    @commands.command()
    async def upload_timetable(self, ctx: commands.Context):
        author: Union[discord.User, discord.Member] = ctx.author
        await author.send("Please upload an image of the timetable from the NYP website")
        await ctx.send("You have been prompted in your DMs")

        def check(msg: discord.Message):
            return len(msg.attachments) > 0

        try:
            received_msg: discord.Message = await self.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You did not send an image, the prompt has been cancelled.")
        else:
            await ctx.send("(WIP) You sent {} images.\n{}"
                           .format(len(received_msg.attachments), received_msg.attachments[0].url)
                           )


def setup(bot: commands.Bot):
    bot.add_cog(TimeTable(bot))
