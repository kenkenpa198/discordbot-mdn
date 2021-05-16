import asyncio
import io
import os
import subprocess
import wave

import discord
from discord.ext import commands

from .utils import msg
from .utils import psql
from .utils import voice


##### コグ #####
class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    ##### 読み上げを開始する #####
    @commands.command(aliases=['s'])
    async def start(self, ctx, tch: discord.TextChannel=None):
        print('===== 読み上げを開始します =====')

        # botが既にボイスチャンネルへ入室していないか判定
        if ctx.guild.voice_client:
            print('--- エラーコード：002 ---')
            embed = discord.Embed(title='コマンドを受け付けられませんでした',description='私はもう入室済みだよ…！\nこちらのコマンドを実行して、使い方を確認してみてね！', color=0xffab6f)
            embed.add_field(name='ㅤ\n❓ ヘルプを表示する', value='```!mdn h```', inline=False)
            await ctx.send(embed=embed)
            return

        # ボイスチャンネルにコマンド実行者がいるか判定
        if not ctx.author.voice:
            print('--- VCにコマンド実行者がいないため待機します ---')
            embed = discord.Embed(title='読み上げの実施を待機するよ', description='読み上げを開始するには、10秒以内にボイスチャンネルへ入室してね。', color=0xe3e5e8)
            await ctx.send(embed=embed)

            # 10秒まで待機
            # ボイスチャンネルにコマンド実行者が入ったら続行する
            try:
                await self.bot.wait_for('voice_state_update', check=voice.vc_check, timeout=10)
            except asyncio.TimeoutError:
                embed = discord.Embed(title='読み上げの実施を中断したよ', description='読み上げを開始するには、コマンド実行者がボイスチャンネルへ入室してね。', color=0xffab6f)
                await ctx.send(embed=embed)
                print('===== VCへの接続を中断しました =====')
                return
            else:
                print('--- VCにコマンド実行者が入室しました ---')
                print('--- 処理を再開します ---')
                await asyncio.sleep(.5)

        async with ctx.channel.typing():
            # 読み上げ対象のサーバー/ ボイスチャンネル / テキストチャンネルを変数に格納
            print('--- 読み上げ対象を設定 ---')
            talk_guild     = ctx.guild                # サーバー
            talk_vc        = ctx.author.voice.channel # ボイスチャンネル
            if tch:
                # !mdn s に引数がある場合は指定のテキストチャンネルを格納
                talk_channel = discord.utils.get(ctx.guild.text_channels, name=tch.name)
                send_hello = False
            else:
                # 引数がない場合はコマンドを実行したテキストチャンネルを格納
                talk_channel = ctx.channel
                send_hello = True

            # 読み上げるサーバー / テキストチャンネル / ボイスチャンネルの ID を DB へ格納
            print('--- 各 ID を 読み上げ対象 DB へ格納 ---')
            guild_id   = talk_guild.id
            vc_id      = talk_vc.id
            channel_id = talk_channel.id
            print('対象サーバー ID           ：' + str(guild_id))
            print('対象ボイスチャンネル ID   ：' + str(vc_id))
            print('対象テキストチャンネル ID ：' + str(channel_id))

            psql.run_query('cogs/sql/talk/upsert_target_id.sql', {'guild_id': guild_id, 'vc_id': vc_id, 'channel_id': channel_id})
            print('--- DB へ格納完了 ---')

        embed = discord.Embed(title='読み上げを開始するよ',description='こちらの内容でおしゃべりを始めるね！', color=0xffd6e9)
        embed.add_field(name='ㅤ\n🎤 入室ボイスチャンネル', value=talk_vc)
        embed.add_field(name='ㅤ\n📗 読み上げ対象', value='<#' + str(talk_channel.id) +'>')
        embed.set_footer(text='ㅤ\nヒント：\n読み上げ対象を再設定したい時や、私がうまく動かない時は「 !mdn c 」コマンドを使用してください。')
        await ctx.send(embed=embed)
        await asyncio.sleep(1)

        # ボイスチャンネルへ接続する
        print('--- VC へ接続 ---')
        print('接続：' + str(talk_vc.id))
        await talk_vc.connect()
        await asyncio.sleep(.5)
        if send_hello:
            await ctx.send(f'やっほー！もだねちゃんだよ！')


    ##### 読み上げ対象のテキストチャンネルを再設定する #####
    @commands.command(aliases=['c'])
    async def change(self, ctx, tch: discord.TextChannel=None):
        print ('===== 読み上げ対象のテキストチャンネルを再設定します =====')

        # botがボイスチャンネルにいるか判定
        if not ctx.guild.voice_client:
            print('--- bot が VC にいないため入室を中止 ---')
            embed = discord.Embed(title='コマンドを受け付けられませんでした',description='そのコマンドは、私がボイスチャンネルへ入室している時のみ使用できるよ。\nこちらのコマンドを先に実行してね。', color=0xffab6f)
            embed.add_field(name='ㅤ\n🎤 読み上げを開始する', value='```!mdn s```', inline=False)
            await ctx.send(embed=embed)
            return

        async with ctx.channel.typing():
            # 読み上げ対象のサーバー/ ボイスチャンネル / テキストチャンネルを変数に格納
            print('--- 読み上げ対象を設定 ---')
            talk_guild     = ctx.guild                # サーバー
            talk_vc        = ctx.author.voice.channel # ボイスチャンネル
            if tch:
                # !mdn s に引数がある場合は指定のテキストチャンネルを格納
                talk_channel = discord.utils.get(ctx.guild.text_channels, name=tch.name)
            else:
                # 引数がない場合はコマンドを実行したテキストチャンネルを格納
                talk_channel = ctx.channel

            # 読み上げるサーバー / テキストチャンネル / ボイスチャンネルの ID を DB へ格納
            print('--- 各 ID を 読み上げ対象 DB へ格納 ---')
            guild_id   = talk_guild.id
            vc_id      = talk_vc.id
            channel_id = talk_channel.id
            print('対象サーバー ID           ：' + str(guild_id))
            print('対象ボイスチャンネル ID   ：' + str(vc_id))
            print('対象テキストチャンネル ID ：' + str(channel_id))

            psql.run_query('cogs/sql/talk/upsert_target_id.sql', {'guild_id': guild_id, 'vc_id': vc_id, 'channel_id': channel_id})
            print('--- DB へ格納完了 ---')
    
        embed = discord.Embed(title='読み上げ対象を再設定したよ',description='こちらのテキストチャンネルでおしゃべりを再開するね！', color=0xffd6e9)
        embed.add_field(name='ㅤ\n:green_book: 読み上げ対象', value='<#' + str(talk_channel.id) +'>')
        await ctx.send(embed=embed)


    ##### 読み上げを終了する #####
    @commands.command(aliases=['e'])
    async def end(self, ctx):
        print('===== 読み上げを終了します：コマンド受付 =====')

        # botがボイスチャンネルにいるか判定
        if not ctx.guild.voice_client:
            print('--- エラーコード：002 ---')
            embed = discord.Embed(title='コマンドを受け付けられませんでした',description='そのコマンドは、私がボイスチャンネルへ入室している時のみ使用できるよ。\nこちらのコマンドを先に実行してね。', color=0xffab6f)
            embed.add_field(name='ㅤ\n🎤 読み上げを開始する', value='```!mdn s```', inline=False)
            await ctx.send(embed=embed)
            return
        
        async with ctx.channel.typing():
        # ボイスチャンネルから退出する
            guild_id = ctx.guild.id
            talk_id = None
            talk_id = psql.run_query_to_var('cogs/sql/talk/select_channel_id.sql', {'guild_id': guild_id})
            talk_channel = ctx.guild.get_channel(talk_id)
            # talk_channel = discord.utils.get(ctx.guild.text_channels, id=int(talk_id))
            talk_vc = ctx.voice_client.channel
            await ctx.voice_client.disconnect()
        embed = discord.Embed(title='読み上げを終了したよ', description='ボイスチャンネルから退出して読み上げを終了しました。またね！', color=0xffd6e9)
        await talk_channel.send(embed=embed)
        print('退室：' + str(talk_vc.id))


    ##### テキストチャンネルに投稿されたテキストを読み上げる #####
    @commands.Cog.listener()
    async def on_message(self, message):

        # メッセージ投稿者がサーバーのボイスチャンネルにいなかったら無視
        if not message.guild.voice_client:
            return

        # DB にテキストチャンネルのIDが入っていなかったら無視
        talk_channel_list = psql.run_query_to_list('cogs/sql/talk/select_channel_ids.sql')
        if not str(message.channel.id) in talk_channel_list:
            return

        # !が先頭に入っていたら or botだったら無視
        if message.content.startswith('!') or message.author.bot:
            # もだねちゃんのセリフは通す
            # if not 'やっほー！もだねちゃんだよ！' in message.content: # あいさつのみ通す時
            if not message.author == self.bot.user:
                return

        print('===== 読み上げを実行します =====')
        print('--- メッセージの整形 ---')
        talk_msg_src = message.clean_content
        talk_msg_fmt = msg.make_talk_src(talk_msg_src)
        print(talk_msg_fmt)

        print('--- 音声データの作成 ---')
        try:
            voice_path = voice.jtalk(talk_msg_fmt, message.guild.id) # 音声データを作成してファイルパスを変数へ格納
            
            # 音声データを開いて再生する
            with wave.open(voice_path, 'rb') as wi:
                voice_src = wi.readframes(-1)
                stream = io.BytesIO(voice_src) # バイナリファイルとして読み込み
                talk_src = discord.PCMAudio(stream) # 音声ファイルを音声ソースとして変数に格納
                print('--- 音声データを再生 ---')
                message.guild.voice_client.play(talk_src) # ボイスチャンネルで再生

            # 以下だと音声の最初にノイズが走る
            # stream = open(voice_path, 'rb')
            # talk_src = discord.PCMAudio(stream)
            # print('--- 音声データを再生 ---')
            # message.guild.voice_client.play(talk_src, after=lambda e: stream.close()) # ボイスチャンネルで再生
            
            # 再生が終わっていたら音声データを削除する
            while message.guild.voice_client.is_playing():
                await asyncio.sleep(1)
            if os.path.isfile(voice_path):
                print('--- 音声データを削除 ---')
                os.remove(voice_path)
        except:
            print('--- 音声データの作成不可 ---')


    ##### ボイスチャンネルへユーザーが入退室した時の処理 #####
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
            print('--- VC へ入室 ---')
            vc = after.channel
            # print(vc.members) # VC人数を表示

        # VC から誰かが退出した時の処理（VoiceState の before が 値有り / after が 値無し だったら）
        elif before.channel and not after.channel:
            print('--- VC から退室 ---')
            vc = before.channel
            
            # botが最後の一人になったら自動退出する
            if (
                len(vc.members) == 1
                and vc.members[0] == self.bot.user
            ):
                vc = discord.utils.get(self.bot.voice_clients, channel=before.channel)
                if vc and vc.is_connected():
                    await asyncio.sleep(1)
                    print('===== 読み上げを終了します：自動退出 =====')
                    guild_id = member.guild.id
                    talk_id = None
                    talk_id = psql.run_query_to_var('cogs/sql/talk/select_channel_id.sql', {'guild_id': guild_id})
                    talk_channel = member.guild.get_channel(talk_id)
                    async with talk_channel.typing():
                        await vc.disconnect()
                    embed = discord.Embed(title='読み上げを終了したよ', description='皆いなくなったので、ボイスチャンネルから退出しました。またね！', color=0xffd6e9)
                    await talk_channel.send(embed=embed)
                    print('退室：' + str(talk_id))

        # bot が VC から退出した時の処理
        if (
            before.channel
            and not after.channel
            and member == self.bot.user
        ):
            await asyncio.sleep(1)
            print('===== 読み上げ終了時の処理を行います =====')

            # 音声データを削除
            voice_path = 'voice_' + str(member.guild.id) + '.wav'
            if os.path.isfile(voice_path):
                print('--- 残っていた音声データを削除 ---')
                os.remove(voice_path)
            # DB から読み上げ対象のレコードを削除
            print('--- 読み上げ対象 DB から退出した ID のレコードを削除 ---')
            guild_id = member.guild.id
            psql.run_query('cogs/sql/talk/delete_target_id.sql', {'guild_id': guild_id})
            print('レコードを削除：' + str(guild_id))


def setup(bot):
    bot.add_cog(Talk(bot))