# coding: utf-8
import discord
from discord.ext import commands
import asyncio
import re

abb_dict = {
    r'@もだねちゃん': '', # @もだねちゃん を削除
    r'@develop-chan': '', # @develop-chan を削除
    r'えらい(\?|？|)': '', # えらい？を削除
    r'って(知|し)ってる(\?|？|)': '', # って知ってる？を削除
}

# 置換用の関数を定義
def abb_msg(t):
    for abb_dict_key in abb_dict:
        t = re.sub(abb_dict_key, abb_dict[abb_dict_key], t)
    return t

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message): # メッセージが投稿された時のイベント
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return
        # もしmessage.mentionsにもだねちゃんが入っていなかったら
        if not self.bot.user in message.mentions:
            return
        if 'えらい' in message.clean_content:
            hello_msg = message.clean_content
            hello_msg_fmt = abb_msg(hello_msg)
            print(hello_msg_fmt)
            async with message.channel.typing():
                await asyncio.sleep(1)
            await message.channel.send(hello_msg_fmt + f'、えらーい！')
            return
        if 'って知ってる' in message.clean_content or 'ってしってる' in message.clean_content:
            hello_msg = message.clean_content
            hello_msg_fmt = abb_msg(hello_msg)
            print(hello_msg_fmt)
            async with message.channel.typing():
                await asyncio.sleep(1)
            await message.channel.send(hello_msg_fmt + f'ってなーに？')
            return
        async with message.channel.typing():
            await asyncio.sleep(1)
        await message.channel.send(f'{message.author.mention}\nやっほー！もだねちゃんだよ！')


def setup(bot):
    bot.add_cog(Hello(bot))

