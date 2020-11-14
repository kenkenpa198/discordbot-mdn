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
def jtalk(t, filepath='voice'):
    open_jtalk = ['open_jtalk']
    mech = ['-x','/usr/local/Cellar/open-jtalk/1.11/dic']
    htsvoice = ['-m','/usr/local/Cellar/open-jtalk/1.11/voice/mei/mei_happy.htsvoice']
    speed = ['-r','0.7']
    halftone = ['-fm','-3']
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
    r'\n': ' ',                                                                                 # 改行を「 」に置換する
    r'https?://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?': 'URL省略',                                   # URLを省略する 正規表現サンプル r'https?://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?$' から変更
    r'<:.{1,}:\d{8,}>': ' ',                                                                    # カスタム絵文字を「 」に置換する
    r'\,|、|\.|。|\!|！|\?|？|\:|：|\;|；|\+|＋|\=|＝|\*|＊|\-|\~|\_|_|\[|「|\]|」|・|…': ' ', # 記号を「 」に置換する
    r'\d{9,}': '数値省略',                                                                      # 9桁以上の数値を省略する
    r'(D|d)iscord': 'ディスコード',                                                             # 辞書変換
    r'64': 'ロクヨン',                                                                          # 辞書変換
    r'(G|g)(C|c)コン': 'ジーシーコン',                                                          # 辞書変換
    r'(G|g)(C|c)': 'ゲームキューブ',                                                            # 辞書変換
    r'(W|w)ii': 'ウィー',                                                                       # 辞書変換
    r'(S|s)witch': 'スイッチ',                                                                  # 辞書変換
    r'(G|g)(B|b)(A|a)': 'アドバンス',                                                           # 辞書変換
    r'(G|g)(B|b)': 'ゲームボーイ',                                                              # 辞書変換
    r'3(D|d)(S|s)': 'スリーディーエス',                                                         # 辞書変換
    r'(D|d)(S|s)': 'ディーエス',                                                                # 辞書変換
    r'(S|s)platoon': 'スプラトゥーン',                                                          # 辞書変換
    r'(D|d)(X|x)': 'デラックス',                                                                # 辞書変換
    r'(S|s)(P|p)': 'スペシャル',                                                                # 辞書変換
    r'(D|d)(B|b)(D|d)': 'デッドバイデイライト',                                                 # 辞書変換
    r'(T|t)witter': 'ツイッター',                                                               # 辞書変換
    r'(S|s)hovel': 'シャベル',                                                                  # 辞書変換
    r'(ノシ|ﾉｼ)': 'バイバイ',                                                                   # 辞書変換
    r'(w|ｗ){2,}': ' わらぁわらぁ',                                                             # 辞書変換 「w」「ｗ」が2つ以上続いたら「わらわら」に置換する
    r'w|ｗ': ' わらぁ',                                                                         # 辞書変換 「w」「ｗ」を「わら」に置換する
    r'〜|～': 'ー',                                                                             # 辞書変換 「〜：波ダッシュ（Mac」「～：全角チルダ（Win」を「ー」に置換する
    r'^\s': ''                                                                                  # 文頭の空白を削除する
}

# 置換用の関数を定義
def abb_msg(t):
    for abb_dict_key in abb_dict:
        t = re.sub(abb_dict_key, abb_dict[abb_dict_key], t)
    # 40文字を超えたら省略する
    if len(t) > 40:
        t = t[:40]
        t += ' 以下略'
    return t


