from datetime import datetime

from discord.ext import commands

from bot_cogs.base.base_cog import BaseCog


class Info(BaseCog):
    @commands.command()
    async def uptime(self, ctx: commands.Context):
        time_since_start = datetime.utcnow() - self.bot.start_time
        await ctx.send("Uptime: {}".format(time_since_start))


def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
