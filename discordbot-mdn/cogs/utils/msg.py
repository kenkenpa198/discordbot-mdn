'''Format message modules'''

import asyncio
import re

import alkana
import discord


# 置換用辞書
re_dict_first = {
    r'\n': ' ',                                                                                 # 改行を「 」に置換する
    r'https?://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?': 'URL省略',                                   # URLを省略する 正規表現サンプル r'https?://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?$' から変更
    r'<:.{1,}:\d{8,}>': ' ',                                                                    # カスタム絵文字を「 」に置換する
    r'\,|、|\.|。|\!|！|\?|？|\:|：|\;|；|\+|＋|\=|＝|\*|＊|\-|\~|\_|_|\[|「|\]|」|・|…': ' ', # 記号を「 」に置換する
    r'\d{9,}': '数値省略',                                                                      # 9桁以上の数値を省略する
}

# 置換用辞書
re_dict_end = {
    r'(D|d)iscord': 'ディスコード',
    r'64': 'ロクヨン',
    r'(G|g)(C|c)コン': 'ジーシーコン',
    r'(G|g)(C|c)': 'ゲームキューブ',
    r'(W|w)ii': 'ウィー',
    r'(S|s)witch': 'スイッチ',
    r'(G|g)(B|b)(A|a)': 'アドバンス',
    r'(G|g)(B|b)': 'ゲームボーイ',
    r'3(D|d)(S|s)': 'スリーディーエス',
    r'(D|d)(S|s)': 'ディーエス',
    r'(S|s)platoon': 'スプラトゥーン',
    r'(D|d)(X|x)': 'デラックス',
    r'(S|s)(P|p)': 'スペシャル',
    r'(D|d)(B|b)(D|d)': 'デッドバイデイライト',
    r'(T|t)witter': 'ツイッター',
    r'(S|s)hovel': 'シャベル',
    r'amiibo': 'アミーボ',
    r'空前': 'くうまえ',
    r'空後': 'くうご',
    r'空上': 'くううえ',
    r'空下': 'くうした',
    r'空(N|Ｎ|n|ｎ)': 'くうえぬ',
    r'空ダ': 'くうだ',
    r'勝った': 'かった',
    r'THE': 'ザ',
    r'BLUE': 'ブルー',
    r'HEARTS': 'ハーツ',
    r'(Y|y)oo (H|h)oo': 'やっほー',
    r'(M|m)odane': 'もだね',
    r'(M|m)dn': 'もだね',
    r'chan': 'ちゃん',
    r'(ノシ|ﾉｼ)': 'バイバイ',
    r'(w|ｗ){2,}': ' わらぁわらぁ', # 「w」「ｗ」が2つ以上続いたら「わらわら」に置換する
    r'w|ｗ': ' わらぁ',             # 「w」「ｗ」を「わら」に置換する
    r'〜|～': 'ー',                 # 「〜：波ダッシュ（Mac」「～：全角チルダ（Win」を「ー」に置換する
    r'^\s': ''                      # 文頭の空白を削除する
}

# 引数で与えられたテキストを正規表現で置換する
def re_msg(msg, dict_):
    for dict_key in dict_:
        msg = re.sub(dict_key, dict_[dict_key], msg)
    return msg

# 引数に含まれる英字をかなへ変換して返す
def en_to_kana(msg_src):
    msg_list = re.split(r'([(a-z)(A-Z)]+)', msg_src)
    msg_list_fmt = []
    for word in msg_list:
        if alkana.get_kana(word) is None:
            msg_list_fmt.append(word)
        else:
            msg_list_fmt.append(alkana.get_kana(word))
    msg_fmt = ''.join(msg_list_fmt)
    return msg_fmt

# 読み上げ用メッセージ変換
def make_talk_src(msg_src):
    m = re_msg(msg_src, re_dict_first)
    m = en_to_kana(m)
    m = re_msg(m, re_dict_end)
    # 40文字を超えたら省略する
    if len(m) > 40:
        m = m[:40]
        m += ' 以下略'
    return m

fmt_dict = {
    r'@もだねちゃん': '', # @もだねちゃん を削除
    r'@develop-mdnchan': '', # @develop-chan を削除
    r'えらい(\?|？|)': '', # えらい？を削除
    r'って(知|し)ってる(\?|？|)': '', # って知ってる？を削除
}

# セリフを与えられた引数から作成する
def make_msg(msg_src, msg_head='', msg_end=''):
    msg_fmt = re_msg(msg_src, fmt_dict)
    msg_fmt = f'{msg_head}{msg_fmt}{msg_end}'
    return msg_fmt
