import asyncio
import re

import alkana
import discord
from discord.ext import commands

from .utils import msg


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message): # メッセージが投稿された時のイベント
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return
        
        # もしmessage.mentionsにもだねちゃんが入っていなかったら無視
        if not self.bot.user in message.mentions:
            return

        if 'やっほー' in message.content:
            msg_fmt = msg.make_msg('', '', 'えへへ、やっほー！')
            async with message.channel.typing():
                await asyncio.sleep(4)
            await message.channel.send(msg_fmt)
            return

        if '偉い' in message.content or 'えらい' in message.content:
            msg_fmt = msg.make_msg(message.clean_content, '', '、えらーい！')
            async with message.channel.typing():
                await asyncio.sleep(4)
            await message.channel.send(msg_fmt)
            return

        if 'って知ってる' in message.content or 'ってしってる' in message.content:
            msg_fmt = msg.make_msg(message.clean_content, '', 'ってなーに？')
            async with message.channel.typing():
                await asyncio.sleep(4)
            await message.channel.send(msg_fmt)
            return

        async with message.channel.typing():
            await asyncio.sleep(4)
        await message.channel.send(f'{message.author.mention}\nやっほー！もだねちゃんだよ！')


def setup(bot):
    bot.add_cog(Hello(bot))