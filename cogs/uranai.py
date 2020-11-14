# coding: utf-8
import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import random
from datetime import datetime


##### 占い用リスト・辞書 #####
# 運勢結果リスト
unsei_list = [
    '🕺 友達運',
    '💞 恋愛運',
    '🎮 ゲーム運',
    '💰 金運',
    '📝 勉強運',
    '💪 健康運',
    '🌈 お天気運'
]

# 運勢結果リスト
star_list = [
    '★',
    '★★',
    '★★',
    '★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★★',
    '★★★★',
    '★★★★',
    '★★★★',
    '★★★★★'
]

# ラッキーアイテムリスト
lucky_list = [
    '🍎 赤色',
    '🎇 橙色',
    '🍋 黄色',
    '📗 緑色',
    '🐳 青色',
    '🔮 紫色',
    ':black_cat: 黒色',
    '🐑 白色',
    '🍞 パン',
    '🍚 お米',
    '🍖 お肉',
    '🐟 お魚',
    '🥬 野菜',
    '🍓 果物',
    '💊 お薬',
    '🍫 チョコレート',
    '🍬 アメ',
    '🥤 ジュース',
    '🍵 お茶',
    '🐱 どうぶつ',
    '🎮 ゲーム',
    '👜 カバン',
    '🖋 ペン',
    '🎧 音楽',
    '👛 お財布',
    '💬 Discord',
    '💻 機械',
    '👕 シャツ',
    '🚃 乗り物',
    '🤝 人助け',
    '🌇 夕焼け'
    ]

# 遊んだ人リストを定義
played_list = []

# played_list の中身を削除する関数を定義
def clear_played_list():
    played_list.clear()
    print('===== 遊んだ人リストの中身を削除しました =====')


##### コグ #####
class Uranai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 指定日時に遊んだ人リストの中身を削除する
    @tasks.loop(seconds=60)
    async def loop():
        # 現在の時刻
        now = datetime.now().strftime('%H:%M')
        if now == '00:00':
            clear_played_list()
    # ループ処理を実行
    loop.start()

    # もだねちゃん占い
    @commands.command(aliases=['u'])
    async def uranai(self, ctx):
        print('===== もだねちゃん占いを開始します =====')

        # played_list にユーザーIDがあるか判定
        if ctx.author.id in played_list:
            print('--- 遊んだ人リストにIDがあるため中断 ---')
            embed = discord.Embed(title='もだねちゃん占いは 1日1回までだよ',description=f'{ctx.author.name}さんの運勢はもう占っちゃった！\nまた明日遊んでね！', color=0xeaa55c)
            await ctx.send(embed=embed)
            print('===== もだねちゃん占いを終了します =====')
            return

        # 運勢占い処理
        random.shuffle(unsei_list)
        print('運勢1：' + unsei_list[0])
        print('運勢2：' + unsei_list[1])
        print('運勢3：' + unsei_list[2])

        star_num_list = []
        star_num_list.append(random.randint(0,len(star_list)-1))
        star_num_list.append(random.randint(0,len(star_list)-1))
        star_num_list.append(random.randint(0,len(star_list)-1))
        print(star_num_list)
        star_num_list.sort(reverse=True)
        print(star_num_list)
        unsei_value_1 = star_list[star_num_list[0]]
        unsei_value_2 = star_list[star_num_list[1]]
        unsei_value_3 = star_list[star_num_list[2]]

        # ラッキーアイテム占い処理
        lucky_num = random.randint(0,len(lucky_list)-1)
        lucky_value = lucky_list[lucky_num]
        print('ラッキーアイテム：' + lucky_value)

        # メッセージ送信
        embed = discord.Embed(title='もだねちゃん占い', description=f'{ctx.author.name}さんの今日の運勢だよ！', color=0xf1bedf)
        embed.add_field(name='ㅤ\n' + unsei_list[0], value=unsei_value_1)
        embed.add_field(name='ㅤ\n' + unsei_list[1], value=unsei_value_2)
        embed.add_field(name='ㅤ\n' + unsei_list[2], value=unsei_value_3)
        embed.add_field(name='ㅤ\nラッキーアイテム', value=lucky_value)

        await ctx.send(embed=embed)
        await asyncio.sleep(1)
        async with ctx.channel.typing():
            await asyncio.sleep(.5)
        await ctx.send(f'結果はどうだった？またねー！')

        # 遊んだ人リストへユーザーIDを格納
        played_list.append(ctx.author.id)
        print(played_list)

        print('===== もだねちゃん占いを終了します =====')


def setup(bot):
    bot.add_cog(Uranai(bot))