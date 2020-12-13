import os
from datetime import datetime
import time
from pytz import timezone
import re

import discord
from discord.ext import commands, tasks

from modules.database import Db

command_prefix = "!"

bot = commands.Bot(command_prefix=command_prefix, case_insensitive=True)


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
    for x in timings:
        if timing == x["time"]:
            print("Reminder Alert")
            await bot.get_guild(x["guildid"]).system_channel.send(
                f"For {x['timetable']}\n\n{x['time']}\n\n{x['subject']}"
            )
            print("Message Sent")
            timings.remove(x)
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
            times = timetable_db.getAllEntry()
            for y in times:
                if day == y["day"]:
                    y["guildid"] = x.id
                    y["timetable"] = collection_name
                    timings.append(y)
    print(timings)


if __name__ == "__main__":
    cogs_path = "bot_cogs"
    for file in os.listdir(os.path.join(os.getcwd(), cogs_path)):
        if file.endswith(".py"):
            # get .py files in bot_cogs and load it
            # e.g load_extension("bot_cogs.timetable")
            bot.load_extension("{}.{}".format(cogs_path, file[:-3]))

    bot.run('NzcxMDAyMjkzMzk4OTI5NDA4.X5lx1w.wDiGh9zA96h6vsOLQ2iLCvKCgMQ')
    # bot.run("Nzc0ODg5NDI5MzkxMjQ1MzUy.X6eWBA.wGtzFFyVNFfvqMEhGAJaE7BNnGg")
