'''Cog Help'''

from discord.ext import commands
from .utils import send as sd

##### コグ #####
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=['h'], description='ヘルプを表示するよ')
    async def help(self, ctx):
        print('===== もだねちゃんヘルプを表示します =====')
        await sd.send_help(ctx)

async def setup(bot):
    await bot.add_cog(Help(bot))
