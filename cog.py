# coding: utf-8

##### 読み込み #####
# Pythonモジュール
import time
import random
import re

# 外部モジュール
import discord #discord.py
from discord.ext import commands # Bot Commands Frameworkのインポート

# 自作モジュール
import utils
import openjtalk

# botのオブジェクトを指定
client = discord.Client()

##### Cog #####
# コグとして用いるクラスを定義
class Cog(commands.Cog):

	# Cogクラスのコンストラクタ Botを受け取り、インスタンス変数として保持
	def __init__(self, bot):
		self.bot = bot
	
	# コマンドの作成 コマンドはcommandデコレータで必ず就職する
	@commands.command()
	async def ping(self, ctx):
		print('===== ping! =====')
		await ctx.send('pong!')
		print(ctx)
		print(ctx.author)
		print(ctx.author.mention)
		print(ctx.message.content)
		print(ctx.message.clean_content)
		print(ctx.guild.voice_channels)
		print(ctx.guild.voice_client)
		print(ctx.guild.voice_client.channel)
		print(ctx.guild.voice_client.channel.members)
		print(ctx.guild.voice_client.channel.id)
	
	@commands.command()
	async def what(self, ctx, what):
		print('===== whatってなーに？ =====')
		what_txt = f'{what}ってなーに？'
		await ctx.send(what_txt)
		print(what_txt)

	### メインとなるmdnコマンド
	@commands.group()
	async def mdn(self, ctx):
		# サブコマンドが指定されていない場合、メッセージを送信する
		if ctx.invoked_subcommand is None:
			help_s = 's：読み上げを開始する\n'
			help_e = 'e：読み上げを終了する\n'
			help_j = 'j：もだねちゃんとジャンケンをする'
			command_help = help_s + help_e + help_j
			await ctx.send('やっほー！もだねちゃんだよ！\n\n私を操作できるコマンドの一覧だよ！\n`!mdn <<コマンド>>`と入力してご指示くださいっ！\n\n')
			embed = discord.Embed(title='コマンドリスト', description=str(command_help), color=0xff7777)
			await ctx.send(embed=embed)
	
	## 読み上げ機能
	# 読み上げは「### テキストチャンネルに投稿されたテキストへ反応する > # 読み上げ機能用」を使用
	vc = 'ボイスチャンネル'

	# mdnサブコマンド：ボイスチャンネルへ入室させる
	@mdn.command()
	async def s(self, ctx):
		print('===== 読み上げを開始します =====')
		# ボイスチャンネルを取得する
		global vc
		vc = ctx.author.voice.channel
		# ボイスチャンネルへ接続する
		await ctx.send(f'{ctx.author.mention}\nはーい！読み上げを開始するねっ！')
		embed = discord.Embed(title='VCへ入室します', description=':microphone:' + str(vc), color=0xff7777)
		await ctx.send(embed=embed)
		time.sleep(1)
		await vc.connect()
		await ctx.send(f'やっほー！もだねちゃんだよ！')
		# global vc_mdn_members
		# vc_mdn_members = ctx.guild.voice_client.channel.members # もだねちゃんが入っているVCのメンバーリスト
		# print(str(vc_mdn_members))
		
		# if文（できれば）
		# if ctx.author in ((discord.VoiceChannel)):
		# 	await vc.connect()
		# 	await ctx.send(f'> :microphone: {ctx.author.voice.channel}\nこのボイスチャンネルへ入室するよ！\nよろしくね！')
		# else:
		# 	await ctx.send(f'ごめんね。入室先が見つからないんだ…。\n先にボイスチャンネルへ入室した上で私を呼んでね！')
	
	# mdnサブコマンド：ボイスチャンネルから退出させる
	@mdn.command()
	async def e(self, ctx):
		# ボイスチャンネルから退出する
		await ctx.send(f'読み上げを終了するよ！またね！')
		time.sleep(3.5)
		await ctx.voice_client.disconnect()
		embed = discord.Embed(title='VCから退出しました', description=':microphone:' + str(vc), color=0xff7777)
		await ctx.send(embed=embed)
		print('===== 読み上げを終了します =====')
	
	## ジャンケン機能
	# mdnサブコマンド：ジャンケンを実行する
	@mdn.command()
	async def j(self, ctx):
		print('===== ジャンケンを開始します =====')
		# ジャンケンの説明文
		janken_list = ':fist:：0　:v:：1　:hand_splayed:：2'

		# ジャンケンの実行
		await ctx.send(f'{ctx.author.mention}\nジャンケンだね！負けないよ！')
		time.sleep(1)
		await ctx.send(f'{ctx.author.mention}\nじゃあいくよっ！\nさいしょはグー！ジャンケン……')
		embed = discord.Embed(title='出したい手を数字で入力してね', description=str(janken_list), color=0xff7777)
		await ctx.send(embed=embed)

		# while文で使う変数と関数を定義
		# プレイヤーとコンピューターの手を入れる変数を定義
		player_hand = 0
		computer_hand = 0

		while player_hand == computer_hand:
			# プレイヤーが送信したメッセージをチェック用関数でチェックする	
			# 0, 1, 2 のどれかだったらOK それら意外であれば待機
			wait_message = await self.bot.wait_for('message', check=utils.janken_check) #メッセージを変数へ格納する

			# プレイヤーの手を算出
			player_hand = int(wait_message.content) #返答をint型へ変換し変数へ格納する
			print('プレイヤーの手：' + str(player_hand)) # プレイヤーの手を出力

			# コンピュータの手を算出
			computer_hand = random.randint(0, 2) # randintを用いて0から2までの数値を取得し、変数computer_handに代入
			print('コンピュータの手：' + str(computer_hand)) # コンピュータの手を出力

			# 出した手の表示
			await ctx.send(f'{ctx.author.mention}\nぽんっ！')
			embed = discord.Embed(color=0xff7777)
			embed.add_field(name=str(ctx.author.name) + 'さんが出した手', value=utils.rise_hand(player_hand), inline=False)
			embed.add_field(name='ㅤ\nもだねちゃんが出した手', value=utils.rise_hand(computer_hand), inline=False)
			await ctx.send(embed=embed)

			# アイコだったらメッセージを送信してもう一回
			if player_hand == computer_hand:
				time.sleep(1.5)
				result = utils.judge_aiko(player_hand, computer_hand)
				await ctx.send(f'{ctx.author.mention}\n' + result)
				embed = discord.Embed(title='出したい手を数字で入力してね', description=str(janken_list), color=0xff7777)
				await ctx.send(embed=embed)
			else:
				break #勝敗が決まった場合whileを抜ける

		# 勝敗の結果を表示して終了
		time.sleep(1.5)
		result = utils.judge(player_hand, computer_hand)
		await ctx.send(f'{ctx.author.mention}\n' + result + '\n\n楽しかった〜！またやろうね！')
		print('===== ジャンケンを終了します =====')

	### テキストチャンネルに投稿されたテキストへ反応する
	@commands.Cog.listener()
	async def on_message(self, message): # メッセージが投稿された時のイベント
		if message.content.startswith('!') or message.content.startswith('?'): # !が先頭に入っていたら無視
			return
		else:
			if message.guild.voice_client: # 読み上げ機能用
				spk_msg = message.clean_content
				print('整形前：' + spk_msg) #置換前のテキストを出力
				spk_msg_fmt = openjtalk.abb_msg(spk_msg) # 置換後のテキストを変数へ格納
				print('整形後：' + spk_msg_fmt) #置換後のテキストを出力
				openjtalk.jtalk(spk_msg_fmt) # jtalkの実行
				source = discord.FFmpegPCMAudio('voice_message.mp3') #wavファイルを出力
				message.guild.voice_client.play(source)
			else:
				return
	
	@commands.Cog.listener()
	async def on_voice_state_update(self,
                                    member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):

		print('--- VCへの入退室を検知 ---')
		# print(member)
		# print(before)
		# print(after)
		# if not before.channel and after.channel:
		# 	print('join to VC')
		# 	vcl = discord.utils.get(self.bot.voice_clients, channel=after.channel)
		# 	print(vcl)
		# elif before.channel and not after.channel:
		# 	print('out of VC')
		# 	vcl = discord.utils.get(self.bot.voice_clients, channel=before.channel)
		# 	print(vcl)
		# 	if vcl and vcl.is_connected():
		# 		await vcl.disconnect()

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
	bot.add_cog(Cog(bot)) #TestCogにBotを渡してインスタンス化し、Botにコグとして登録する