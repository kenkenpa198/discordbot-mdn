# coding: utf-8
from discord.ext import commands

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.command()
    async def r(self, ctx, module_name):
        await ctx.send(f" モジュール {module_name} の再読み込みを開始します")
        try:
            self.bot.reload_extension(module_name)
            await ctx.send(f" モジュール {module_name} の再読み込みを終了しました")
        except (commands.errors.ExtensionNotLoaded, commands.errors.ExtensionNotFound, commands.errors.NoEntryPointError, commands.errors.ExtensionFailed) as e:
            await ctx.send(f" モジュール {module_name} の再読み込みに失敗しました 理由:{e}")
            return

def setup(bot):
    bot.add_cog(Reload(bot))