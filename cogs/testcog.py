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

	# メインとなるroleコマンド
	@commands.group()
	async def role(self, ctx):
		# サブコマンドが指定されていない場合、メッセージを送信する
		if ctx.invoked_subcommand is None:
			await ctx.send('このコマンドにはサブコマンドが必要だよ！')
	
	# roleコマンドのサブコマンド
	# 指定したユーザーに指定した役職を付与する
	@role.command()
	async def add(self, ctx, member: discord.Member, role: discord.Role):
		await member.add_roles(role)
		await ctx.send(f'{member}さんに役職「{role}」を付与したよ！')
	
	# roleコマンドのサブコマンド
	# 指定したユーザーから指定した役職を剥奪する
	@role.command()
	async def remove(self, ctx, member: discord.Member, role: discord.Role):
		await member.remove_roles(role)
		await ctx.send(f'{member}さんから役職「{role}」を解除したよ！')

	# あいさつ
	@commands.Cog.listener()
	async def on_message(self, message):
		# メッセージ送信者がBotだった場合は無視する
		print(message.content)		
		if message.author.bot:
			return
		if 'やっほー！' in message.mentions:
			await message.channel.send(f'{message.author.mention}\nやっほー！もだねちゃんだよ！')

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
	bot.add_cog(TestCog(bot)) #TestCogにBotを渡してインスタンス化し、Botにコグとして登録する