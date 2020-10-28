from typing import Union
import asyncio

import discord
from discord.ext import commands

from bot_cogs.base.base_cog import BaseCog


class TimeTable(BaseCog):
    @commands.command()
    async def upload_timetable(self, ctx: commands.Context):
        author: Union[discord.User, discord.Member] = ctx.author

        try:
            await author.send("Please upload an image of the timetable from the NYP website")
        except Exception as e:
            if type(e) == discord.Forbidden:
                await ctx.send(
                    "{} please turn on your DMs and try again."
                        .format(author.mention)
                )
            else:
                await ctx.send(
                    "{} I was unable to send you a DM. Error: {}"
                    .format(author.mention, e)
                )
            # stop function from running since DM could not be sent
            return
        else:
            await ctx.send("You have been prompted in your DMs.")

        def check(msg: discord.Message):
            return (
                msg.author == author
                and msg.channel.type == discord.ChannelType.private
                and len(msg.attachments) > 0
            )

        try:
            received_msg: discord.Message = await self.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You did not send an image on time, the prompt has been cancelled.")
            return
        else:
            await author.send(
                "(WIP) You sent {} images.\n{}"
                .format(len(received_msg.attachments), received_msg.attachments[0].url)
            )


def setup(bot: commands.Bot):
    bot.add_cog(TimeTable(bot))
