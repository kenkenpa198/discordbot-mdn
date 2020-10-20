# coding: utf-8
from discord.ext import commands
import discord


##### コグ #####
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['h'])
    async def help(self, ctx):
        await ctx.send('もだねちゃんのコマンド一覧だよ！\n以下のコマンドを入力して指示してね！')
        embed = discord.Embed(title='読み上げコマンド', color=0xf1bedf)
        embed.add_field(name='🎤 読み上げを開始する', value='```!mdn s```', inline=False)
        embed.add_field(name='ㅤ\n🎤 読み上げ対象のテキストチャンネルを変更する', value='```!mdn c```', inline=False)
        embed.add_field(name='ㅤ\n🎤 読み上げを終了する', value='```!mdn e```', inline=False)
        embed.set_footer(text='ㅤ\nヒント：\n開始 / 変更 コマンドは、お好みのテキストチャンネルを読み上げ対象として設定することもできます。\n（コマンド例）!mdn s 雑談部屋')
        await ctx.send(embed=embed)

        embed = discord.Embed(title='その他', color=0xf1bedf)
        embed.add_field(name='✌️ もだねちゃんとジャンケンをする', value='```!mdn j```', inline=False)
        embed.add_field(name='ㅤ\n❓ ヘルプ（コレ）を表示する', value='```!mdn h```', inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))