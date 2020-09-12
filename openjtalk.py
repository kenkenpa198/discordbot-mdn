#coding: utf-8
import os
import subprocess
import re
from pydub import AudioSegment

# open-jtalk
def jtalk(t, filepath='voice_message'):
    open_jtalk = ['open_jtalk']
    mech = ['-x','/usr/local/Cellar/open-jtalk/1.11/dic']
    htsvoice = ['-m','/usr/local/Cellar/open-jtalk/1.11/voice/mei/mei_happy.htsvoice']
    speed = ['-r','0.8']
    outwav = ['-ow', filepath+'.wav']
    cmd = open_jtalk + mech + htsvoice + speed + outwav
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(t.encode())
    c.stdin.close()
    c.wait()
    audio_segment = AudioSegment.from_wav(filepath+'.wav')
    os.remove(filepath+'.wav')
    audio_segment.export(filepath+'.mp3', format='mp3')
    return filepath+'.mp3'

# メンションを省略
def abb_msg(t):
    rep = r'https?://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?' # 正規表現サンプル r'https?://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?$' から変更
    return re.sub(rep, 'URL省略', t)

if __name__ == '__main__':
    pass # say_datetime()