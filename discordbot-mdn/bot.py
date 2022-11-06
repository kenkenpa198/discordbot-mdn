"""main bot program"""

import asyncio
from datetime import datetime
import logging
import os
import platform
import traceback

import discord
from discord.ext import commands

from cogs.utils import psql
from cogs.utils import send as sd

print('====================================')
print('           discordbot-mdn           ')
print('====================================')

print(str(datetime.now()))
print(f'python v{platform.python_version()}')
print(f'discord.py v{discord.__version__}')

# logging の設定
discord.utils.setup_logging(level=logging.INFO, root=False)

# intents の許可設定
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!mdn ', intents=intents)


@bot.event
async def on_ready():
    """bot がログイン時に実行する処理"""

    print('===== bot 起動後の処理を実行します =====')

    # ターミナルへログイン通知を表示
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

    # スラッシュコマンドの同期
    await bot.tree.sync()

    # アクティビティ表示を変更
    print('アクティビティ表示を変更')
    client = bot
    act = discord.Game('"/" でコマンド一覧を表示するよ！                          ') # Discord のメンバー欄で「〜をプレイ中」を表示させないため空白をいっぱい入れている
    await client.change_presence(status=None, activity=act)

    # 読み上げ機能: 自動再接続処理
    print('読み上げ機能: 自動再接続処理を開始')
    print('読み上げ対象チャンネルの情報を talk_channels テーブルから取得')
    guild_id_list    = psql.do_query_fetch_list('./sql/talk/select_guild_ids.sql')
    vc_id_list       = psql.do_query_fetch_list('./sql/talk/select_vc_ids.sql')
    channel_id_list  = psql.do_query_fetch_list('./sql/talk/select_channel_ids.sql')

    if guild_id_list:
        num = 0
        for guild_id, vc_id, channel_id in zip(guild_id_list, vc_id_list, channel_id_list):
            print('VC への接続を実行（'+ str(num) +'）')
            talk_guild = bot.get_guild(int(guild_id))
            talk_vc = talk_guild.get_channel(int(vc_id))
            talk_channel = talk_guild.get_channel(int(channel_id))
            await talk_vc.connect()
            print('VC へ接続完了')

            try:
                await sd.send_talk_reconnect(talk_channel)
            except AttributeError as e:
                print('メッセージを送信できませんでした')
                traceback.print_exc()
                print(e)
            num += 1
    else:
        print('読み上げ対象チャンネルが存在しなかったためスキップ')


    print('===== bot 起動時の処理を完了しました =====')
    print('===== Hello, World! =====')


##### イベント発生時に動作する処理 #####
@bot.event
async def on_command_error(ctx, error):
    """コマンドのエラー時に実行する処理"""

    print('コマンドの実行エラー')
    print(f'on_command_error: {error}')
    print(traceback.format_exc())

    await sd.send_on_command_error(ctx)


##### 接続処理 #####
# 環境変数に格納したトークンを取得
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Botの起動とDiscordサーバーへの接続
print('===== Discord サーバーへ接続します =====')

async def main():
    async with bot:

        # デフォルトの help を削除
        bot.remove_command('help')

        # Cogの読み込み
        await bot.load_extension('cogs.talk')
        await bot.load_extension('cogs.janken')
        await bot.load_extension('cogs.help')
        await bot.load_extension('cogs.hello')
        await bot.load_extension('cogs.uranai')
        await bot.load_extension('cogs.petite')
        await bot.load_extension('cogs.reload')

        # Bot を開始
        await bot.start(BOT_TOKEN)

asyncio.run(main())
