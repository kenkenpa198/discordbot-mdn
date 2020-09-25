# coding: utf-8
from discord.ext import commands
import discord
import config

print('===== もだねちゃん起動 =====')
print('discord.py ' + discord.__version__)

bot = commands.Bot(command_prefix='!mdn ') # コマンド実行を示す「!mdn 」を指定
# bot = commands.Bot(command_prefix='?mdn ') # 開発用

# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('===== ログインしました =====')

# Cogの読み込み
bot.load_extension('cogs.read')
bot.load_extension('cogs.janken')
bot.load_extension('cogs.help')
bot.load_extension('cogs.petite')
bot.load_extension('cogs.reload')

# Botの起動とDiscordサーバーへの接続
bot.run(config.TOKEN)