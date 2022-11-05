'''Cog Janken'''

import asyncio
import random

import discord
from discord.ext import commands


##### コグ #####
class Janken(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # もだねちゃんとジャンケンをする
    @commands.hybrid_command(aliases=['j'], description='ジャンケンで遊べるよ')
    async def janken(self, ctx):
        print('===== ジャンケンを開始します =====')

        # wait_for に渡すリアクションの種別を判定するチェック関数を定義
        def janken_check(reaction, user):
            # リアクションの送信ユーザーを判定
            user_ok = (user == ctx.author)
            # リアクションの種別を判定
            reaction_ok = (reaction.emoji == '✊' or reaction.emoji == '✌️' or reaction.emoji == '🖐')
            return user_ok and reaction_ok

        # プレイヤーとコンピュータの手を比較してアイコの判定を戻り値として返す関数
        def judge_aiko(player, computer):
            if player == computer:
                print('勝敗: アイコ')
                print('繰り返します')
                return 'アイコだ！さあ、もう一回！'

        # プレイヤーとコンピュータの手を比較して勝敗を戻り値として返す関数
        def judge(player, computer):
            if player == 0 and computer == 1:
                print('勝敗: プレイヤーの勝ち')
                return 'わっ！負けちゃった！', f'{ctx.author.display_name}さん', ctx.author.display_avatar
            elif player == 1 and computer == 2:
                print('勝敗: プレイヤーの勝ち')
                return 'あー！完敗だ！', f'{ctx.author.display_name}さん', ctx.author.display_avatar
            elif player == 2 and computer == 0:
                print('勝敗: プレイヤーの勝ち')
                return 'うーっ！私の負け…！', f'{ctx.author.display_name}さん', ctx.author.display_avatar
            else:
                print('勝敗: コンピュータの勝ち')
                return 'やったー！わたしの勝ち！', f'{self.bot.user.display_name}', self.bot.user.display_avatar

        # 入力されたリストの番号（0, 1, 2）を受け取り、番号に対応した手を出力する
        def rise_hand(hand):
            hands = ['✊ グー！', '✌️ チョキ！', '🖐 パー！']
            return hands[hand]


        # ジャンケンの実行
        await ctx.send(f'{ctx.author.mention}\nジャンケンだね！負けないよ！')
        await asyncio.sleep(1)
        await ctx.send('じゃあいくよっ！さいしょはグー！')

        # TODO: 以下処理について後半にも全く同じ処理があるので、この処理を関数化する
        embed = discord.Embed(title='ジャンケン……', description='出したい手のリアクションを押してね。', color=0xffd6e9)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('✊')
        await msg.add_reaction('✌️')
        await msg.add_reaction('🖐')

        # プレイヤーとコンピューターの手を入れる変数を定義（初期値はアイコ）
        player_hand = 0
        computer_hand = 0

        while player_hand == computer_hand:
            # リアクションを押されるまで待機
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=janken_check, timeout=20)
            except asyncio.TimeoutError:
                embed = discord.Embed(title='ジャンケンを中断したよ', description='さいしょはグーのポーズをずっとするの疲れちゃった！\n出したい手は20秒以内に選んでね！', color=0xffab6f)
                await ctx.send(embed=embed)
                print('===== ジャンケンを中断しました =====')
                return
            else:
                pass

            async with ctx.channel.typing():
                # プレイヤーの手を算出して変数に格納
                await asyncio.sleep(.5)
                if reaction.emoji == '✊':
                    player_hand = 0
                elif reaction.emoji == '✌️':
                    player_hand = 1
                else:
                    player_hand = 2
                print('プレイヤーの手: ' + str(player_hand))

                # コンピュータの手を算出して変数に格納
                # グー: 30% チョキ: 40% パー: 30%
                computer_hand_rdm = random.randint(1, 100)
                print('computer_hand_rdm: ' + str(computer_hand_rdm))
                if 1 <= computer_hand_rdm <= 30:
                    computer_hand = 0
                elif 31 <= computer_hand_rdm <= 70:
                    computer_hand = 1
                else:
                    computer_hand = 2
                print('コンピュータの手: ' + str(computer_hand))

            # お互いの手を表示する
            embed = discord.Embed(title='ぽんっ！', color=0xffd6e9)
            embed.add_field(name='もだねちゃんの手', value=rise_hand(computer_hand), inline=False)
            embed.add_field(name=f'ㅤ\n{ctx.author.display_name}さんの手', value=rise_hand(player_hand), inline=False)
            await ctx.send(embed=embed)

            # アイコだったらメッセージを送信してもう一回繰り返す
            if player_hand == computer_hand:
                await asyncio.sleep(1)
                async with ctx.channel.typing():
                    await asyncio.sleep(.5)
                result_msg = judge_aiko(player_hand, computer_hand)
                await ctx.send(result_msg)

                # ジャンケンスタート
                embed = discord.Embed(title='ジャンケン……', description='出したい手のリアクションを押してね', color=0xffd6e9)
                msg = await ctx.send(embed=embed)
                await msg.add_reaction('✊')
                await msg.add_reaction('✌️')
                await msg.add_reaction('🖐')
            else:
                break # 勝敗が決まった場合whileを抜ける

        # 勝敗の結果を表示する
        await asyncio.sleep(1.5)
        result_msg, result_winner, result_winner_img = judge(player_hand, computer_hand)
        embed = discord.Embed(title='勝者は……', description=f'🎉 {result_winner}！', color=0xffd6e9)
        embed.set_thumbnail(url=result_winner_img)
        await ctx.send(embed=embed)
        await asyncio.sleep(2)
        async with ctx.channel.typing():
            await asyncio.sleep(.5)
        await ctx.send(result_msg + '\n\n楽しかった〜！またやろうね！')
        print('===== ジャンケンを終了します =====')

async def setup(bot):
    await bot.add_cog(Janken(bot))
