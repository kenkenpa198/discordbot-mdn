#coding: utf-8
import subprocess
import re
from datetime import datetime

import discord #discord.py
from discord.ext import commands # Bot Commands Frameworkのインポート

# open-jtalk
def jtalk(t):
    open_jtalk = ['open_jtalk']
    mech = ['-x','/usr/local/lib/open_jtalk/dic']
    htsvoice = ['-m','/usr/local/lib/open_jtalk/voice/mei/mei_happy.htsvoice']
    speed = ['-r','0.8']
    outwav = ['-ow','out.wav']
    cmd = open_jtalk + mech + htsvoice + speed + outwav
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(t.encode())
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','out.wav']
    wr = subprocess.Popen(aplay)

# メンションを省略
def abb_msg(t):
    rep = r'https?://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?' # 正規表現サンプル r'https?://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?$' から変更
    return re.sub(rep, 'URL省略', t)

if __name__ == '__main__':
    pass # say_datetime()