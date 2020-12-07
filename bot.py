import os
from datetime import datetime
import time
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


@tasks.loop(seconds=1.0)
async def reminder():
    global day
    global timings
    global prevday

    day = datetime.today().weekday()
    timing = f"{time.strftime('%H%M', time.gmtime(time.time() + 8*60*60))}"
    for x in timings:
        if timing == x["time"]:
            print("Reminder Alert")
            await bot.get_guild(x["guildid"]).system_channel.send(
                f"{x['time']}\n\n{x['subject']}"
            )
            print("Message Sent")
            timings.remove(x)
    if day != prevday:
        await refresh(day)
        prevday = day


@reminder.before_loop
async def reminder_pre():
    global prevday
    prevday = datetime.today().weekday()
    await refresh(prevday)
    await bot.wait_until_ready()
    print("Reminder setted up")


async def refresh(day):
    global timings
    timings = []
    for x in bot.guilds:
        times = Db(x.id)
        times = times.getAllEntry()
        for y in times:
            if day == y["day"]:
                y["guildid"] = x.id
                timings.append(y)


if __name__ == "__main__":
    cogs_path = "bot_cogs"
    for file in os.listdir(os.path.join(os.getcwd(), cogs_path)):
        if file.endswith(".py"):
            # get .py files in bot_cogs and load it
            # e.g load_extension("bot_cogs.timetable")
            bot.load_extension("{}.{}".format(cogs_path, file[:-3]))

    bot.run('NzcxMDAyMjkzMzk4OTI5NDA4.X5lx1w.wDiGh9zA96h6vsOLQ2iLCvKCgMQ')
    # bot.run("Nzc0ODg5NDI5MzkxMjQ1MzUy.X6eWBA.wGtzFFyVNFfvqMEhGAJaE7BNnGg")
