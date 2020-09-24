# coding: utf-8

##### 読み込み #####
# Pythonモジュール
import traceback # エラー表示のためにインポート

# Discordモジュール
import discord
from discord.ext import commands
print('discord.py ' + discord.__version__)

# 自作モジュール

# コグの名前を格納
INITIAL_EXTENSIONS = [
    'cog'
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


##### Botの起動とDiscordサーバーへの接続 #####
if __name__ == '__main__':
    bot = MyBot(command_prefix='!mdn ') #コマンド実行を示す「!」を指定
    TOKEN = 'NzU0NDExODkzNDAxMTkwNDEw.X10W0w._1PBisR0GF1bN6ETHIELGkU1EVY' # トークン

    # 開発
    # bot = MyBot(command_prefix='?mdn ') #コマンド実行を示す「?」を指定
    # TOKEN = 'NzU0NDE2NjU5NjIzNzA2ODQ1.X10bRA.0oWkYlYppLNwh9VUKstKvDG4fmM' # トークン
    bot.run(TOKEN)