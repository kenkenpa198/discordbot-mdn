##### 読み込み #####

# coding: utf-8

# 基本モジュール
import datetime
import time
import pytz
import random

# Discord
import discord
from discord.ext import commands

# utils.py
import utils

##### 起動確認 #####
print('===== もだねちゃん起動 =====')
print('===== 動作確認 =====')

# 変数nowを定義（現在の日時）
now = datetime.datetime.now()

# 変数yymm_kpn hhmm_jpnを定義（現在の日時を日本語表記にフォーマット化）
yymm_jpn = '{0:%m}'.format(now) + '月' + '{0:%d}'.format(now) + '日'
hhmm_jpn = '{0:%H}'.format(now) + '時' + '{0:%M}'.format(now) + '分'

print(yymm_jpn)
print(hhmm_jpn)
print('現在時刻：' + yymm_jpn + hhmm_jpn)

# 接続に必要なオブジェクトを生成
client = discord.Client() # ユーザー
bot = commands.Bot(command_prefix='!') # プレフィックスの設定

@bot.group()
async def mdn(ctx):
	if ctx.invoked_subcommand is None:
		await ctx.send('aaa')

@mdn.command()
async def t(message):
	#変数nowを定義（現在の日時）
	now = datetime.datetime.now()

	#変数day_j hhmm_jpnを定義（現在の日時を日本語表記にフォーマット化）
	yymm_jpn = '{0:%m}'.format(now) + '月' + '{0:%d}'.format(now) + '日'
	hhmm_jpn = '{0:%H}'.format(now) + '時' + '{0:%M}'.format(now) + '分'

	reply = f'{message.author.mention}\nはーい！\n今は' + yymm_jpn + hhmm_jpn + 'だよ！'
	await message.channel.send(reply)
	print(reply)

# 起動時に動作する処理
@bot.event
async def on_ready():
	# 起動したらターミナルにログイン通知が表示される
	print('===== ログインしました =====')

##### コマンド入力時 or 話しかけられた時に実行されるイベントハンドラを定義 #####
## あいさつ
@bot.command(name='mdn')
async def send_hello(ctx):
	reply = f'{ctx.message.author.mention}\nやっほー！もだねちゃんだよ！'
	await ctx.channel.send(reply)
	print(reply)

## 時報
async def send_datetime(message):
	#変数nowを定義（現在の日時）
	now = datetime.datetime.now()

	#変数day_j hhmm_jpnを定義（現在の日時を日本語表記にフォーマット化）
	yymm_jpn = '{0:%m}'.format(now) + '月' + '{0:%d}'.format(now) + '日'
	hhmm_jpn = '{0:%H}'.format(now) + '時' + '{0:%M}'.format(now) + '分'

	reply = f'{message.author.mention}\nはーい！\n今は' + yymm_jpn + hhmm_jpn + 'だよ！'
	await message.channel.send(reply)
	print(reply)

## ジャンケン
# ジャンケンの説明文
janken_list = '▼出したい手を数字で入力してね\n:fist:：0　:v:：1　:hand_splayed:：2'

# 関数
async def send_janken(message):
	reply = f'{message.author.mention}\nジャンケンだね！負けないよ！'
	await message.channel.send(reply)
	time.sleep(1)
	reply = f'{message.author.mention}\nじゃあいくよっ！\nさいしょはグー！ジャンケン……\n\n' + janken_list
	await message.channel.send(reply)

	# while文で使う変数を定義
	player_hand = 0
	computer_hand = 0
	while player_hand == computer_hand:

		# 返答のチェック関数を定義
		def janken_check(m):
			return m.content == '0' or m.content == '1' or m.content == '2' #数値が0,1,2のどれかだったらOK
		wait_message = await client.wait_for('message', check=janken_check) #メッセージを変数へ格納する

		# プレイヤーの手を算出
		player_hand = int(wait_message.content) #返答をint型へ変換し変数へ格納する
		print('プレイヤーの手：' + str(player_hand)) # プレイヤーの手を出力

		# コンピュータの手を算出
		computer_hand = random.randint(0, 2) # randintを用いて0から2までの数値を取得し、変数computer_handに代入
		print('コンピュータの手：' + str(computer_hand)) # コンピュータの手を出力

		# 出した手の表示
		player_hand_result = utils.rise_hand(player_hand, 'あなた')
		computer_hand_result = utils.rise_hand(computer_hand, 'もだねちゃん')
		reply = f'{message.author.mention}\nぽんっ！\n\n' + player_hand_result + '\n\n' + computer_hand_result
		await message.channel.send(reply)

		# アイコだったらメッセージを送信してもう一回繰り返す
		if player_hand == computer_hand:
			time.sleep(1.5)
			result = utils.judge_aiko(player_hand, computer_hand)
			reply = f'{message.author.mention}\n' + result + '\n' + janken_list
			await message.channel.send(reply)
		else:
			break #勝敗が決まった場合whileを抜ける

	# 勝敗の結果を表示して終了
	time.sleep(1.5)
	result = utils.judge(player_hand, computer_hand)
	reply = f'{message.author.mention}\n' + result + '\n\n楽しかったー！またやろうね！'
	await message.channel.send(reply)


##### 発言時に実行されるイベントハンドラを定義 #####
@bot.event
async def on_message(message):
	# メッセージ送信者がBotだった場合は無視する
	if message.author.bot:
		return
	# 話しかけられたかの判定
	# もしmessage.mentionsにもだねちゃんが入っていたら or message.contentに'!mdn'が入っていたら
	if client.user in message.mentions:
		print(message.content)
		if '何日' in message.content or '何時' in message.content or '何分' in message.content:
			await send_datetime(message)
		elif 'じゃんけん' in message.content or 'ジャンケン' in message.content:
			await send_janken(message)
		else:
			await send_hello(message)
	await bot.process_commands(message)


##### Botの起動とDiscordサーバーへの接続 #####
bot.run(info.TOKEN)