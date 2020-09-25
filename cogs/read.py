# coding: utf-8
import discord
from discord.ext import commands
import asyncio
import openjtalk

class Read(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def s(self, ctx):
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
                pass #await asyncio.sleep(.5)
        else:
            pass

        global vc, var_ctx
        vc = ctx.author.voice.channel
        var_ctx = ctx
        print('接続：' + str(vc))
        # ボイスチャンネルへ接続する
        await vc.connect()
        embed = discord.Embed(title='読み上げを開始します', description='このボイスチャンネルに接続しました\n:microphone: ' + str(vc), color=0x44b582)
        await ctx.send(embed=embed)
        await asyncio.sleep(1)
        await ctx.send(f'やっほー！もだねちゃんだよ！')

    # 読み上げを終了する
    @commands.command()
    async def e(self, ctx):
        # ボイスチャンネルから退出する
        print('===== 読み上げを終了します =====')
        # vc = ctx.voice_client.channel
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

    # 人がいなくなったら自動で退出する
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
                    embed = discord.Embed(title='読み上げを終了しました', description='誰もいなくなったので、ボイスチャンネルから退出しました', color=0xff7777)
                    await var_ctx.send(embed=embed)
                    print('退室：' + str(vc))


def setup(bot):
    bot.add_cog(Read(bot))