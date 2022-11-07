"""Cog Uranai"""

from datetime import datetime
import logging
import random

from discord.ext import commands
from discord.ext import tasks

from .utils import psql
from .utils import send as sd

# TODO: CSV などへ切り出し
##### 占い用リスト・辞書 #####
# 運勢結果リスト
fortune_list = [
    '🕺 友達運',
    '💞 恋愛運',
    '🎮 ゲーム運',
    '💰 金運',
    '📝 勉強運',
    '💪 健康運',
    '🌈 お天気運',
    '🛌 睡眠運',
    '🖌 お絵描き運',
    '⚽️ スポーツ運',
    '💡 ひらめき運',
    '⚔️ 勝負運',
    '🥘 お料理運',
    '🔥 逆転運',
    '🛒 お買い物運',
    '👔 お仕事運',
    '😭 感動運'
]

# 運勢結果リスト
star_list = ['★', '★★', '★★★', '★★★★', '★★★★★', '⭐️⭐️⭐️⭐️⭐️⭐️']

# ラッキーアイテムリスト
lucky_list = [
    '🍎 赤色',
    '🎇 橙色',
    '🍋 黄色',
    '📗 緑色',
    '🐳 青色',
    '🔮 紫色',
    '🐈‍⬛ 黒色',
    '🐑 白色',
    '🙆‍♂️ リアクション',
    '🍞 パン',
    '🍚 お米',
    '🍖 お肉',
    '🍜 ラーメン',
    '🐟 お魚',
    '🥬 野菜',
    '🍓 果物',
    '💊 お薬',
    '🍫 チョコレート',
    '🍬 アメ',
    '🍛 大好物',
    '🥤 ジュース',
    '🍵 お茶',
    '🐱 猫',
    '🐶 犬',
    '🐿 どうぶつ',
    '🎮 ゲーム',
    '👜 カバン',
    '🖊 ペン',
    '📔 ノート',
    '🎧 音楽',
    '🪕 普段は聴かない音楽',
    '👛 お財布',
    '💬 Discord',
    '💻 パソコン',
    '📱 携帯電話',
    '📺 テレビ',
    '🎞 動画',
    '👕 シャツ',
    '👚 お気に入りの服',
    '👘 あまり着ない服',
    '🚃 電車',
    '🚙 車',
    '🚓 パトカー',
    '🚠 珍しい乗り物',
    '🤝 人助け',
    '🪟 窓',
    '🏙 お昼',
    '🌇 夕焼け',
    '🌌 夜空',
    '🗡 斬撃',
    '🔨 打撃',
    '🏹 射撃',
    '😷 マスク',
    '🧸 ぬいぐるみ',
    '🎏 季節モノ',
    '⏳ 3分',
    '📻 レトロ',
    '🚽 トイレ',
    '🛀 お風呂',
    '🚿 シャワー',
    '💇‍♀️ 自分磨き',
    '💓 ドキドキ',
    '🔑 カギ',
    '🔀 シャッフル再生',
    '🔁 リピート再生',
    '😎 ドヤ顔',
    '😳 びっくり',
    '😄 笑顔',
    '🤔 考察',
    '😆 わーい',
    '😪 おねむ',
    '🐕 お散歩',
    '👦 キャラメイク',
    '📹 配信',
    '🍦 アイス',
    '🕊️ SNS',
    '📺 動画サイト',
    '🎮 コントローラー',
    '🦖 古代',
    '📡 未来',
    '📰 ニュース'
    ]

# played_list の中身を削除する関数を定義
def delete_played_tb():
    """占い済みテーブルのレコードを削除する"""
    logging.info('played_fortune_users テーブルのレコードを削除')
    psql.do_query('./sql/uranai/delete_user_id.sql')


##### コグ #####
class Uranai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 指定日時に played_fortune_users テーブルの中身を削除する
    @tasks.loop(seconds=60)
    async def loop():
        now = datetime.now().strftime('%H:%M')
        if now == '00:00':
            delete_played_tb()
    # ループ処理を実行
    loop.start()

    # もだねちゃん占い
    @commands.hybrid_command(aliases=['u'], description='今日の運勢を占うよ')
    async def uranai(self, ctx):
        logging.info('占いコマンドを受付')

        # played_fortune_users テーブルにユーザー ID があるか判定
        async with ctx.channel.typing():
            logging.info('played_fortune_users テーブルのユーザー ID をチェック')
            played_list = []
            played_list = psql.do_query_fetch_list('./sql/uranai/select_user_id.sql')

        # played_list にユーザーIDがあるか判定
        if str(ctx.author.id) in played_list:
            logging.info('遊んだ人リストに ID があるため中断')
            await sd.send_uranai_played(ctx)
            logging.info('もだねちゃん占いを終了')
            return

        # 運勢占い処理
        random.shuffle(fortune_list)
        logging.info('運勢 3つを決定: %s, %s, %s', fortune_list[0], fortune_list[1], fortune_list[2])

        # 運勢用の星を算出してリストに格納
        star_result_list = random.choices(star_list, k=3, weights=[4, 15, 50, 25, 4, 2])
        star_result_list.sort(reverse=True)
        logging.info('運勢の星を決定: %s, %s, %s', star_result_list[0], star_result_list[1], star_result_list[2])

        # ラッキーアイテム占い処理
        lucky_num = random.randint(0, len(lucky_list)-1)
        lucky_value = lucky_list[lucky_num]
        logging.info('ラッキーアイテムを決定: %s', lucky_value)

        logging.info('結果を送信')
        # メッセージ送信
        await sd.send_uranai_result(ctx, fortune_list, star_result_list, lucky_value)

        # played_fortune_users テーブルへユーザーIDを格納する
        logging.info('played_fortune_users テーブルへ ユーザーID を格納')
        user_id = ctx.author.id
        psql.do_query('./sql/uranai/insert_user_id.sql', {'user_id': user_id})

        logging.info('もだねちゃん占いを終了')

async def setup(bot):
    await bot.add_cog(Uranai(bot))
