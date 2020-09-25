# coding: utf-8
import discord
from discord.ext import commands
import random
import asyncio
import utils


class Janken(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## もだねちゃんとジャンケンをする
    @commands.command()
    async def j(self, ctx):
        print('===== ジャンケンを開始します =====')
        # ジャンケンの説明文
        janken_list = ':fist:：0　:v:：1　:hand_splayed:：2'

        # ジャンケンの実行
        await ctx.send(f'{ctx.author.mention}\nジャンケンだね！負けないよ！')
        await asyncio.sleep(1)
        await ctx.send(f'{ctx.author.mention}\nじゃあいくよっ！\nさいしょはグー！ジャンケン……')
        embed = discord.Embed(title='出したい手を数字で入力してね', description=str(janken_list), color=0xff7777)
        await ctx.send(embed=embed)

        # while文で使う変数と関数を定義
        # プレイヤーとコンピューターの手を入れる変数を定義
        player_hand = 0
        computer_hand = 0

        while player_hand == computer_hand:
            # プレイヤーが送信したメッセージをチェック用関数でチェックする    
            # 0, 1, 2 のどれかだったらOK それら意外であれば待機
            wait_message = await self.bot.wait_for('message', check=utils.janken_check) #メッセージを変数へ格納する

            # プレイヤーの手を算出
            player_hand = int(wait_message.content) #返答をint型へ変換し変数へ格納する
            print('プレイヤーの手：' + str(player_hand)) # プレイヤーの手を出力

            # コンピュータの手を算出
            computer_hand = random.randint(0, 2) # randintを用いて0から2までの数値を取得し、変数computer_handに代入
            print('コンピュータの手：' + str(computer_hand)) # コンピュータの手を出力

            # 出した手の表示
            await ctx.send(f'{ctx.author.mention}\nぽんっ！')
            embed = discord.Embed(color=0xff7777)
            embed.add_field(name=str(ctx.author.name) + 'さんが出した手', value=utils.rise_hand(player_hand), inline=False)
            embed.add_field(name='ㅤ\nもだねちゃんが出した手', value=utils.rise_hand(computer_hand), inline=False)
            await ctx.send(embed=embed)

            # アイコだったらメッセージを送信してもう一回
            if player_hand == computer_hand:
                await asyncio.sleep(1.5)
                result = utils.judge_aiko(player_hand, computer_hand)
                await ctx.send(f'{ctx.author.mention}\n' + result)
                embed = discord.Embed(title='出したい手を数字で入力してね', description=str(janken_list), color=0xff7777)
                await ctx.send(embed=embed)
            else:
                break #勝敗が決まった場合whileを抜ける

        # 勝敗の結果を表示して終了
        await asyncio.sleep(1.5)
        result = utils.judge(player_hand, computer_hand)
        await ctx.send(f'{ctx.author.mention}\n' + result + '\n\n楽しかった〜！またやろうね！')
        print('===== ジャンケンを終了します =====')

def setup(bot):
    bot.add_cog(Janken(bot))