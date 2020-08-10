##モジュール読み込み

#Discord
import discord

# 基本モジュール
import datetime
import time
import pytz
import random

#utils.py
import utils

#変数nowを定義（現在の日時）
now = datetime.datetime.now()

#変数day_j time_jを定義（現在の日時を日本語表記にフォーマット化）
date_j = '{0:%m}'.format(now) + '月' + '{0:%d}'.format(now) + '日'
time_j = '{0:%H}'.format(now) + '時' + '{0:%M}'.format(now) + '分'

print('===== もだねちゃん起動 =====')

print('===== 動作確認 =====')
print(date_j)
print(time_j)
print('現在時刻：' + date_j + time_j)

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzMzODQ3NTg4MDQxNjU0MzYz.XxJJaA.BjEDKqzF3Yz0o-ZFm4fXWRdQLq4'

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
	# 起動したらターミナルにログイン通知が表示される
	print('===== ログインしました =====')

# ------------------------------------------

### 話しかけた人に返信する非同期関数を定義
## あいさつ
async def send_hello(message):
	reply = f'{message.author.mention}\nやっほー！もだねちゃんだよ！'
	await message.channel.send(reply)
	print(reply)

## 時間のお知らせ
async def send_datetime(message):

	#変数nowを定義（現在の日時）
	now = datetime.datetime.now()

	#変数day_j time_jを定義（現在の日時を日本語表記にフォーマット化）
	date_j = '{0:%m}'.format(now) + '月' + '{0:%d}'.format(now) + '日'
	time_j = '{0:%H}'.format(now) + '時' + '{0:%M}'.format(now) + '分'

	reply = f'{message.author.mention}\nはーい！\n今は' + date_j + time_j + 'だよ！'
	await message.channel.send(reply)
	print(reply)

## ジャンケン

# ジャンケンの説明文
janken_list = 'ジャンケン……\n\n▼出したい手を数字で入力してね\n:fist:：0　:v:：1　:hand_splayed:：2'

# 「さいしょはグー」を送信する関数
async def send_janken(message):
	reply = f'{message.author.mention}\nジャンケンだね！負けないよ！'
	await message.channel.send(reply)
	time.sleep(1)
	reply = f'{message.author.mention}\nじゃあいくよっ！\nさいしょはグー！' + janken_list
	await message.channel.send(reply)

# プレイヤーとコンピュータの手を算出する関数
async def send_janken_2(message):

	# アイコだった場合ジャンケンを繰り返す
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

		# アイコだったらメッセージを送信してもう一回
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

# ------------------------------------------

## 発言時に実行されるイベントハンドラを定義
@client.event
async def on_message(message):
	# メッセージ送信者がBotだった場合は無視する
	if message.author.bot:
		return
	# 話しかけられたかの判定
	# もしmessage.mentionsにもだねちゃんが入っていたら or message.contentに'!mdn'が入っていたら
	if client.user in message.mentions or '!mdn' in message.content:
		print(message.content)
		if '日時' in message.content or '日付' in message.content or '何日' in message.content or '何時' in message.content or '何分' in message.content or '!mdn t' in message.content:
			await send_datetime(message)
		elif 'じゃんけん' in message.content or 'ジャンケン' in message.content or '!mdn j' in message.content:
			await send_janken(message)
			await send_janken_2(message)
		else:
			await send_hello(message)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)