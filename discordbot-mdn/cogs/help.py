'''Cog Help'''


import logging
from discord.ext import commands
from .utils import send as sd

# logging の設定


##### コグ #####
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=['h'], description='ヘルプを表示するよ')
    async def help(self, ctx):
        logging.info('ヘルプコマンドを受付')
        await sd.send_help(ctx)

async def setup(bot):
    await bot.add_cog(Help(bot))
