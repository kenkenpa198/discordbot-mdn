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

print('====================================')
print('           discordbot-mdn           ')
print('====================================')

print(str(datetime.now()))
print(f'python {platform.python_version()}')
print(f'discord.py {discord.__version__}')

# logging の設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s [ %(levelname)s ] %(message)s')

# intents の許可設定
intents = discord.Intents.default()
intents.message_content = True

# Bot インスタンスの作成
bot = commands.Bot(command_prefix='!mdn ', intents=intents)

# デフォルトの help を削除
bot.remove_command('help')

async def main():
    """
    discordbot-mdn を実行
    """
    async with bot:
        logging.info('Bot を起動')

        logging.info('Cog を読み込み')
        await bot.load_extension('cogs.hello')
        await bot.load_extension('cogs.help')
        await bot.load_extension('cogs.init')
        await bot.load_extension('cogs.janken')
        await bot.load_extension('cogs.reload')
        await bot.load_extension('cogs.small')
        await bot.load_extension('cogs.talk')
        await bot.load_extension('cogs.uranai')

        # 環境変数に格納したトークンを取得
        BOT_TOKEN = os.environ.get('BOT_TOKEN')

        logging.info('Bot のログインと接続を実行')
        await bot.start(BOT_TOKEN)

@bot.event
async def on_command_error(ctx, error):
    """
    コマンドのエラー時に実行する処理
    """
    logging.error('on command error: %s', error)
    logging.error(traceback.format_exc())

    await sd.send_on_command_error(ctx)

##### main() を呼び出し #####
asyncio.run(main())
