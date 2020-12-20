# built-in modules
from typing import Union
import asyncio
import re
import os
from datetime import datetime, timedelta

# other modules
import discord
from discord.ext import commands, tasks
from bot_cogs.base.base_cog import BaseCog
from tabulate import tabulate
from dpymenus import Page, PaginatedMenu
import validators

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


def add_hours(time_str, hours):
    return datetime.strftime(
        datetime.strptime(time_str, "%H%M") + timedelta(hours=hours), "%H%M"
    )


def create_entry_embed(name, entry):
    subject_text = entry["subject"].replace("\n", " ")
    timetable_name = extract_name(name)

    end_entry = entry.get("endEntry")
    if end_entry is None:
        end_time = add_hours(entry["time"], 1)
    else:
        end_time = add_hours(end_entry["time"], 1)

    description = f"From `{entry['time']}` to  `{end_time}`"
    link = entry.get("link")
    if link:
        description += f"\n{link}"
    embed = discord.Embed(
        title=f"{timetable_name}: {subject_text}",
        color=0xFFC905,
        description=description
    )

    return embed


class TimeTable(BaseCog):
    days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

    @commands.group()
    # @commands.guild_only()
    async def timetable(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help("timetable")

    @timetable.command(usage="<name>")
    async def add(self, ctx: commands.Context, name: str):
        author: Union[discord.User, discord.Member] = ctx.author

        guild_id = ctx.guild.id
        guildcollections = [
                extract_name(x)
                for x in database.db.list_collection_names()
                if x.startswith(str(guild_id))
            ]
        
        if name in guildcollections:
            await ctx.send("Timetable with name already exists.")
            return
        if len(guildcollections) >= 3:
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

    def get_entries_by_day(self, collection_name: str):
        return [
            sorted(list(database.db[collection_name].find({"day": i})), key=lambda entry: entry["time"])
            for i in range(7)
        ]

    def create_menu(self, ctx: commands.Context, name: str):
        guild_id = ctx.guild.id
        guildcollections = [
            extract_name(x)
            for x in database.db.list_collection_names()
            if extract_id(x) == str(guild_id)
        ]
        if name not in guildcollections:
            return None
        else:
            menu = PaginatedMenu(ctx)
            all_pages = {}

            collection_name = f"{guild_id}_{name}"
            entries_by_day = self.get_entries_by_day(collection_name)

            for i in range(7):
                day_entries = entries_by_day[i]
                x = "\n".join(
                    [
                        f"{num + 1}) " +
                        (" ".join(list(map(str, list([entry[key] for key in entry if key != "link"])[2:]))))
                        .replace(
                            "\n", " "
                        )
                        for num, entry in enumerate(day_entries)
                    ]
                )
                if x == "" or None or type(x) != str:
                    break
                page_i = Page(title=f"Page {i + 1}", description=f"Slots for {TimeTable.days[i]}")
                page_i.add_field(name=TimeTable.days[i], value=x)

                all_pages[i] = page_i.as_safe_embed()

            menu.add_pages(list(all_pages.values()))
            menu.hide_cancel_button()
            menu.show_skip_buttons()
            menu.set_timeout(120)
            menu.allow_multisession()

            return menu

    @timetable.command(usage="<name>", enabled=True)
    async def view(self, ctx: commands.Context, name: str):
        print("hi", ctx, name,)
        menu = self.create_menu(ctx, name)
        if menu is None:
            await ctx.send("Timetable does not exist.")
        else:
            await menu.open()

    @timetable.command(usage="<name> <day> <entry number/name>", enabled=True)
    async def link(self, ctx: commands.Context, name: str, day: str, entry_input: str):
        day = day.lower()
        lower_days = list(map(lambda x: x.lower(), TimeTable.days))

        if lower_days.count(day) == 0:
            await ctx.send("Please enter a valid day.")
            return
        day_index = lower_days.index(day)

        guild_id = ctx.guild.id
        collection_names = database.db.list_collection_names()
        collection_name = f"{guild_id}_{name}"

        if collection_name not in collection_names:
            await ctx.send("Please enter a valid timetable name.")
            await self.list(ctx)
            return

        db = database.Db(collection_name)
        entries_by_day = self.get_entries_by_day(collection_name)

        valid_input = True
        try:
            entry_input = int(entry_input)
        except ValueError:
            merged_entry = db.getMergedSubjectEntryFromDay(day_index, entry_input.upper(), 0.1)
            if merged_entry is None:
                valid_input = False
        else:
            try:
                entry = entries_by_day[day_index][entry_input - 1]
            except IndexError:
                valid_input = False
            else:
                merged_entry = db.getMergedSubjectEntryFromDay(day_index, entry["subject"])

        if not valid_input:
            await ctx.send("Please enter a valid entry (subject name or number from view)")
            return

        author: Union[discord.User, discord.Member] = ctx.author


        if merged_entry.get("link"):
            await ctx.send(
                "A zoom link is already in place. Do you want to overwrite it? (Y/N)",
               embed=create_entry_embed(collection_name, merged_entry)
            )
            confirm_msg: discord.Message = await self.bot.wait_for(
                "message", check=lambda msg: msg.author == author, timeout=prompt_duration
            )
            if confirm_msg.content.lower() != "y":
                await ctx.send("Prompt cancelled.")
                return

        subject_text = merged_entry["subject"].replace("\n", " ")
        try:
            await author.send(f"You have {prompt_duration} seconds to send a zoom link for `{subject_text}`.")
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
            return

        if ctx.channel.type != discord.ChannelType.private:
            await ctx.send("You have been prompted in your DMs.")

        def check(msg: discord.Message):
            return (
                msg.author == author
                and msg.channel.type == discord.ChannelType.private
            )

        try:
            received_msg: discord.Message = await self.bot.wait_for(
                "message", check=lambda msg: check(msg) and validators.url(msg.content), timeout=prompt_duration
            )
        except asyncio.TimeoutError:
            await author.send(
                "You did not send a valid link on time, the prompt has been cancelled."
            )
            return

        link = received_msg.content

        db.updateEntry(
            merged_entry["subject"],
            merged_entry["day"],
            merged_entry["time"],
            "link",
            link
        )

        merged_entry["link"] = link
        await author.send("Entry has been updated!", embed=create_entry_embed(collection_name, merged_entry))


def setup(bot: commands.Bot):
    bot.add_cog(TimeTable(bot))
