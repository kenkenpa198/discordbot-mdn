# インストールした discord.py を読み込む
import discord

# 日付を読み込む！
#from datetime import datetime, timedelta
import datetime
import time
import pytz

#ジャンケンモジュールの読み込み
import utils

#ランダムモジュールの読み込み
import random

#変数nowを定義（現在の日時）
now = datetime.datetime.now()

#変数day_j time_jを定義（現在の日時を日本語表記にフォーマット化）
date_j = '{0:%m}'.format(now) + '月' + '{0:%d}'.format(now) + '日'
time_j = '{0:%H}'.format(now) + '時' + '{0:%M}'.format(now) + '分'

now = datetime.datetime.now()
print('test_' + str(now))
print('今の日付は' + str(now) + 'だよ！')
print('今の日付は' + '{0:%m}'.format(now) + '月' + '{0:%d}'.format(now) + '日だよ！')
print('test_{0:%Y%m%d}'.format(now))
print('test_{0:%Y%m%d}{1:.3f}'.format(now,random.random()) + 'test_{0:%Y%m%d}'.format(now))

# tokyo = pytz.timezone('Asia/Tokyo')

# tokyo_datetime = tokyo.localize(datetime(2019, 7, 7, 14, 12, 34))

# print(tokyo_datetime)

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzMzODQ3NTg4MDQxNjU0MzYz.XxJJaA.BjEDKqzF3Yz0o-ZFm4fXWRdQLq4'

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
	# 起動したらターミナルにログイン通知が表示される
	print('ログインしました')

# メッセージ受信時に動作する処理
# @client.event
# async def on_message(message):
# 	# メッセージ送信者がBotだった場合は無視する
# 	if message.author.bot:
# 		return
	# 「/~~~」と発言したら指定したメッセージが返る処理
	# if message.content == '/もだねちゃん、こんにちは！':
		# await message.channel.send('こんにちはー！！')


# # 話しかけた人に返信する
# # 返信する非同期関数を定義
# async def reply(message):
# 	reply = f'{message.author.mention} やっほー！' # 返信メッセージの作成
# 	await message.channel.send(reply) # 返信メッセージを送信

# # 発言時に実行されるイベントハンドラを定義
# @client.event
# async def on_message(message):
# 	if client.user in message.mentions: #話しかけられたかの判定
# 		await reply(message) # 返信する非同期関数を実行


# ▼話しかけた人に返信する

# 返信する非同期関数を定義
# 基本の返信
async def hello(message):
	reply = f'{message.author.mention}\nやっほー！もだねちゃんだよ！'
	await message.channel.send(reply)
	print(reply)

	# 時間のお知らせ
async def datetime(message):
	reply = f'{message.author.mention}\nはーい！\n今は' + date_j + time_j + 'だよ！'
	await message.channel.send(reply)
	print(reply)

async def janken(message):
	reply = f'{message.author.mention}\nジャンケンだね！負けないよ！'
	await message.channel.send(reply)
	time.sleep(1)
	reply = f'{message.author.mention}\nじゃあいくよっ！\nさいしょはグー！ジャンケン……\n\n▼出したい手を数字で入力してね\n:fist:：0　:v:：1　:hand_splayed:：2'
	await message.channel.send(reply)

async def janken_2(message):

	#while文で使う変数を定義
	player_hand = 0
	computer_hand = 0
	while player_hand == computer_hand:

		def janken_check(m): #チェック関数を定義
			return m.content == '0' or m.content == '1' or m.content == '2' #数値が0,1,2のどれかだったらOK
		wait_message = await client.wait_for('message', check=janken_check) #メッセージを変数へ格納する

		player_hand = int(wait_message.content) #メッセージをint型へ変換し変数へ格納する
		# プレイヤーの手を出力
		print('プレイヤーの手：' + str(player_hand))

		if utils.validate(player_hand): #メッセージに格納されたテキストが0,1,2か判定する

			# コンピュータの手を算出
			computer_hand = random.randint(0, 2) # randintを用いて0から2までの数値を取得し、変数computer_handに代入
			# コンピュータの手を出力
			print('コンピュータの手：' + str(computer_hand))

			# 出した手の表示
			player_hand_result = utils.rise_hand(player_hand, 'あなた')
			computer_hand_result = utils.rise_hand(computer_hand, 'もだねちゃん')
			reply = f'{message.author.mention}\nぽんっ！\n\n' + player_hand_result + '\n\n' + computer_hand_result
			await message.channel.send(reply)

		else:
			reply = f'{message.author.mention}\nごめんね！\nジャンケンの手は記載の数字のみを入力してね！'
			await message.channel.send(reply)

		if player_hand == computer_hand:
			time.sleep(1.5)
			result = utils.judge_aiko(player_hand, computer_hand)
			reply = f'{message.author.mention}\n' + result
			await message.channel.send(reply)
		else:
			break
	# 結果の表示
	time.sleep(1.5)
	result = utils.judge(player_hand, computer_hand)
	reply = f'{message.author.mention}\n' + result + '\n\n楽しかったー！またやろうね！'
	await message.channel.send(reply)

# 発言時に実行されるイベントハンドラを定義
@client.event
async def on_message(message):
	# メッセージ送信者がBotだった場合は無視する
	if message.author.bot:
		return
# 話しかけられたかの判定
	if client.user in message.mentions: # もしmessage.mentionsにもだねが入っていたら
		print(message.content)
		if '日時' in message.content or '日付' in message.content or '何日' in message.content or '何時' in message.content or '何分' in message.content:
			await datetime(message)
		elif 'じゃんけん' in message.content or 'ジャンケン' in message.content:
			await janken(message)
			await janken_2(message)
		else:
			await hello(message)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)