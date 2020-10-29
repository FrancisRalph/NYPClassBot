from typing import Union
import asyncio
import re

import discord
from discord.ext import commands

from bot_cogs.base.base_cog import BaseCog

valid_image_extensions = ("jpg", "jpeg", "png")


class TimeTable(BaseCog):
    @commands.group()
    async def timetable(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help("timetable")

    @timetable.command(usage="<name>")
    async def add(self, ctx: commands.Context, name: str):
        author: Union[discord.User, discord.Member] = ctx.author

        try:
            await author.send("Please upload an image of the timetable from the NYP website.")
        except Exception as error:
            if isinstance(error, discord.Forbidden):
                await ctx.send(
                    "{} please turn on your DMs and try again."
                    .format(author.mention)
                )
            else:
                await ctx.send(
                    "{} I was unable to send you a DM. Error: {}"
                    .format(author.mention, error)
                )
            # stop function from running since DM could not be sent
            return
        else:
            if ctx.channel.type != discord.ChannelType.private:
                await ctx.send("You have been prompted in your DMs.")

        def check(msg: discord.Message):
            return (
                msg.author == author
                and msg.channel.type == discord.ChannelType.private
                and len(msg.attachments) > 0
                and re.search(".+[.](.+)", msg.attachments[0].filename).group(1) in valid_image_extensions
            )

        try:
            received_msg: discord.Message = await self.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await author.send("You did not send an image on time, the prompt has been cancelled.")
            return
        else:
            attachment = received_msg.attachments[0]
            await author.send(
                "(WIP) You sent {} image(s).\n{}"
                .format(len(received_msg.attachments), attachment.url)
            )

    @timetable.command(usage="<name>", enabled=False)
    async def remove(self, ctx: commands.Context, name: str):
        pass

    @timetable.command(usage="<name>", enabled=False)
    async def list(self, ctx: commands.Context):
        pass


def setup(bot: commands.Bot):
    bot.add_cog(TimeTable(bot))
