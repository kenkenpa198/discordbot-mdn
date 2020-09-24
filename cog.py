# coding: utf-8

##### 読み込み #####
# Pythonモジュール
import time
import random
import re
import asyncio

# 外部モジュール
import discord
from discord.ext import commands

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
    async def p(self, ctx):
        print('===== ping! =====')
        await ctx.send('pong!')
        print(ctx)
        print(ctx.author)
        print(ctx.author.mention)
        print(ctx.message.content)
        print(ctx.message.clean_content)
        if ctx.author.voice is None: # ボイスチャンネルにコマンド実行者がいるか判定
            print('--- VCにコマンド実行者がいません ---')
            return
        print(ctx.guild.voice_channels)
        print(ctx.guild.voice_client)
        print(ctx.guild.voice_client.channel)
        print(ctx.guild.voice_client.channel.members)
        print(ctx.guild.voice_client.channel.id)

    @commands.command()
    async def w(self, ctx, what):
        print('===== whatってなーに？ =====')
        what_txt = f'{what}ってなーに？'
        await ctx.send(what_txt)
        print(what_txt)

    # @commands.command()
    # async def set(self, ctx):
    #     print('===== 初期設定を行います =====')
    #     guild = ctx.message.guild
    #     role = discord.utils.get(guild.roles, name='develop')
    #     print('変更対象：' + str(role))
    #     print('--- 役職の色を変更しました ---')
    #     await role.edit(colour=discord.Colour.from_rgb(250, 250, 250))
    #     await ctx.send(f'初期設定を行ったよ！これからよろしくねっ！')


    ## ヘルプを表示する
    @commands.command()
    async def h(self, ctx):
        # サブコマンドが指定されていない場合、メッセージを送信する
        if ctx.invoked_subcommand is None:
            await ctx.send('やっほー！もだねちゃんだよ！\n↓のコマンドを入力して指示してね！')
            embed = discord.Embed(color=0xff7777)
            embed.add_field(name='🎤 読み上げを開始する', value='```!mdn s```', inline=False)
            embed.add_field(name='ㅤ\n🎤 読み上げを終了する', value='```!mdn e```', inline=False)
            embed.add_field(name='ㅤ\n✌️ もだねちゃんとジャンケンをする', value='```!mdn j```', inline=False)
            embed.add_field(name='ㅤ\n❓ ヘルプ（コレ）を表示する', value='```!mdn h```', inline=False)
            await ctx.send(embed=embed)
    
    ## 読み上げ機能
    # 読み上げは「### テキストチャンネルに投稿されたテキストへ反応する > # 読み上げ機能用」を使用
    # 読み上げを開始する
    @commands.command()
    async def s(self, ctx):
        print('===== 読み上げを開始します =====')

        # ボイスチャンネルにコマンド実行者がいるか判定
        if ctx.author.voice is None:
            print('--- VCにコマンド実行者がいないため待機します ---')
            embed = discord.Embed(title='読み上げの実施を待機します', description='読み上げを開始するには、10秒以内にボイスチャンネルへ入室してください', color=0xff7777)
            await ctx.send(embed=embed)

            # ボイスチャンネルにコマンド実行者がいるかチェックする関数を定義
            def vc_check(m, b, a):
                return ctx.author.voice is not None # bool(ctx.author.voice)でもOK

            # ボイスチャンネルにコマンド実行者がいれば変数へVCの情報を渡す
            try:
                await self.bot.wait_for('voice_state_update', check=vc_check, timeout=10)
            except asyncio.TimeoutError:
                embed = discord.Embed(title='読み上げの開始を中断しました', description='ボイスチャンネルへもだねちゃんが接続できませんでした\n読み上げを開始するには、コマンド実行者がボイスチャンネルへ入室してください', color=0xff7777)
                await ctx.send(embed=embed)
                print('===== VCへの接続を中断しました =====')
                return
            else:
                pass #await asyncio.sleep(.5)
        else:
            pass

        global vc, var_ctx
        vc = ctx.author.voice.channel
        var_ctx = ctx
        print('接続：' + str(vc))
        # ボイスチャンネルへ接続する
        embed = discord.Embed(title='読み上げを開始します', description=':microphone: ' + str(vc), color=0x44b582)
        await ctx.send(embed=embed)
        await asyncio.sleep(1)
        await vc.connect()
        await ctx.send(f'やっほー！もだねちゃんだよ！')
        
    
    # 読み上げを終了する
    @commands.command()
    async def e(self, ctx):
        # ボイスチャンネルから退出する
        print('===== 読み上げを終了します =====')
        vc = ctx.voice_client.channel
        await ctx.voice_client.disconnect()
        embed = discord.Embed(title='読み上げを終了しました', description=':microphone: ' + str(vc), color=0xff7777)
        await ctx.send(embed=embed)
        print('退室：' + str(vc))


    ## もだねちゃんとジャンケンをする
    @commands.command()
    async def j(self, ctx):
        print('===== ジャンケンを開始します =====')
        # ジャンケンの説明文
        janken_list = ':fist:：0　:v:：1　:hand_splayed:：2'

        # ジャンケンの実行
        await ctx.send(f'{ctx.author.mention}\nジャンケンだね！負けないよ！')
        await asyncio.sleep(1)
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
                await asyncio.sleep(1.5)
                result = utils.judge_aiko(player_hand, computer_hand)
                await ctx.send(f'{ctx.author.mention}\n' + result)
                embed = discord.Embed(title='出したい手を数字で入力してね', description=str(janken_list), color=0xff7777)
                await ctx.send(embed=embed)
            else:
                break #勝敗が決まった場合whileを抜ける

        # 勝敗の結果を表示して終了
        await asyncio.sleep(1.5)
        result = utils.judge(player_hand, computer_hand)
        await ctx.send(f'{ctx.author.mention}\n' + result + '\n\n楽しかった〜！またやろうね！')
        print('===== ジャンケンを終了します =====')

    ### テキストチャンネルに投稿されたテキストへ反応する
    @commands.Cog.listener()
    async def on_message(self, message): # メッセージが投稿された時のイベント
        if message.content == 'やっほー！もだねちゃんだよ！' or 'ってなーに？' in message.content:
            if message.guild.voice_client: # 読み上げ機能用
                spk_msg = message.clean_content
                print('整形前：' + spk_msg) # 置換前のテキストを出力
                spk_msg_fmt = openjtalk.abb_msg(spk_msg) # 置換後のテキストを変数へ格納
                print('整形後：' + spk_msg_fmt) # 置換後のテキストを出力
                openjtalk.jtalk(spk_msg_fmt) # jtalkの実行
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
                spk_msg_fmt = openjtalk.abb_msg(spk_msg) # 置換後のテキストを変数へ格納
                print('整形後：' + spk_msg_fmt) # 置換後のテキストを出力
                openjtalk.jtalk(spk_msg_fmt) # jtalkの実行
                source = discord.FFmpegPCMAudio('voice_message.mp3') # mp3ファイルを指定
                message.guild.voice_client.play(source)
            else:
                return

    @commands.Cog.listener()
    async def on_voice_state_update(self,
                                    member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):

        print('--- VCステータスの変更を検知 ---')
        if not before.channel and after.channel: # ユーザーの前と後のVCの状態を比較して、値が有る状態だったら（入室したら）
            print('--- VCへ入室 ---')
            vcl = discord.utils.get(self.bot.voice_clients, channel=after.channel)
            print(vcl)
        elif before.channel and not after.channel: # ユーザーの前と後のVCの状態を比較して、値が無い状態だったら（退室したら）
            print('--- VCから退室 ---')
            vch = before.channel
            if len(vch.members) == 1 and vch.members[0] == self.bot.user: # 
                vcl = discord.utils.get(self.bot.voice_clients, channel=before.channel)
                if vcl and vcl.is_connected():
                    print('===== 読み上げを終了します =====')
                    await vcl.disconnect()
                    embed = discord.Embed(title='読み上げを終了しました', description=':microphone: ' + str(vc), color=0xff7777)
                    await var_ctx.send(embed=embed)
                    print('退室：' + str(vc))

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    bot.add_cog(Cog(bot)) #TestCogにBotを渡してインスタンス化し、Botにコグとして登録する