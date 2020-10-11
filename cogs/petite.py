# coding: utf-8
import discord
from discord.ext import commands
import asyncio


##### コグ #####
class Petite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # pingコマンド
    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        print('===== ping! =====')
        await ctx.send('pong!')
        print(ctx)
        print(ctx.author)
        print(ctx.author.mention)
        print(ctx.message.content)
        print(ctx.message.clean_content)
        if ctx.author.voice is None: # ボイスチャンネルにコマンド実行者がいるか判定
            print('--- VCにコマンド実行者がいません ---')
            return
        print(ctx.guild.voice_channels)
        print(ctx.guild.voice_client)
        print(ctx.guild.voice_client.channel)
        print(ctx.guild.voice_client.channel.members)
        print(ctx.guild.voice_client.channel.id)

    # whatコマンド
    @commands.command(aliases=['w'])
    async def what(self, ctx, what):
        print('===== whatってなーに？ =====')
        async with ctx.channel.typing():
            await asyncio.sleep(1)
        what_txt = f'{what}ってなーに？'
        await ctx.send(what_txt)
        print(what_txt)

    # 初期設定コマンド
    # @commands.command()
    # async def set(self, ctx):
    #     print('===== 初期設定を行います =====')
    #     guild = ctx.message.guild
    #     role = discord.utils.get(guild.roles, name='develop')
    #     print('変更対象：' + str(role))
    #     print('--- 役職の色を変更しました ---')
    #     await role.edit(colour=discord.Colour.from_rgb(250, 250, 250))
    #     await ctx.send(f'初期設定を行ったよ！これからよろしくねっ！')


def setup(bot):
    bot.add_cog(Petite(bot))