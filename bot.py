import os
from datetime import datetime
import time
from pytz import timezone
import re

import discord
from discord.ext import commands, tasks

from modules.database import Db
from bot_cogs.timetable import create_entry_embed

command_prefix = "!"

bot = commands.Bot(command_prefix=command_prefix, case_insensitive=True)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

    # track when bot started so that !uptime can be used
    # to check if bot has updated
    bot.start_time = datetime.utcnow()

    # Change bot activity to "!help"
    await bot.change_presence(
        activity=discord.Activity(
            name="{}help".format(command_prefix), type=discord.ActivityType.playing
        )
    )
    reminder.start()


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)


timings = []
day = -1
prevday = -1
sgtime = datetime.fromtimestamp(time.time(), timezone("Asia/Singapore"))
timing = ""


@tasks.loop(seconds=1.0)
async def reminder():
    global day
    global timings
    global prevday
    global timing

    sgtime = datetime.fromtimestamp(time.time(), timezone("Asia/Singapore"))
    day = sgtime.weekday()
    timing = f"{sgtime.strftime('%H%M')}"

    for timing_dict in timings:
        entry = timing_dict["entry"]
        if timing == entry["time"]:
            await bot.get_guild(timing_dict["guildId"]).system_channel.send(
                embed=create_entry_embed(timing_dict["timetableName"], entry)
            )

            print("Message Sent")
            timings.remove(timing_dict)

    if day != prevday:
        await refresh(day)
        prevday = day


@reminder.before_loop
async def reminder_pre():
    global prevday
    global timing
    global sgtime
    prevday = sgtime.weekday()
    await refresh(prevday)
    await bot.wait_until_ready()
    print("Reminder setted up")


async def refresh(day):
    global timing
    global timings
    timings = []
    collection_names = Db.cluster.list_collection_names()
    for x in bot.guilds:
        guild_collection_names = []
        for name in collection_names:
            # extract guild id from collection name
            match = re.match("([^_]+)_.+", name)
            if match:
                collection_guild = match.group(1)
                # if collection guild id is the same as current guild id,
                # add to list so that timings get be retrieved
                if collection_guild == str(x.id):
                    guild_collection_names.append(name)
        for collection_name in guild_collection_names:
            timetable_db = Db(collection_name)
            times = timetable_db.getEntriesMergedBySubject()

            for entry in times:
                if day == entry["day"]:
                    timing_dict = {
                        "guildId": x.id,
                        "timetableName": collection_name,
                        "entry": entry,
                    }
                    timings.append(timing_dict)
    print(timings)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="!help",
        description="Shows available commands and their usage.",
        color=0x0080C0,
    )
    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/769097949514563597/789432709616238622/1536892103042-removebg-preview.png"
    )
    embed.add_field(
        name="!timetable add [name]",
        value="Registers timetable for server, maximum 3.",
        inline=False,
    )
    embed.add_field(
        name="!timetable remove [name]",
        value="Removes specified timetable from server.",
        inline=False,
    )
    embed.add_field(
        name="!timetable list",
        value="Shows all timetables associated with this server.",
        inline=False,
    )
    embed.add_field(
        name="!timetable view [name]",
        value="Shows all entries of specified timetable.",
        inline=False,
    )
    embed.add_field(
        name="!timetable link [name] [day] [entry number/name]",
        value="Allows you to add zoom links to subjects in a timetable.",
        inline=False,
    )
    await ctx.send(embed=embed)


if __name__ == "__main__":
    cogs_path = "bot_cogs"
    for file in os.listdir(os.path.join(os.getcwd(), cogs_path)):
        if file.endswith(".py"):
            # get .py files in bot_cogs and load it
            # e.g load_extension("bot_cogs.timetable")
            bot.load_extension("{}.{}".format(cogs_path, file[:-3]))

    # bot.run("NzcxMDAyMjkzMzk4OTI5NDA4.X5lx1w.wDiGh9zA96h6vsOLQ2iLCvKCgMQ")
    bot.run("Nzc0ODg5NDI5MzkxMjQ1MzUy.X6eWBA.wGtzFFyVNFfvqMEhGAJaE7BNnGg")
