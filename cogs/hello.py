# coding: utf-8
import discord
from discord.ext import commands
import asyncio

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message): # メッセージが投稿された時のイベント
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return
        # もしmessage.mentionsにもだねちゃんが入っていたら
        if self.bot.user in message.mentions:
            async with message.channel.typing():
                await asyncio.sleep(1)
            await message.channel.send(f'{message.author.mention}\nやっほー！もだねちゃんだよ！')


def setup(bot):
    bot.add_cog(Hello(bot))