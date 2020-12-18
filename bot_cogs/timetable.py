# built-in modules
from typing import Union
import asyncio
import re
import os

# other modules
import discord
from discord.ext import commands, tasks
from bot_cogs.base.base_cog import BaseCog
from tabulate import tabulate
from dpymenus import Page, PaginatedMenu

# project modules
from modules import dataprocess, upscaler, timetableconverter, database

valid_image_extensions = ("jpg", "jpeg", "png")
max_image_size = 2e6  # in bytes (1MB)
prompt_duration = 30
localpath = os.getcwd()


def extract_name(x: str):
    match: re.Match = re.search("[^_]+_(.+)", x)
    if match is not None:
        return match.group(1)
    else:
        print(f"Error extracting timetable name from {x}")
        return None


def extract_id(x: str):
    match: re.Match = re.search("([^_]+)_.+", x)
    if match is not None:
        return match.group(1)
    else:
        print(f"Error extracting timetable guild id from {x}")
        return None


def asynchronise_func(foo):
    async def bar(*args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, foo, *args)

    return bar


class TimeTable(BaseCog):
    @commands.group()
    # @commands.guild_only()
    async def timetable(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help("timetable")

    @timetable.command(usage="<name>")
    async def add(self, ctx: commands.Context, name: str):
        author: Union[discord.User, discord.Member] = ctx.author

        guild_id = ctx.guild.id
        no_guildcollections = len(
            [
                extract_name(x)
                for x in database.db.list_collection_names()
                if x.startswith(str(guild_id))
            ]
        )
        if no_guildcollections >= 3:
            await ctx.send("Max number of timetables registered for this server.")
            return

        try:
            await author.send(
                "Please upload an image of the timetable from the NYP website."
            )
        except Exception as error:
            if isinstance(error, discord.Forbidden):
                await ctx.send(
                    "{} please turn on your DMs and try again.".format(author.mention)
                )
            else:
                await ctx.send(
                    "{} I was unable to send you a DM. Error: {}".format(
                        author.mention, error
                    )
                )
            # stop function from running since DM could not be sent
            return

        if ctx.channel.type != discord.ChannelType.private:
            await ctx.send("You have been prompted in your DMs.")

        def check(msg: discord.Message):
            return (
                msg.author == author
                and msg.channel.type == discord.ChannelType.private
                # check if user sent an attachment
                and len(msg.attachments) > 0
                # check if attachment is a valid image
                and re.search(".+[.](.+)", msg.attachments[0].filename).group(1)
                in valid_image_extensions
                # restrict attachment size to prevent long processing time
            )

        try:
            await author.send(f"You have {prompt_duration} seconds to send an image.")
            # received_msg variable is used instead of msg
            # due to the check function using msg as its parameter
            received_msg: discord.Message = await self.bot.wait_for(
                "message", check=check, timeout=prompt_duration
            )
        except asyncio.TimeoutError:
            await author.send(
                "You did not send an image on time, the prompt has been cancelled."
            )
            return

        image = received_msg.attachments[0]
        if image.size > max_image_size:
            await author.send(
                f"Image is too big. Please send an image with a size less than {max_image_size // 1e6}MB"
            )
            return

        collection_name = f"{ctx.guild.id}_{name}"
        # paths for input and output
        image_path = os.path.join(os.getcwd(), f"images/{collection_name}.png")
        excel_path = os.path.join(os.getcwd(), f"excel/{collection_name}.xlsx")

        await image.save(image_path)
        await author.send("File saved, upscaling now.")

        await asynchronise_func(upscaler.upscale)(image_path, collection_name)
        await author.send("Upscaling finished, converting to excel now.")

        # converting xlxs
        await asynchronise_func(timetableconverter.readfile)(image_path, excel_path)
        await author.send("File converted to excel, cleaning file.")

        # cleaning xlxs
        array_of_entries = (dataprocess.cleanData(excel_path, collection_name))[0]
        await author.send("File has been cleaned, adding to database.")

        # inserting to db
        db = await asynchronise_func(database.Db)(collection_name)
        await author.send("Database has been created.")

        await asynchronise_func(db.insertManyEntry)(array_of_entries)
        await author.send("Collection has been inserted.")

        try:
            os.remove(image_path)
            os.remove(excel_path)
        except Exception as e:
            print(e, e.__traceback__)

    @timetable.command(usage="<name>", enabled=True)
    async def remove(self, ctx: commands.Context, name: str):
        guild_id = ctx.guild.id
        guildcollections = [
            extract_name(x)
            for x in database.db.list_collection_names()
            if x.startswith(str(guild_id))
        ]
        if name not in guildcollections:
            await ctx.send("Timetable does not exist.")
        else:
            removal = database.db[f"{guild_id}_{name}"]
            removal.drop()
            await ctx.send(f"{name} has been removed")

    @timetable.command(usage="peepeepoopoo", enabled=True)
    async def list(self, ctx: commands.Context):
        guild_id = ctx.guild.id
        message = [
            x
            for x in database.db.list_collection_names()
            if extract_id(x) == str(guild_id)
        ]
        output = ""
        for x in range(len(message)):
            y = extract_name(message[x])
            output += f"{x+1}. {y}\n"
        embed = discord.Embed(title="List Of Timetables", color=0x0080FF)
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/770215748860772382/785844394972545094/mongodb-removebg-preview.png"
        )
        embed.add_field(name="!remove !add", value=output, inline=False)
        await ctx.send(embed=embed)

    @timetable.command(usage="BENIS", enabled=True)
    async def view(self, ctx: commands.Context, name: str):
        guild_id = ctx.guild.id
        guildcollections = [
            extract_name(x)
            for x in database.db.list_collection_names()
            if extract_id(x) == str(guild_id)
        ]
        if name not in guildcollections:
            await ctx.send("Timetable does not exist.")
        else:
            menu = PaginatedMenu(ctx)
            all_pages = {}
            days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
            for i in range(7):
                x = "\n".join(
                    [
                        (" ".join(list(map(str, list(i.values())[2:])))).replace(
                            "\n", " "
                        )
                        for i in list(
                            database.db[f"{guild_id}_{name}"].find({"day": i})
                        )
                    ]
                )
                if x == "" or None or type(x) != str:
                    break
                page_i = Page(title=f"Page {i+1}", description=f"Slots for {days[i]}")
                page_i.add_field(name=days[i], value=x)
                all_pages[i] = page_i

            menu.add_pages(list(all_pages.values()))
            menu.hide_cancel_button()
            menu.show_skip_buttons()
            # page3 = Page(title="Page 3", description="Third page test!")
            # page3.add_field(name="Example E", value="Example F")
            await menu.open()
            await ctx.send(menu)


def setup(bot: commands.Bot):
    bot.add_cog(TimeTable(bot))
