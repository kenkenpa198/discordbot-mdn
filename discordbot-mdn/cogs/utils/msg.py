"""Format message modules"""

import re
import alkana

# alkana へ外部辞書を登録
alkana.add_external_data('./cogs/csv/alkana_dict.csv')

# 置換用辞書（かな変換の前処理用）
init_dict = {
    r'\n': ' ',                                               # 改行を「 」に置換する
    r'https?://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?': 'URL省略', # URLを省略する
    r'<:.{1,}:\d{8,}>': ' ',                                  # カスタム絵文字を「 」に置換する
    r'\,|、|\.|。|\!|！|\?|？|\:|：|\;|；|\+|＋|\=|＝|\*|＊|\-|\~|\_|_|\[|「|\]|」|・|…': ' ', # 記号を「 」に置換する
    r'\d{9,}': '数値省略'                                     # 9桁以上の数値を省略する
}

# 置換用辞書（かな変換の後処理用）
deinit_dict = {
    r'(w|ｗ){2,}': ' わらぁわらぁ',                           # 「w」「ｗ」が2つ以上続いたら「わらわら」に置換する
    r'w|ｗ': ' わらぁ',                                       # 「w」「ｗ」を「わら」に置換する
    r'〜|～': 'ー',                                           # 「〜：波ダッシュ（Mac」「～：全角チルダ（Win」を「ー」に置換する
    r'^\s': ''                                                # 文頭の空白を削除する
}

# あいさつ機能用辞書
hello_dict = {
    r'@もだねちゃん': '',                                     # 「@もだねちゃん」を削除
    r'@develop-mdnchan': '',                                  # 「@develop-chan」を削除
    r'えらい(\?|？|)': '',                                    # 「えらい？」を削除
    r'って(知|し)ってる(\?|？|)': ''                          # 「って知ってる？」を削除
}

def re_text(text, dict_):
    """
    引数で与えられたテキストを正規表現で置換する

    Parameters
    ----------
    text : str
        置換対象のテキスト
    dict_ : dict
        置換用の辞書。キーのテキストを値のテキストに置換する

    Returns
    -------
    text : str
        置換されたテキスト
    """
    for dict_key in dict_:
        text = re.sub(dict_key, dict_[dict_key], text)
    return text

def do_alkana(text):
    """
    alkana を実行して語句をかなへ変換

    Parameters
    ----------
    text : str
        置換対象のテキスト

    Returns
    -------
    text : str
        置換されたテキスト
    """
    words = re.split(r'([(a-z)(A-Z)]+)', text)
    converted_words = []
    for word in words:
        if alkana.get_kana(word) is None:
            converted_words.append(word)
        else:
            converted_words.append(alkana.get_kana(word))
    return ''.join(converted_words)

def make_talk_src(text):
    """
    読み上げ用のメッセージへ変換する

    Parameters
    ----------
    text : str
        変換対象のテキスト

    Returns
    -------
    m : str
        変換されたテキスト
    """
    m = re_text(text, init_dict)
    m = do_alkana(m)
    m = re_text(m, deinit_dict)
    # 40文字を超えたら省略する
    if len(m) > 40:
        m = m[:40]
        m += ' 以下略'
    print(text)
    print(m)
    return m

def make_msg(text, msg_head='', msg_end=''):
    """
    セリフを与えられた引数から作成する
    """
    converted_text = re_text(text, hello_dict)
    return f'{msg_head}{converted_text}{msg_end}'
