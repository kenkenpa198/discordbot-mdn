# coding: utf-8
import discord
from discord.ext import commands
import asyncio
import random


##### コグ #####
class Janken(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ## もだねちゃんとジャンケンをする
    @commands.command(aliases=['j'])
    async def janken(self, ctx):
        print('===== ジャンケンを開始します =====')

        ##ジャンケン用関数を定義
        # wait_for に渡すチェック関数を定義
        def janken_check(reaction, user):
            # リアクションの送信ユーザーを判定
            user_ok = (user == ctx.author)
            # リアクションの種別を判定
            reaction_ok = (reaction.emoji == '✊' or reaction.emoji == '✌️' or reaction.emoji == '🖐')
            return user_ok and reaction_ok

        # プレイヤーとコンピュータの手を比較してアイコの判定を戻り値として返す
        def judge_aiko(player, computer):
            if player == computer:
                print('勝敗：アイコ')
                print('--- 繰り返します ---')
                return 'アイコだ！さあ、もう一回！'

        # プレイヤーとコンピュータの手を比較して勝敗を戻り値として返す
        def judge(player, computer):
            if player == 0 and computer == 1:
                print('勝敗：プレイヤーの勝ち')
                return 'わっ！負けちゃった！', f'{ctx.author.name}さん', ctx.author.avatar_url
            elif player == 1 and computer == 2:
                print('勝敗：プレイヤーの勝ち')
                return 'あー！完敗だ！', f'{ctx.author.name}さん', ctx.author.avatar_url
            elif player == 2 and computer == 0:
                print('勝敗：プレイヤーの勝ち')
                return 'うーっ！私の負け…！', f'{ctx.author.name}さん', ctx.author.avatar_url
            else:
                print('勝敗：コンピュータの勝ち')
                return 'やったー！わたしの勝ち！', 'もだねちゃん', self.bot.user.avatar_url
        
        # 入力されたリストの番号（0, 1, 2）を受け取り、番号に対応した手を出力する
        def rise_hand(hand):
            hands = ['✊ グー！', '✌️ チョキ！', '🖐 パー！'] # 0:グー 1:チョキ 2:パー
            return hands[hand]


        # ジャンケンの実行
        await ctx.send(f'{ctx.author.mention}\nジャンケンだね！負けないよ！')
        await asyncio.sleep(1)
        
        # ジャンケンスタート
        await ctx.send(f'じゃあいくよっ！さいしょはグー！')
        embed = discord.Embed(title='ジャンケン……', description='出したい手のリアクションを押してね。', color=0xffd6e9)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('✊')
        await msg.add_reaction('✌️')
        await msg.add_reaction('🖐')


        # while文で使う変数と関数を定義
        # プレイヤーとコンピューターの手を入れる変数を定義
        player_hand = 0
        computer_hand = 0

        while player_hand == computer_hand:
            
            # 20秒まで待機
            # プレイヤーが送信したメッセージをチェック用関数でチェックする    
            # 0, 1, 2 のどれかだったらOK それら意外であれば待機
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
                await asyncio.sleep(.5)
                # プレイヤーの手を算出
                if reaction.emoji == '✊':
                    player_hand = 0
                elif reaction.emoji == '✌️':
                    player_hand = 1
                else:
                    player_hand = 2

                print('プレイヤーの手：' + str(player_hand)) # プレイヤーの手を出力

                # コンピュータの手を算出
                computer_hand_rdm = random.randint(1, 100) # randintを用いて1から100までの数値を取得し、変数computer_hand_numに代入
                print('computer_hand_rdm：' + str(computer_hand_rdm))

                # computer_hand へジャンケンの手に対応した 0, 1, 2 を格納する
                # 1 - 30：グー / 31 - 70：チョキ / 71 - 100：パー
                if 1 <= computer_hand_rdm <= 30:
                    computer_hand = 0
                elif 31 <= computer_hand_rdm <= 70:
                    computer_hand = 1
                else:
                    computer_hand = 2
                
                print('コンピュータの手：' + str(computer_hand)) # コンピュータの手を出力

            # 出した手の表示
            embed = discord.Embed(title='ぽんっ！', color=0xffd6e9)
            embed.add_field(name='もだねちゃんの手', value=rise_hand(computer_hand), inline=False)
            embed.add_field(name=f'ㅤ\n{ctx.author.name}さんの手', value=rise_hand(player_hand), inline=False)
            await ctx.send(embed=embed)

            # アイコだったらメッセージを送信してもう一回
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
                break #勝敗が決まった場合whileを抜ける

        # 勝敗の結果を表示して終了
        await asyncio.sleep(1.5)
        
        result_msg, result_winner, result_winner_img = judge(player_hand, computer_hand)
        embed = discord.Embed(title='勝者は…', description=f'🎉 {result_winner}！', color=0xffd6e9)
        embed.set_thumbnail(url=result_winner_img)
        await ctx.send(embed=embed)
        await asyncio.sleep(2)
        async with ctx.channel.typing():
            await asyncio.sleep(.5)
        await ctx.send(result_msg + f'\n\n楽しかった〜！またやろうね！')
        print('===== ジャンケンを終了します =====')


def setup(bot):
    bot.add_cog(Janken(bot))