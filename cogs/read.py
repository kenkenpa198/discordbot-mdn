# coding: utf-8
import discord
from discord.ext import commands
import asyncio

##### openjtalk関数 #####
# jtalk関数用のモジュールをインポート
import os
import subprocess
import re
from pydub import AudioSegment

# jtalk関数を定義
def jtalk(t, filepath='voice_message'):
    open_jtalk = ['open_jtalk']
    mech = ['-x','/usr/local/Cellar/open-jtalk/1.11/dic']
    htsvoice = ['-m','/usr/local/Cellar/open-jtalk/1.11/voice/mei/mei_happy.htsvoice']
    speed = ['-r','0.75']
    halftone = ['-fm','-2']
    weight = ['-jf','3']
    volume = ['-g', '-5']
    outwav = ['-ow', filepath+'.wav']
    cmd = open_jtalk + mech + htsvoice + speed + halftone + weight + volume + outwav
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(t.encode())
    c.stdin.close()
    c.wait()
    audio_segment = AudioSegment.from_wav(filepath+'.wav')
    os.remove(filepath+'.wav')
    audio_segment.export(filepath+'.mp3', format='mp3')
    return filepath+'.mp3'


##### テキスト置換関数 #####
# 辞書を作成
abb_dic = {}
# abb_dic[r'置換前のテキスト'] = '置換後のテキスト'
abb_dic[r'https?://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?'] = 'URL省略' # URLを置換する 正規表現サンプル r'https?://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?$' から変更
abb_dic[r'<:.{1,255}:\d{8,255}>'] = '' # カスタム絵文字を置換する
abb_dic[r'[w|ｗ]{2,255}'] = ' わらわら' # 「w」「ｗ」が2つ以上続いたら「わらわら」に置換する
abb_dic[r'[w|ｗ]'] = ' わら' # 「w」「ｗ」を「わら」に置換する
abb_dic[r'\d{9,255}'] = '数値省略' # 9桁以上の数値を置換する
print(abb_dic)

# 正規表現で読み上げテキストを置換する関数を定義
def abb_msg(t):
    for abb_dic_key in abb_dic:
        t = re.sub(abb_dic_key, abb_dic[abb_dic_key], t)
    return t


