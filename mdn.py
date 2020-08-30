# coding: utf-8

##### 情報読み込み #####
# Pythonモジュール
import traceback # エラー表示のためにインポート

# Discordモジュール
import discord
from discord.ext import commands

# コグの名前を格納
INITIAL_EXTENSIONS = [
	'cogs.cog'
]

# 起動確認
print('===== もだねちゃん起動 =====')

client = discord.Client() # ユーザー

class MyBot(commands.Bot):

	# MyBotのコンストラタ
	def __init__(self, command_prefix):
		# superクラスのコンストラクタに値を渡して実行
		super().__init__(command_prefix)

		# INITIAL_COGSに格納されている名前からコグを読み込む
		# エラーが発生した場合はエラー内容を表示
		for cog in INITIAL_EXTENSIONS:
			try:
				self.load_extension(cog)
			except Exception:
				traceback.print_exc()


	# 起動時に動作する処理
	async def on_ready(self):
		# 起動したらターミナルにログイン通知が表示される
		print('===== ログインしました =====')
		print(self.user)
		print(self.user.name)
		print(self.user.id)

##### コマンド #####
## あいさつ
# @bot.command(name='mdn h')
# async def hello(ctx):
# 	await ctx.send(f'{ctx.message.author.mention}\nやっほー！もだねちゃんだよ！')


##### Botの起動とDiscordサーバーへの接続 #####
if __name__ == '__main__':
	bot = MyBot(command_prefix='!') #コマンド実行を示す「!」を指定
	TOKEN = 'NzMzODQ3NTg4MDQxNjU0MzYz.XxJJaA.BjEDKqzF3Yz0o-ZFm4fXWRdQLq4' # botのトークン
	bot.run(TOKEN)