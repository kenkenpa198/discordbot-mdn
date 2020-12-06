import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import random
from datetime import datetime


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
    '⚽️ スポーツ運'
]

# 運勢結果リスト
star_list = [
    '★',
    '★★',
    '★★',
    '★★',
    '★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★',
    '★★★★',
    '★★★★',
    '★★★★',
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
    '🌌 夜空'
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
            embed = discord.Embed(title='もだねちゃん占いは 1日1回までだよ',description=f'{ctx.author.display_name}さんの運勢はもう占っちゃった！\nまた明日遊んでね！', color=0xffab6f)
            await ctx.send(embed=embed)
            print('===== もだねちゃん占いを終了します =====')
            return

        # 運勢占い処理
        print('--- 運勢 3つを決定 ---')
        random.shuffle(fortune_list)

        print(fortune_list)
        for i in range(3):
            print('運勢 ' + str(i) + '：' + fortune_list[i])

        star_num_list = []
        for i in range(3):
            star_num_list.append(random.randint(0,len(star_list)-1))
        print('ソート前：' + str(star_num_list))
        star_num_list.sort(reverse=True)
        print('ソート後：' + str(star_num_list))

        # ラッキーアイテム占い処理
        print('--- ラッキーアイテムを決定 ---')
        lucky_num = random.randint(0,len(lucky_list)-1)
        lucky_value = lucky_list[lucky_num]
        print('ラッキーアイテム：' + lucky_value)

        print('===== 結果を送信します =====')
        # メッセージ送信
        embed = discord.Embed(title='もだねちゃん占い', description=f'{ctx.author.display_name}さんの今日の運勢だよ！', color=0xffd6e9)
        embed.add_field(name='ㅤ\n' + fortune_list[0], value=star_list[star_num_list[0]])
        embed.add_field(name='ㅤ\n' + fortune_list[1], value=star_list[star_num_list[1]])
        embed.add_field(name='ㅤ\n' + fortune_list[2], value=star_list[star_num_list[2]])
        embed.add_field(name='ㅤ\nラッキーアイテム', value=lucky_value)

        await ctx.send(embed=embed)
        await asyncio.sleep(1)
        async with ctx.channel.typing():
            await asyncio.sleep(.5)
        await ctx.send(f'結果はどうだった？またねー！')

        # 遊んだ人リストへユーザーIDを格納
        print('--- 遊んだ人リストへ ユーザーID を格納 ---')
        played_list.append(ctx.author.id)
        print('遊んだ人リスト：' + str(played_list))

        print('===== もだねちゃん占いを終了します =====')


def setup(bot):
    bot.add_cog(Uranai(bot))