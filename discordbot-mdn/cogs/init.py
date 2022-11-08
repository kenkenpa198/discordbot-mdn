"""Cog Init"""

import logging

import discord
from discord.ext import commands

from cogs.utils import psql
from cogs.utils import send as sd

class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Bot がログイン時に実行する処理
        """
        # ターミナルへログイン通知を表示
        logging.info('Logged in as %s (ID: %s)', self.bot.user, self.bot.user.id)

        logging.info('Bot ログイン後の処理を実行')

        # アクティビティ表示を変更
        logging.info('アクティビティ表示を変更')
        act = discord.Game('"/" でコマンドを実行できるよ！                                        ') # Discord のメンバー欄で「〜をプレイ中」を表示させないため空白をいっぱい入れている
        await self.bot.change_presence(status=None, activity=act)

        # スラッシュコマンドの同期
        logging.info('スラッシュコマンドを同期')
        await self.bot.tree.sync()

        # 読み上げ機能: 自動再接続処理
        logging.info('読み上げ機能: 自動再接続処理を開始')
        logging.info('読み上げ対象チャンネルの情報を talk_channels テーブルから取得')
        guild_id_list    = psql.do_query_fetch_list('./sql/talk/select_guild_ids.sql')
        vc_id_list       = psql.do_query_fetch_list('./sql/talk/select_vc_ids.sql')
        channel_id_list  = psql.do_query_fetch_list('./sql/talk/select_channel_ids.sql')

        if guild_id_list:
            num = 0
            for guild_id, vc_id, channel_id in zip(guild_id_list, vc_id_list, channel_id_list):
                logging.info('VC への接続を実行: %s', str(num))

                talk_guild   = self.bot.get_guild(int(guild_id))
                talk_vc      = talk_guild.get_channel(int(vc_id))
                talk_channel = talk_guild.get_channel(int(channel_id))

                await talk_vc.connect()
                await sd.send_talk_reconnect(talk_channel)

                num += 1
        else:
            logging.info('読み上げ対象チャンネルが存在しなかったためスキップ')

        logging.info('Bot ログイン後の処理を完了')
        logging.info('Hello, World!')

async def setup(bot):
    await bot.add_cog(Init(bot))
