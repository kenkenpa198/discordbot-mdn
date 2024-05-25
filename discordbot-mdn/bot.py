"""Main bot program"""

import asyncio
from datetime import datetime
import logging
import os
import platform
import traceback

import discord
from discord.ext import commands

from cogs.utils import send as sd

def setup_logging():
    """ログ設定を行う関数"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [ %(levelname)s ] %(message)s')

def print_startup_info():
    """起動情報を表示する関数"""
    print('====================================')
    print('           discordbot-mdn           ')
    print('====================================')
    print(str(datetime.now()))
    print(f'python {platform.python_version()}')
    print(f'discord.py {discord.__version__}')

def get_bot_token():
    """
    環境変数から Bot のトークンを取得する関数

    Returns:
        str: Bot のトークン
    Raises:
        ValueError: BOT_TOKEN 環境変数が設定されていない場合
    """
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN 環境変数が設定されていません")
        raise ValueError("BOT_TOKEN 環境変数が設定されていません")
    return BOT_TOKEN

def create_bot():
    """
    Bot インスタンスを作成する関数

    Returns:
        discord.ext.commands.Bot: Bot のインスタンス
    """
    intents = discord.Intents.default()
    intents.message_content = True
    # Bot インスタンスの作成
    bot = commands.Bot(command_prefix='!mdn ', intents=intents)
    # デフォルトの help を削除
    bot.remove_command('help')

    return bot

async def load_cogs(bot):
    """
    cogs をロードする関数

    Args:
        bot (discord.ext.commands.Bot): コグをロードする Bot のインスタンス
    """
    cog_names = [
        'hello',
        'help',
        'init',
        'janken',
        'reload',
        'small',
        'talk',
        'uranai'
    ]
    for cog in cog_names:
        await bot.load_extension(f'cogs.{cog}')
        logging.info(f'cogs.{cog} をロードしました')

async def main():
    """
    Bot のメインエントリポイント
    """
    # ログ設定を実行
    setup_logging()

    # 起動情報を表示
    print_startup_info()

    # Bot インスタンスを作製
    bot = create_bot()

    # Bot のトークンを取得
    BOT_TOKEN = get_bot_token()

    # Bot を起動する
    async with bot:
        logging.info('Bot を起動')

        logging.info('cogs をロード')
        await load_cogs(bot)
        logging.info('Bot のログインと接続を実行')
        await bot.start(BOT_TOKEN)

    @bot.event
    async def on_command_error(ctx, error):
        """
        コマンド実行中に発生したエラーを処理する関数

        Args:
            ctx (discord.ext.commands.Context): エラーが発生したコンテキスト
            error (Exception): 発生したエラー
        """
        logging.error('on command error: %s', error)
        logging.error(traceback.format_exc())

        await sd.send_on_command_error(ctx)

# main() を呼び出し
asyncio.run(main())
