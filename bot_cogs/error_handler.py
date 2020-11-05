import discord
from discord.ext import commands

from bot_cogs.base.base_cog import BaseCog


class ErrorHandler(BaseCog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        # if command has its own error handler, don't do anything
        # to prevent overriding it
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("Command is disabled as it is work in progress.")
        else:
            raise error


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
