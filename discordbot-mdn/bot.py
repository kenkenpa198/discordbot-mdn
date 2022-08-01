from discord.ext import commands
import discord
import os
import platform
from datetime import datetime
import traceback
from cogs.utils import psql

print('===== もだねちゃんを起動します =====')
print('起動時刻：' + str(datetime.now()))
print('python ' + platform.python_version())
print('discord.py ' + discord.__version__)

bot = commands.Bot(command_prefix='!mdn ') # コマンド実行を示す「!mdn 」を指定
bot.remove_command('help') # デフォルトの help を削除


##### bot 起動時に動作する処理 #####
@bot.event
async def on_ready():
    # 起動したらターミナルへログイン通知を表示
    print('--- ログイン成功 ---')
    print('===== bot 起動時の処理を実行します =====')

    # アクティビティ表示を変更
    print('--- アクティビティ表示を変更 ---')
    client = bot
    act = discord.Game('「 !mdn h 」でヘルプを表示するよ！                          ') # Discord のメンバー欄で「〜をプレイ中」を表示させないため空白をいっぱい入れている
    await client.change_presence(status=None, activity=act)

    # 読み上げ機能：自動再接続処理
    print('--- 読み上げ機能：自動再接続処理を開始 ---')
    print('--- 読み上げ対象 DB を取得 ---')
    guild_id_list    = psql.run_query_to_list('cogs/sql/talk/select_guild_ids.sql')
    vc_id_list       = psql.run_query_to_list('cogs/sql/talk/select_vc_ids.sql')
    channel_id_list  = psql.run_query_to_list('cogs/sql/talk/select_channel_ids.sql')

    if guild_id_list:
        num = 0
        for guild_id, vc_id, channel_id in zip(guild_id_list, vc_id_list, channel_id_list):
            print('--- VC への接続を実行（'+ str(num) +'） ---')
            talk_guild = bot.get_guild(int(guild_id))
            talk_vc = talk_guild.get_channel(int(vc_id))
            talk_channel = talk_guild.get_channel(int(channel_id))
            await talk_vc.connect()
            print('--- VC へ接続完了 ---')

            embed = discord.Embed(title='ボイスチャンネルへ再入室しました',description='もだねちゃんが再起動したので、再接続処理を行いました。', color=0xffd6e9)
            try:
                await talk_channel.send(embed=embed)
            except AttributeError as e:
                print('--- メッセージを送信できませんでした ---')
                traceback.print_exc()
                print(e)
            num += 1
    else:
        print('--- 読み上げ対象 DB にレコードが無かったためスキップ ---')


    print('===== bot 起動時の処理を完了しました =====')
    print('===== Hello, World! =====')


##### イベント発生時に動作する処理 #####
@bot.event
async def on_command_error(ctx, error):
    print('--- エラー ---')
    print('on_command_error')
    print(traceback.format_exc())
    embed = discord.Embed(title='コマンドを受け付けられませんでした',description='なんらかの原因でコマンドを実行できなかったよ。ごめんね。\n以下のコマンドで使い方を確認してみてね！', color=0xffab6f)
    embed.add_field(name='ㅤ\n❓ ヘルプを表示する', value='もだねちゃんのコマンド一覧を表示できます。```!mdn h```', inline=False)
    embed.set_footer(text='ㅤ\n正しくコマンドを送信している場合でも、サーバー側の仕様によりこのメッセージが表示されることがあります。\n読み上げ終了時にこのメッセージが出てしまい、もだねちゃんを退出させることができない場合は以下の手順をお試しください。\n\n1. 「!mdn s」を送信し、読み上げ対象チャンネルを再設定する。\n2. 「!mdn e」を送信する。\n\n問題が解決されない場合、お手数ですが以下の手順でもだねちゃんを切断してあげてください。\n\n1. ボイスチャンネルのもだねちゃんを右クリックする。\n2.「切断」を選ぶ。')

    await ctx.send(embed=embed)


##### Cogの読み込み #####
bot.load_extension('cogs.talk')
bot.load_extension('cogs.janken')
bot.load_extension('cogs.help')
bot.load_extension('cogs.hello')
bot.load_extension('cogs.uranai')
bot.load_extension('cogs.petite')
bot.load_extension('cogs.reload')


##### 接続処理 #####
# 環境変数に格納したトークンを取得
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Botの起動とDiscordサーバーへの接続
print('===== Discord サーバーへ接続します =====')
bot.run(BOT_TOKEN)