##### コグ #####
class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.talk_tc_dict = {} # 読み上げ対象テキストチャンネルのIDを格納する空の辞書（キーは Guild ID）を作成


    # 読み上げを開始する
    @commands.command(aliases=['s'])
    async def start(self, ctx, tch: discord.TextChannel=None):
        print('===== 読み上げを開始します =====')

        # botが既にボイスチャンネルへ入室していないか判定
        if ctx.guild.voice_client:
            print('--- エラーコード：002 ---')
            embed = discord.Embed(title='コマンドを受け付けられませんでした',description='私はもう入室済みだよ…！\n以下のコマンドを実行して、使い方を確認してみてね！', color=0xeaa55c)
            embed.add_field(name='ㅤ\n❓ ヘルプを表示する', value='```!mdn h```', inline=False)
            await ctx.send(embed=embed)
            return

        # ボイスチャンネルにコマンド実行者がいるか判定
        if not ctx.author.voice:
            print('--- VCにコマンド実行者がいないため待機します ---')
            embed = discord.Embed(title='読み上げの実施を待機するよ', description='読み上げを開始するには、10秒以内にボイスチャンネルへ入室してね。', color=0xe3e5e8)
            await ctx.send(embed=embed)

            # 10秒まで待機
            # ボイスチャンネルにコマンド実行者が入ったら変数へVCの情報を渡す
            try:
                await self.bot.wait_for('voice_state_update', check=vc_check, timeout=10)
            except asyncio.TimeoutError:
                embed = discord.Embed(title='読み上げの実施を中断したよ', description='読み上げを開始するには、コマンド実行者がボイスチャンネルへ入室してね。', color=0xeaa55c)
                await ctx.send(embed=embed)
                print('===== VCへの接続を中断しました =====')
                return
            else:
                print('--- VCにコマンド実行者が入室しました ---')
                print('--- 処理を再開します ---')
                await asyncio.sleep(.5)

        # 入室するボイスチャンネルを変数へ格納
        vc = ctx.author.voice.channel

        # 読み上げ対象のテキストチャンネルを設定
        if tch: # 引数がある場合は指定のテキストチャンネルを読み上げ
            print(tch)
            talk_tc = discord.utils.get(ctx.guild.text_channels, name=tch.name)
            print(talk_tc)
            self.talk_tc_dict[ctx.guild.id] = talk_tc.id # talk_tc_dictへIDを登録
            print('読み上げ対象：' + str(self.talk_tc_dict))
            send_hello = False

        else: # 引数がない場合はコマンドを実行したテキストチャンネルを読み上げ
            self.talk_tc_dict[ctx.guild.id] = ctx.channel.id # talk_tc_dictへIDを登録
            print('読み上げ対象：' + str(self.talk_tc_dict))
            talk_tc = discord.utils.get(ctx.guild.text_channels, id=self.talk_tc_dict[ctx.guild.id])
            print(talk_tc)
            send_hello = True

        embed = discord.Embed(title='読み上げを開始するよ',description='以下の内容でおしゃべりを始めるね！', color=0xf1bedf)
        embed.add_field(name='ㅤ\n🎤 入室ボイスチャンネル', value=vc)
        embed.add_field(name='ㅤ\n📗 読み上げ対象', value='<#' + str(self.talk_tc_dict[ctx.guild.id]) + '>')
        embed.set_footer(text='ㅤ\nヒント：\n読み上げ対象を変更したい時は、「 !mdn c 」コマンドを使用してください。')
        await ctx.send(embed=embed)
        await asyncio.sleep(1)

        # ボイスチャンネルへ接続する
        await vc.connect()
        print('接続：' + str(vc))
        await asyncio.sleep(.5)
        if send_hello:
            await ctx.send(f'やっほー！もだねちゃんだよ！')


    # 読み上げ対象のテキストチャンネルを変更する
    @commands.command(aliases=['c'])
    async def change(self, ctx, tch: discord.TextChannel=None):
        print ('===== 読み上げ対象のテキストチャンネルを変更します =====')

        # botがボイスチャンネルにいるか判定
        if not ctx.guild.voice_client:
            print('--- エラーコード：002 ---')
            embed = discord.Embed(title='コマンドを受け付けられませんでした',description='そのコマンドは、私がボイスチャンネルへ入室している時のみ使用できるよ。\n以下のコマンドを先に実行してね。', color=0xeaa55c)
            embed.add_field(name='ㅤ\n🎤 読み上げを開始する', value='```!mdn s```', inline=False)
            await ctx.send(embed=embed)
            return

        # 読み上げ対象のテキストチャンネルを設定
        if tch: # 引数がある場合は指定のテキストチャンネルを読み上げ
            print(tch)
            talk_tc = discord.utils.get(ctx.guild.text_channels, name=tch.name)
            print(talk_tc)
            self.talk_tc_dict[ctx.guild.id] = talk_tc.id # talk_tc_dictへIDを登録
            print('読み上げ対象：' + str(self.talk_tc_dict))

        else: # 引数がない場合はコマンドを実行したテキストチャンネルを読み上げ
            self.talk_tc_dict[ctx.guild.id] = ctx.channel.id # talk_tc_dictへIDを登録
            print('読み上げ対象：' + str(self.talk_tc_dict))
            talk_tc = discord.utils.get(ctx.guild.text_channels, id=self.talk_tc_dict[ctx.guild.id])
            print(talk_tc)
    
        embed = discord.Embed(title='読み上げ対象を変更したよ',description='以下のテキストチャンネルを読み上げ対象に再設定したよ。', color=0xf1bedf)
        embed.add_field(name='ㅤ\n:green_book: 読み上げ対象', value='<#' + str(self.talk_tc_dict[ctx.guild.id]) + '>')
        await ctx.send(embed=embed)


    # 読み上げを終了する
    @commands.command(aliases=['e'])
    async def end(self, ctx):
        print('===== 読み上げを終了します：コマンド受付 =====')

        # botがボイスチャンネルにいるか判定
        if not ctx.guild.voice_client:
            print('--- エラーコード：002 ---')
            embed = discord.Embed(title='コマンドを受け付けられませんでした',description='そのコマンドは、私がボイスチャンネルへ入室している時のみ使用できるよ。\n以下のコマンドを先に実行してね。', color=0xeaa55c)
            embed.add_field(name='ㅤ\n🎤 読み上げを開始する', value='```!mdn s```', inline=False)
            await ctx.send(embed=embed)
            return

        # ボイスチャンネルから退出する
        vc = ctx.voice_client.channel
        await ctx.voice_client.disconnect()
        embed = discord.Embed(title='読み上げを終了したよ', description='ボイスチャンネルから退出して読み上げを終了しました。またね！', color=0xf1bedf)
        await ctx.send(embed=embed)
        print('退室：' + str(vc))


    # テキストチャンネルに投稿されたテキストを読み上げる
    @commands.Cog.listener()
    async def on_message(self, message): # メッセージが投稿された時のイベント

        # コマンド実行者がサーバーのボイスチャンネルにいなかったら無視
        if not message.guild.voice_client:
            return

        # talk_tc_dictにテキストチャンネルのIDが入っていなかったら無視
        if not message.channel.id == self.talk_tc_dict[message.guild.id]:
            return

        # !が先頭に入っていたら or botだったら無視
        if message.content.startswith('!') or message.author.bot:
            if not 'やっほー！もだねちゃんだよ！' in message.content or 'ってなーに？' in message.content: # 指定テキストの場合以外に中断する
                return

        spk_msg = message.clean_content
        # print('整形前：' + spk_msg) # 置換前のテキストを出力
        spk_msg_fmt = abb_msg(spk_msg) # 置換後のテキストを変数へ格納
        # print('整形後：' + spk_msg_fmt) # 置換後のテキストを出力
        jtalk(spk_msg_fmt, 'voice_' + str(message.guild.id)) # jtalkの実行
        source = discord.FFmpegPCMAudio('voice_' + str(message.guild.id) + '.mp3') # mp3ファイルを指定
        message.guild.voice_client.play(source)


    # ボイスチャンネルへユーザーが入退室した時の処理
    @commands.Cog.listener()
    async def on_voice_state_update(self,
                                    member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):
        # before と after に変化がなければ無視
        if before.channel == after.channel:
            return
        
        print('===== VC人数の変更を検知 =====')
        # VCへ誰かが入室した時の処理（VoiceState の before が 値無し / after が 値有り だったら）
        if not before.channel and after.channel:
            print('--- VCへ入室 ---')
            vc = after.channel
            # print(vc)
            # print('VC人数：' + str(len(vc.members))) # VC人数を表示
            # print(vc.members)

        # VCから誰かが退出した時の処理（VoiceState の before が 値有り / after が 値無し だったら）
        elif before.channel and not after.channel:
            print('--- VCから退室 ---')
            vc = before.channel
            # print(vc)
            # print('VC人数：' + str(len(vc.members))) # VC人数を表示
            # print(vc.members)
            
            # botが最後の一人になったら自動退出する
            if (
                len(vc.members) == 1
                and vc.members[0] == self.bot.user
            ):
                vc = discord.utils.get(self.bot.voice_clients, channel=before.channel)
                # print(vc)
                if vc and vc.is_connected():
                    await asyncio.sleep(1)
                    print('===== 読み上げを終了します：自動退出 =====')
                    await vc.disconnect()
                    embed = discord.Embed(title='読み上げを終了したよ', description='皆いなくなったので、ボイスチャンネルから退出しました。またね！', color=0xf1bedf)
                    talk_tc = discord.utils.get(member.guild.text_channels, id=self.talk_tc_dict[member.guild.id])
                    print(talk_tc)
                    await talk_tc.send(embed=embed)
                    print('退室：' + str(vc))

        # bot が VC から退出した時の処理
        if (
            before.channel
            and not after.channel
            and member == self.bot.user
        ):
            await asyncio.sleep(1)
            print('===== 読み上げ終了時の処理を行います =====')
            # 音声データを削除
            print('--- 音声データを削除 ---')
            os.remove('voice_' + str(member.guild.id) + '.mp3')
            # talk_tc_dictからギルドIDを削除
            print('--- 読み上げ対象辞書からギルドIDを削除 ---')
            del self.talk_tc_dict[member.guild.id]
            print('読み上げ対象：' + str(self.talk_tc_dict))


def setup(bot):
    bot.add_cog(Talk(bot))