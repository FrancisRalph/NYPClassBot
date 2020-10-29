import os
from datetime import datetime

import discord
from discord.ext import commands
from pathlib import Path

root_path = str(Path(__file__).parents[0])

command_prefix = "!"

bot = commands.Bot(command_prefix=command_prefix, case_insensitive=True)


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

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)


if __name__ == "__main__":
    cogs_path = "bot_cogs"
    for file in os.listdir("{}/{}".format(root_path, cogs_path)):
        if file.endswith(".py"):
            # get .py files in bot_cogs and load it
            # e.g load_extension("bot_cogs.timetable")
            bot.load_extension("{}.{}".format(cogs_path, file[:-3]))

    bot.run('NzcxMDAyMjkzMzk4OTI5NDA4.X5lx1w.wDiGh9zA96h6vsOLQ2iLCvKCgMQ')
