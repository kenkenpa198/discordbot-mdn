"""Cog Uranai"""

from datetime import datetime
import logging
import random

from discord.ext import commands
from discord.ext import tasks

from .utils import psql
from .utils import send as sd

##### 占い用リストの読み込み #####
# 運勢リスト
with open('./csv/fortune_list.csv', 'r', encoding='utf-8') as f:
    fortune_list = [s.strip() for s in f.readlines()]
# print(fortune_list)

# 運勢の星リスト
star_list = ['★', '★★', '★★★', '★★★★', '★★★★★', '⭐️⭐️⭐️⭐️⭐️⭐️']

# ラッキーアイテムリスト
with open('./csv/lucky_list.csv', 'r', encoding='utf-8') as f:
    lucky_list = [s.strip() for s in f.readlines()]
# print(lucky_list)


##### コグ #####
class Uranai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=60)
    async def loop():
        """
        毎日0時にレコードを削除する
        """
        now = datetime.now().strftime('%H:%M')
        if now == '00:00':
            logging.info('played_fortune_users テーブルのレコードを削除')
            psql.do_query('./sql/uranai/delete_user_id.sql')
    # ループ処理を実行
    loop.start()

    @commands.hybrid_command(aliases=['u'], description='今日の運勢を占うよ')
    async def uranai(self, ctx):
        """
        占いコマンド
        """
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
