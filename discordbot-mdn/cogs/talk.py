"""Cog Talk"""

import asyncio
import io
import logging
import os
import subprocess
import wave

import discord
from discord.ext import commands
from jtalkbot import openjtalk

from .utils import psql
from .utils import replace as rp
from .utils import send as sd


##### コグ #####
class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_talkable(self, message):
        """
        メッセージが読み上げ可能かチェックする

        Parameters
        ----------
        message : class
            チェック対象のメッセージ

        Returns
        -------
        True : bool
            読み上げ可能な場合は真を返す
        False : bool
            読み上げ不可能な場合は偽を返す
        """
        # メッセージが投稿されたサーバーに Bot のボイス接続が存在しなかったら無視
        # 別のサーバーに投稿されたメッセージに対して反応を行わなくさせるための条件
        if not message.guild.voice_client:
            return False

        # もだねちゃん以外の Bot だったら無視
        if message.author.bot and message.author != self.bot.user:
            return False

        # 本文が存在しなかったら無視
        if not message.content:
            return False

        # !が先頭に入っていたら（コマンドだったら）無視
        if message.content.startswith('!'):
            return False

        # talk_channels テーブルにテキストチャンネルのIDが入っていなかったら無視
        talk_channel_list = psql.do_query_fetch_list('./sql/talk/select_channel_ids.sql')
        if str(message.channel.id) not in talk_channel_list:
            return False

        return True

    def jtalk(self, text, guild_id):
        """
        音声ファイルを作成する

        Parameters
        ----------
        text : str
            音声ファイルのソースとなるテキスト
        guild_id : int
            ギルド ID 。音声ファイルのファイルネームに使用する

        Returns
        -------
        voice_path : str
            生成した音声ファイルのファイルパス
        """

        # open jtalk コマンド
        open_jtalk = ['open_jtalk']

        # 声質のオプション指定
        mech       = ['-x', '/usr/local/lib/open_jtalk/dic']
        htsvoice   = ['-m', '/usr/local/lib/open_jtalk/voice/mei/mei_happy.htsvoice']
        speed      = ['-r',   '0.7'] # スピーチ速度係数
        halftone   = ['-fm', '-3.5'] # 追加ハーフトーン（高低）
        volume     = ['-g',  '-5.0'] # 声の大きさ

        # ファイルパスの指定
        voice_path = 'voice_' + str(guild_id) + '.wav'
        outwav     = ['-ow', voice_path]

        # コマンドを作成して標準入力から作成
        cmd        = open_jtalk + mech + htsvoice + speed + halftone + volume + outwav
        c          = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        c.stdin.write(text.encode())
        c.stdin.close()
        c.wait()

        # 音声ファイルをモノラルからステレオへ変換
        voice_fmt_src = openjtalk.mono_to_stereo(voice_path)
        os.remove(voice_path)
        with open(voice_path, 'wb') as f:
            f.write(voice_fmt_src)

        return voice_path

    def play_voice(self, voice_path, message):
        """
        音声ファイルを再生する

        Parameters
        ----------
        voice_path : str
            再生対象の音声ファイルのファイルパス
        message : class
            チェック対象のメッセージ

        Notes
        -----
        以下だと音声の最初にノイズが走る
            stream = open(voice_path, 'rb')
            talk_src = discord.PCMAudio(stream)
            message.guild.voice_client.play(talk_src, after=lambda e: stream.close())
        """
        with wave.open(voice_path, 'rb') as wi:
            voice_src = wi.readframes(-1)
        stream = io.BytesIO(voice_src) # バイナリファイルとして読み込み
        talk_src = discord.PCMAudio(stream) # 音声ファイルを音声ソースとして変数に格納
        message.guild.voice_client.play(talk_src) # ボイスチャンネルで再生

    def talk_deinit(self, member):
        """
        読み上げを終了した際の後処理

        Parameters
        ----------
        member : class
            トリガーとなる member クラス

        Notes
        -----
        音声ファイルの削除は通常の再生時に行っているが、
        削除前にボイスチャンネルを抜けた場合、削除処理が行われないため後処理でも削除処理を行う。
        """
        # 音声ファイルを削除
        voice_path = 'voice_' + str(member.guild.id) + '.wav'
        if os.path.isfile(voice_path):
            logging.info('残っていた音声ファイルを削除')
            os.remove(voice_path)

        # talk_channels テーブルから読み上げ対象のレコードを削除
        logging.info('talk_channels テーブルから退出した ID のレコードを削除')
        guild_id = member.guild.id
        psql.do_query('./sql/talk/delete_target_id.sql', {'guild_id': guild_id})


    ##### 読み上げを開始する #####
    @commands.hybrid_command(aliases=['s', 'start'], description='読み上げを開始するよ')
    async def t_start(self, ctx, text_channel: discord.TextChannel=None):
        logging.info('読み上げ開始コマンドを受付')

        # botが既にボイスチャンネルへ入室している場合はボイスチャンネルを再設定する
        if ctx.guild.voice_client:
            # 読み上げ対象のサーバー/ ボイスチャンネル / テキストチャンネルを変数に格納
            logging.info('読み上げ対象チャンネルを設定')
            talk_guild     = ctx.guild                # サーバー
            talk_vc        = ctx.author.voice.channel # ボイスチャンネル
            if text_channel:
                # !mdn s に引数がある場合は指定のテキストチャンネルを格納
                talk_channel = discord.utils.get(ctx.guild.text_channels, name=text_channel.name)
            else:
                # 引数がない場合はコマンドを実行したテキストチャンネルを格納
                talk_channel = ctx.channel

            # 読み上げるサーバー / テキストチャンネル / ボイスチャンネルの ID を talk_channels テーブルへ格納
            logging.info('読み上げ対象チャンネルの情報を talk_channels テーブルへ格納')
            guild_id   = talk_guild.id
            vc_id      = talk_vc.id
            channel_id = talk_channel.id

            psql.do_query(
                './sql/talk/upsert_target_id.sql',
                {'guild_id': guild_id, 'vc_id': vc_id, 'channel_id': channel_id}
            )

            await sd.send_talk_restart(ctx, channel_id)
            return

        # ボイスチャンネルにコマンド実行者がいるか判定
        if not ctx.author.voice:
            logging.info('ボイスチャンネルにコマンド実行者がいないため待機')
            await sd.send_talk_wait(ctx)

            # 10秒まで待機
            # ボイスチャンネルにコマンド実行者が入ったら続行する
            def check(member, before, after):
                return member == ctx.author and member.voice

            try:
                await self.bot.wait_for('voice_state_update', check=check, timeout=10)
            except asyncio.TimeoutError:
                logging.warning('ボイスチャンネルへの接続を中断')
                await sd.send_talk_stop(ctx)
                return
            else:
                logging.info('ボイスチャンネルへのコマンド実行者入室を検知')
                logging.info('処理を再開')
                await asyncio.sleep(.5)

        # 読み上げ対象のサーバー/ ボイスチャンネル / テキストチャンネルを変数に格納
        logging.info('読み上げ対象チャンネルを設定')
        talk_guild     = ctx.guild                # サーバー
        talk_vc        = ctx.author.voice.channel # ボイスチャンネル
        if text_channel:
            # !mdn s に引数がある場合は指定のテキストチャンネルを格納
            talk_channel = discord.utils.get(ctx.guild.text_channels, name=text_channel.name)
            send_hello = False
        else:
            # 引数がない場合はコマンドを実行したテキストチャンネルを格納
            talk_channel = ctx.channel
            send_hello = True

        # 読み上げるサーバー / ボイスチャンネル / テキストチャンネルの ID を talk_channels テーブルへ格納
        logging.info('読み上げ対象チャンネルの情報を talk_channels テーブルへ格納')
        guild_id   = talk_guild.id
        vc_id      = talk_vc.id
        channel_id = talk_channel.id

        psql.do_query(
            './sql/talk/upsert_target_id.sql',
            {'guild_id': guild_id, 'vc_id': vc_id, 'channel_id': channel_id}
        )

        await sd.send_talk_start(ctx, talk_vc, channel_id)
        await asyncio.sleep(1)

        # ボイスチャンネルへ接続する
        logging.info('ボイスチャンネルへ接続')
        await talk_vc.connect()

        # あいさつを送信
        if send_hello:
            await asyncio.sleep(.5)
            await sd.send_yahho(ctx)


    ##### 読み上げを終了する #####
    @commands.hybrid_command(aliases=['e', 'end'], description='読み上げを終了するよ')
    async def t_end(self, ctx):
        logging.info('読み上げ終了コマンドを受付')

        # botがボイスチャンネルにいなかったらメッセージを送信
        if not ctx.guild.voice_client:
            logging.warning('bot がボイスチャンネルへいなかったためメッセージを送信')
            await sd.send_talk_not_in_vc(ctx)
            return

        # ボイスチャンネルから退出する
        logging.info('ボイスチャンネルから切断')
        await ctx.voice_client.disconnect()
        await sd.send_talk_end(ctx)


    ##### テキストチャンネルに投稿されたテキストを読み上げる #####
    @commands.Cog.listener()
    async def on_message(self, message):
        logging.info('メッセージを受付')

        # 読み上げ不可能な場合は終了
        if not self.is_talkable(message):
            logging.info('is_talkable: False')
            return

        logging.info('is_talkable: True')
        logging.info('読み上げの実行を開始')

        # 読み上げ中であれば1秒待機
        while message.guild.voice_client.is_playing():
            logging.info('音声を再生中のため待機')
            await asyncio.sleep(1)

        logging.info('メッセージを整形')
        talk_msg = rp.make_talk_src(message.clean_content)

        logging.info('音声ファイルを生成')
        voice_path = self.jtalk(talk_msg, message.guild.id)

        logging.info('音声ファイルを再生')
        self.play_voice(voice_path, message)

        if os.path.isfile(voice_path):
            logging.info('音声ファイルを削除')
            os.remove(voice_path)


    ##### ボイスチャンネルへユーザーが入退室した時の処理 #####
    @commands.Cog.listener()
    async def on_voice_state_update(self,
                                    member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):
        # before と after に変化がなければ無視
        if before.channel == after.channel:
            return

        # VCへ誰かが入室した時の処理（VoiceState の before が 値無し / after が 値有り だったら）
        if not before.channel and after.channel:
            logging.info('ボイスチャンネル人数の変更を検知: 入室')
            # vc = after.channel
            # logging.info(vc.members) # VC人数を表示

        # VC から誰かが退出した時の処理（VoiceState の before が 値有り / after が 値無し だったら）
        elif before.channel and not after.channel:
            logging.info('ボイスチャンネル人数の変更を検知: 退室')
            vc_b = before.channel

            # Bot が最後の一人になったら自動退出する
            if (
                len(vc_b.members) == 1
                and vc_b.members[0] == self.bot.user
            ):
                vc = discord.utils.get(self.bot.voice_clients, channel=vc_b)
                if vc and vc.is_connected():
                    logging.info('読み上げを終了: 自動退出')
                    await asyncio.sleep(1)
                    await vc.disconnect()

                    # 自動退出したメッセージを送信
                    guild_id = member.guild.id
                    talk_id = int(psql.do_query_fetch_one('./sql/talk/select_channel_id.sql', {'guild_id': guild_id}))
                    talk_channel = member.guild.get_channel(talk_id)
                    await sd.send_talk_end_auto(talk_channel)

        # Bot が VC から退出した時の処理
        if (
            before.channel
            and not after.channel
            and member == self.bot.user
        ):
            logging.info('読み上げ終了時の処理を実行')
            self.talk_deinit(member)

async def setup(bot):
    await bot.add_cog(Talk(bot))
