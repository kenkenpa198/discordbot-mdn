#coding: utf-8
import subprocess
import re
from datetime import datetime

import discord #discord.py
from discord.ext import commands # Bot Commands Frameworkのインポート

def jtalk(t):
    open_jtalk = ['open_jtalk']
    mech = ['-x','/usr/local/Cellar/open-jtalk/1.11/dic']
    htsvoice = ['-m','/usr/local/Cellar/open-jtalk/1.11/voice/mei/mei_happy.htsvoice']
    speed = ['-r','0.8']
    outwav = ['-ow','out.wav']
    cmd = open_jtalk + mech + htsvoice + speed + outwav
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(t.encode())
    c.stdin.close()
    c.wait()
    aplay = ['afplay','-q','out.wav']
    wr = subprocess.Popen(aplay)

def say_datetime():
    d = datetime.now()
    text = '%s月%s日、%s時%s分%s秒aあああああ' % (d.month, d.day, d.hour, d.minute, d.second)
    jtalk(text)

def abb_mention(t):
    if '<@' in t:
        t.replace(re.compile('<@'), '')
    else:
        return
        

def abb_url(t):
    pass

if __name__ == '__main__':
    say_datetime()