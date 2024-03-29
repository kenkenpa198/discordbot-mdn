"""Cog Help"""

import logging
from discord.ext import commands
from .utils import send as sd

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        description='❓ ヘルプを表示するよ',
        aliases=['h']
    )
    async def help(self, ctx):
        """
        ヘルプコマンド
        """
        logging.info('ヘルプコマンドを受付')
        await sd.send_help(ctx)

async def setup(bot):
    await bot.add_cog(Help(bot))
