import os

import discord
from discord.ext import commands
from pathlib import Path

root_path = Path(__file__).parents[0]

command_prefix = "!"

bot = commands.Bot(command_prefix=command_prefix, case_insensitive=True)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

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
    for file in os.listdir(root_path + "/bot_cogs"):
        if file.endswith(".py"):
            bot.load_extension(file)

    bot.run('NzcxMDAyMjkzMzk4OTI5NDA4.X5lx1w.wDiGh9zA96h6vsOLQ2iLCvKCgMQ')
