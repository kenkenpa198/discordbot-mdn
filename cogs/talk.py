# coding: utf-8
import discord
from discord.ext import commands
import asyncio

##### チェック用関数 #####
# ボイスチャンネルにコマンド実行者がいるか判定
def vc_check(m, b, a):
    return m.voice is not None # bool(ctx.author.voice)でもOK

# botが発言中か判定
def playing_check(m):
    if m.guild.voice_client:
        return m.guild.voice_client.is_playing() is False

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
    volume = ['-g', '-5']
    outwav = ['-ow', filepath+'.wav']
    cmd = open_jtalk + mech + htsvoice + speed + halftone + volume + outwav
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(t.encode())
    c.stdin.close()
    c.wait()
    audio_segment = AudioSegment.from_wav(filepath+'.wav')
    os.remove(filepath+'.wav')
    audio_segment.export(filepath+'.mp3', format='mp3')
    return filepath+'.mp3'


##### 読み上げ対象のメッセージを置換 #####
# 置換用の辞書を作成
abb_dict = {
    r'\n': '', # 改行を削除する
    r'https?://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?': 'URL省略', # URLを省略する 正規表現サンプル r'https?://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?$' から変更
    r'<:.{1,}:\d{8,}>': ' ', # カスタム絵文字を「 」に置換する
    r'\,|、|\.|。|\!|！|\?|？|\:|：|\;|；|\+|＋|\=|＝|\*|＊|\-|\~|\_|_|\[|「|\]|」|・|…': ' ', # 記号を「 」に置換する
    r'(w|ｗ){2,}': ' わらわら', # 「w」「ｗ」が2つ以上続いたら「わらわら」に置換する
    r'w|ｗ': ' わら', # 「w」「ｗ」を「わら」に置換する
    r'\d{9,}': '数値省略' # 9桁以上の数値を省略する
}

# 置換用の関数を定義
def abb_msg(t):
    for abb_dict_key in abb_dict:
        t = re.sub(abb_dict_key, abb_dict[abb_dict_key], t)
    return t


##### コグ #####
class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.to_read = {} # 読み上げテキストチャンネルIDを格納する空の辞書（キーは Guild ID）を作成

    @commands.command(aliases=['s'])
    async def start(self, ctx):
        print('===== 読み上げを開始します =====')

        # ボイスチャンネルにコマンド実行者がいるか判定
        if ctx.author.voice is None:
            print('--- VCにコマンド実行者がいないため待機します ---')
            embed = discord.Embed(title='読み上げの開始を待機します', description='読み上げを開始するには、10秒以内にボイスチャンネルへ入室してください', color=0x8bda76)
            await ctx.send(embed=embed)

            # 10秒まで待機 ボイスチャンネルにコマンド実行者が入ったら変数へVCの情報を渡す
            try:
                await self.bot.wait_for('voice_state_update', check=vc_check, timeout=10)
            except asyncio.TimeoutError:
                embed = discord.Embed(title='読み上げの開始を中断しました', description='ボイスチャンネルへ接続できませんでした\n読み上げを開始するには、コマンド実行者がボイスチャンネルへ入室してください', color=0x8bda76)
                await ctx.send(embed=embed)
                print('===== VCへの接続を中断しました =====')
                return
            else:
                await asyncio.sleep(1)
        else:
            pass

        vc = ctx.author.voice.channel
        print('接続：' + str(vc))
        # ボイスチャンネルへ接続する
        await vc.connect()

        self.to_read[ctx.guild.id] = ctx.channel.id # 読み上げテキストチャンネル辞書へIDを登録
        print('読み上げtch：' + str(self.to_read))
        read_tch = discord.utils.get(ctx.guild.channels, id=self.to_read[ctx.guild.id])
        print(read_tch)

        embed = discord.Embed(title='読み上げを開始します',description='以下のチャンネルで実行します', color=0xf1bedf)
        embed.add_field(name='ㅤ\n:microphone: 入室', value=vc)
        embed.add_field(name='ㅤ\n:notepad_spiral: 読み上げ対象', value=read_tch)
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
        embed = discord.Embed(title='読み上げを終了しました', description='ボイスチャンネルから退出しました', color=0x8bda76)
        await ctx.send(embed=embed)
        print('退室：' + str(vc))
        del self.to_read[ctx.guild.id] # 読み上げテキストチャンネル辞書からギルドIDを削除
        print('読み上げtch：' + str(self.to_read))

    # テキストチャンネルに投稿されたテキストを読み上げる
    @commands.Cog.listener()
    async def on_message(self, message): # メッセージが投稿された時のイベント
        if message.content == 'やっほー！もだねちゃんだよ！' or 'ってなーに？' in message.content:
            if message.guild.voice_client:
                if not message.channel.id == self.to_read[message.guild.id]: # 読み上げテキストチャンネル辞書にIDが入っていなかったら無視
                    return
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
            if message.guild.voice_client:
                if not message.channel.id == self.to_read[message.guild.id]: # 読み上げテキストチャンネル辞書にIDが入っていなかったら無視
                    return
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
                # if not self.bot.user in after.channel.members:
                #     print('読み上げtch：')



                # botが最後の一人になったら自動退出する
                bch = before.channel
                if len(bch.members) == 1 and bch.members[0] == self.bot.user:
                    vcl = discord.utils.get(self.bot.voice_clients, channel=before.channel)
                    if vcl and vcl.is_connected():
                        print('===== 読み上げを終了します =====')
                        await asyncio.sleep(1)
                        await vcl.disconnect()
                        embed = discord.Embed(title='読み上げを終了しました', description='誰もいなくなったので、ボイスチャンネルから退出しました', color=0x8bda76)
                        send_tch = discord.utils.get(member.guild.channels, id=self.to_read[member.guild.id])
                        print(send_tch)
                        await send_tch.send(embed=embed)
                        print('退室：' + str(vcl))
                        del self.to_read[member.guild.id] # 読み上げテキストチャンネル辞書からギルドIDを削除
                        print('読み上げtch：' + str(self.to_read))
        else:
            return


def setup(bot):
    bot.add_cog(Talk(bot))