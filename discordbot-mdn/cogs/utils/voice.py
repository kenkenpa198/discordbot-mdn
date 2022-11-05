'''Generate voice modules'''

import os
import subprocess

from jtalkbot import openjtalk


##### チェック用モジュール #####
# ボイスチャンネルにコマンド実行者がいるか判定する
def vc_check(m, b, a):
    return m.voice is not None # bool(ctx.author.voice)でもOK

# botが発言中か判定する
def playing_check(m):
    if m.guild.voice_client:
        return m.guild.voice_client.is_playing() is False


##### モジュール #####
# 音声ファイル作成
def jtalk(t, guild_id):
    # 音声データの作成
    voice_path = 'voice_' + str(guild_id) + '.wav'
    open_jtalk = ['open_jtalk']
    mech       = ['-x', '/usr/local/lib/open_jtalk/dic']
    htsvoice   = ['-m', '/usr/local/lib/open_jtalk/voice/mei/mei_happy.htsvoice']

    # 声質の設定
    speed      = ['-r',   '0.7'] # スピーチ速度係数
    halftone   = ['-fm', '-3.5'] # 追加ハーフトーン（高低）
    volume     = ['-g',  '-5.0'] # 声の大きさ

    outwav     = ['-ow', voice_path]
    cmd        = open_jtalk + mech + htsvoice + speed + halftone + volume + outwav
    c          = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    c.stdin.write(t.encode())
    c.stdin.close()
    c.wait()

    # 音声データをモノラルからステレオへ変換
    voice_fmt_src = openjtalk.mono_to_stereo(voice_path)
    os.remove(voice_path)
    with open(voice_path, 'wb') as f:
        f.write(voice_fmt_src)

    return voice_path
