"""Cog Petite"""

import asyncio
import logging
from discord.ext import commands


##### コグ #####
class Petite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        """
        ping コマンド
        """
        logging.info('ping コマンドを受付')
        await ctx.send('pong!')
        logging.info(ctx)
        logging.info(ctx.author)
        logging.info(ctx.author.mention)
        logging.info(ctx.message.content)
        logging.info(ctx.message.clean_content)
        if ctx.author.voice is None: # ボイスチャンネルにコマンド実行者がいるか判定
            logging.info('VCにコマンド実行者がいません')
            return
        logging.info(ctx.guild.voice_channels)
        logging.info(ctx.guild.voice_client)
        logging.info(ctx.guild.voice_client.channel)
        logging.info(ctx.guild.voice_client.channel.members)
        logging.info(ctx.guild.voice_client.channel.id)

    @commands.command(aliases=['w'])
    async def what(self, ctx, what):
        """
        what コマンド
        """
        logging.info('what コマンドを受付')
        async with ctx.channel.typing():
            await asyncio.sleep(1)
        what_txt = f'{what}ってなーに？'
        await ctx.send(what_txt)
        logging.info(what_txt)

    # TODO: もだねちゃんのユーザー名の色を設定したい
    # @commands.command()
    # async def set(self, ctx):
    #     logging.info('===== 初期設定を行います =====')
    #     guild = ctx.message.guild
    #     role = discord.utils.get(guild.roles, name='develop')
    #     logging.info('変更対象: ' + str(role))
    #     logging.info('役職の色を変更しました')
    #     await role.edit(colour=discord.Colour.from_rgb(250, 250, 250))
    #     await ctx.send(f'ロール「もだねちゃん」の色を変更しました。')

async def setup(bot):
    await bot.add_cog(Petite(bot))