##### コグ #####
class Read(commands.Cog):

    # var_ctx: discord.ext.commands.Context = None

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['s'])
    async def start(self, ctx):
        print('===== 読み上げを開始します =====')

        # ボイスチャンネルにコマンド実行者がいるか判定
        if ctx.author.voice is None:
            print('--- VCにコマンド実行者がいないため待機します ---')
            embed = discord.Embed(title='読み上げの開始を待機します', description='読み上げを開始するには、10秒以内にボイスチャンネルへ入室してください', color=0xff7777)
            await ctx.send(embed=embed)

            # ボイスチャンネルにコマンド実行者がいるかチェックする関数を定義
            def vc_check(m, b, a):
                return ctx.author.voice is not None # bool(ctx.author.voice)でもOK

            # ボイスチャンネルにコマンド実行者がいれば変数へVCの情報を渡す
            try:
                await self.bot.wait_for('voice_state_update', check=vc_check, timeout=10)
            except asyncio.TimeoutError:
                embed = discord.Embed(title='読み上げの開始を中断しました', description='ボイスチャンネルへ接続できませんでした\n読み上げを開始するには、コマンド実行者がボイスチャンネルへ入室してください', color=0xff7777)
                await ctx.send(embed=embed)
                print('===== VCへの接続を中断しました =====')
                return
            else:
                await asyncio.sleep(1)
        else:
            pass


        vc = ctx.author.voice.channel
        # self.var_ctx = ctx
        print('接続：' + str(vc))
        # ボイスチャンネルへ接続する
        await vc.connect()
        embed = discord.Embed(title='読み上げを開始します', description='このボイスチャンネルに接続しました\n:microphone: ' + str(vc), color=0x44b582)
        await ctx.send(embed=embed)
        await asyncio.sleep(1)
        await ctx.send(f'やっほー！もだねちゃんだよ！')

    # 読み上げを終了する
    @commands.command(aliases=['e'])
    async def end(self, ctx):
        # ボイスチャンネルから退出する
        print('===== 読み上げを終了します =====')
        vc = ctx.voice_client.channel
        await ctx.voice_client.disconnect()
        embed = discord.Embed(title='読み上げを終了しました', description='ボイスチャンネルから退出しました', color=0xff7777)
        await ctx.send(embed=embed)
        print('退室：' + str(vc))

    # テキストチャンネルに投稿されたテキストを読み上げる
    @commands.Cog.listener()
    async def on_message(self, message): # メッセージが投稿された時のイベント
        if message.content == 'やっほー！もだねちゃんだよ！' or 'ってなーに？' in message.content:
            if message.guild.voice_client: # 読み上げ機能用
                spk_msg = message.clean_content
                print('整形前：' + spk_msg) # 置換前のテキストを出力
                spk_msg_fmt = abb_msg(spk_msg) # 置換後のテキストを変数へ格納
                print('整形後：' + spk_msg_fmt) # 置換後のテキストを出力
                jtalk(spk_msg_fmt) # jtalkの実行
                source = discord.FFmpegPCMAudio('voice_message.mp3') # mp3ファイルを指定
                message.guild.voice_client.play(source)
            else:
                return
        elif message.content.startswith('!') or message.content.startswith('?') or message.author.bot: # !が先頭に入っていたら無視
            return
        else:
            if message.guild.voice_client: # 読み上げ機能用
                spk_msg = message.clean_content
                print('整形前：' + spk_msg) # 置換前のテキストを出力
                spk_msg_fmt = abb_msg(spk_msg) # 置換後のテキストを変数へ格納
                print('整形後：' + spk_msg_fmt) # 置換後のテキストを出力
                jtalk(spk_msg_fmt) # jtalkの実行
                source = discord.FFmpegPCMAudio('voice_message.mp3') # mp3ファイルを指定
                message.guild.voice_client.play(source)
            else:
                return

    # 人がいなくなったら自動で退出する
    @commands.Cog.listener()
    async def on_voice_state_update(self,
                                    member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):
        if self.bot.voice_clients:
            print('--- VCステータスの変更を検知 ---')

            # VCへ誰かが入室したら（ユーザーの前と後のVCの状態を比較して、値が有る状態だったら）
            if not before.channel and after.channel:
                print('--- VCへ入室 ---')
                vcl = discord.utils.get(self.bot.voice_clients, channel=after.channel)
                print(vcl)
                print('VC人数：' + str(len(after.channel.members))) # VC人数を表示

            # VCから誰かが退出したら（ユーザーの前と後のVCの状態を比較して、値が無い状態だったら）
            elif before.channel and not after.channel:
                print('--- VCから退室 ---')
                vcl = discord.utils.get(self.bot.voice_clients, channel=after.channel)
                print(vcl)
                print('VC人数：' + str(len(before.channel.members))) # VC人数を表示

                # botが最後の一人になったら自動退出する
                bch = before.channel
                if len(bch.members) == 1 and bch.members[0] == self.bot.user:
                    vcl = discord.utils.get(self.bot.voice_clients, channel=before.channel)
                    if vcl and vcl.is_connected():
                        print('===== 読み上げを終了します =====')
                        await asyncio.sleep(1)
                        await vcl.disconnect()
                        # embed = discord.Embed(title='読み上げを終了しました', description='誰もいなくなったので、ボイスチャンネルから退出しました', color=0xff7777)
                        # await self.var_ctx.send(embed=embed)
                        print('退室：' + str(vcl))
        else:
            return


def setup(bot):
    bot.add_cog(Read(bot))