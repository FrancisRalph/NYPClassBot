from typing import Union
import asyncio
import re
import time
import os

import discord
from discord.ext import commands

from bot_cogs.base.base_cog import BaseCog
from codes.timetableconverter import TimeTable as TimeTableConverter

valid_image_extensions = ("jpg", "jpeg", "png")


class TimeTable(BaseCog):
    @commands.group()
    @commands.guild_only()
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

        attachment = received_msg.attachments[0]
        await author.send("Processing the image...")

        try:
            attachment_path = os.path.join(os.getcwd(), "Images/{}.png".format(attachment.id))
            attachment_size = await attachment.save(attachment_path)
        except Exception as error:
            await author.send(
                "An unexpected error has occurred. Please try again. (error: {})"
                .format(error)
            )
            return

        await author.send("Image saved! Size: {}B".format(attachment_size))

        await author.send("Converting to data...")
        start_time = time.time()
        converter = TimeTableConverter(id=attachment.id)

        try:
            dataframe = await converter.readfile(attachment_path)
            save_duration = time.time() - start_time
        except Exception as error:
            await author.send("Unable to convert to data! Please try again. {}".format(error))
            return
        finally:
            os.remove(attachment_path)

        await author.send("Converted to data! Took {:.3f}s".format(save_duration))

    @timetable.command(usage="<name>", enabled=False)
    async def remove(self, ctx: commands.Context, name: str):
        pass

    @timetable.command(usage="<name>", enabled=False)
    async def list(self, ctx: commands.Context):
        pass


def setup(bot: commands.Bot):
    bot.add_cog(TimeTable(bot))
