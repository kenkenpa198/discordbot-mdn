import discord
from discord.ext import commands # Bot Commands Frameworkのインポート

# コグとして用いるクラスを定義
class TestCog(commands.Cog):

	# TestCogクラスのコンストラクタ Botを受け取り、インスタンス変数として保持
	def __init__(self, bot):
		self.bot = bot
	
	# コマンドの作成 コマンドはcommandデコレータで必ず就職する
	@commands.command()
	async def ping(self, ctx):
		await ctx.send('pong!')
	
	@commands.command()
	async def what(self, ctx, what):
		await ctx.send(f'{what}ってなーに？')

	# メインとなるmdnコマンド
	@commands.group()
	async def mdn(self, ctx):
		# サブコマンドが指定されていない場合、メッセージを送信する
		if ctx.invoked_subcommand is None:
			help_s = 's：読み上げを開始する\n'
			help_e = 'e：読み上げを終了する\n'
			help_j = 'j：もだねちゃんとジャンケンをする'
			command_help = '▼コマンド一覧```' + help_s + help_e + help_j + '```'
			await ctx.send('やっほー！もだねちゃんだよ！\n\n私を操作できるコマンド一覧だよ！\n`!mdn <<コマンド名>>`と入力してご指示くださいっ！\n\n' + command_help)
	
	# mdnコマンドのサブコマンド
	# ボイスチャンネルへ入室させる
	@mdn.command()
	async def s(self, ctx):
		# ボイスチャンネルを取得する
		vc = ctx.author.voice.channel
		# ボイスチャンネルへ接続する
		await vc.connect()
		await ctx.send(f'> :microphone: {ctx.author.voice.channel}\nこのボイスチャンネルへ入室するよ！\nよろしくね！')
		
		# if文（できれば）
		# if ctx.author in discord.VoiceChannel:
		# 	await vc.connect()
		# 	await ctx.send(f'> :microphone: {ctx.author.voice.channel}\nこのボイスチャンネルへ入室するよ！\nよろしくね！')
		# else:
		# 	await ctx.send(f'ごめんね。入室先が見つからないんだ…。\n先にボイスチャンネルへ入室した上で私を呼んでね！')
	
	# mdnコマンドのサブコマンド
	# ボイスチャンネルから退出させる
	@mdn.command()
	async def e(self, ctx):
		# ボイスチャンネルから退出する
		await ctx.voice_client.disconnect()
		await ctx.send(f'ボイスチャンネルから退室したよ！\nまたね！')

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
	bot.add_cog(TestCog(bot)) #TestCogにBotを渡してインスタンス化し、Botにコグとして登録する