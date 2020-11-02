import os
from datetime import datetime
import time
import discord
from discord.ext import commands
from codes import database
command_prefix = "!"

bot = commands.Bot(command_prefix=command_prefix, case_insensitive=True)

##Refresh reminders for the next day
def refresh(day, guilds):
    timings = []
    for x in guilds:
        times = Db(x.id).getAllEntry()
        for y in times:
            if day == y["day"]:
                y["guildid"] = x
                timings.append(y)
        

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    # track when bot started so that !uptime can be used
    # to check if bot has updated
    bot.start_time = datetime.utcnow()

    # Change bot activity to "!help"
    await bot.change_presence(
        activity=discord.Activity(
            name="{}help".format(command_prefix),
            type=discord.ActivityType.playing
        )
    )
    prevday = date.today().weekday()
    times = refresh(prevday, bot.guilds)
    try:
        while True:
            day = date.today().weekday()
            timing = f"{time.strftime("%H%M")}"
            for x in times:
                if timing == x["time"]:
                    await bot.get_guild(x["guildid"]).system_channel.send(f"{x["time"]}\n\n{x{"subject"}}")
            if(day != prevday):
                times = refresh(day, bot.guilds)
                prevday = day
            pass
    except KeyboardInterrupt:
        print("Exiting")
        quit()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)


if __name__ == "__main__":
    cogs_path = "bot_cogs"
    for file in os.listdir(os.path.join(os.getcwd(), cogs_path)):
        if file.endswith(".py"):
            # get .py files in bot_cogs and load it
            # e.g load_extension("bot_cogs.timetable")
            bot.load_extension("{}.{}".format(cogs_path, file[:-3]))

    bot.run('NzcxMDAyMjkzMzk4OTI5NDA4.X5lx1w.wDiGh9zA96h6vsOLQ2iLCvKCgMQ')
