# coding: utf-8
from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['h'])
    async def help(self, ctx):
        await ctx.send('やっほー！もだねちゃんだよ！\n↓のコマンドを入力して指示してね！')
        embed = discord.Embed(color=0xff7777)
        embed.add_field(name='🎤 読み上げを開始する', value='```!mdn s```', inline=False)
        embed.add_field(name='ㅤ\n🎤 読み上げを終了する', value='```!mdn e```', inline=False)
        embed.add_field(name='ㅤ\n✌️ もだねちゃんとジャンケンをする', value='```!mdn j```', inline=False)
        embed.add_field(name='ㅤ\n❓ ヘルプ（コレ）を表示する', value='```!mdn h```', inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))