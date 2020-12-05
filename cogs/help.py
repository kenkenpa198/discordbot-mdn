from discord.ext import commands
import discord


##### コグ #####
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['h'])
    async def help(self, ctx):
        print('===== もだねちゃんヘルプを表示します =====')
        embed = discord.Embed(title='もだねちゃんヘルプ', description='もだねちゃんのお仕事コマンド一覧だよ！\nもっと詳しい操作方法は[ 📙 ガイドブック ](https://github.com/kenkenpa198/discordbot-mdn/blob/master/README.md)を確認してみてね！', color=0xffd6e9)

        help_talk = f'ㅤ\n\n■ 読み上げコマンド'
        mdn_s = f'ㅤ\n🎤 読み上げを開始する```!mdn s```'
        mdn_c = f'ㅤ\n🎤 読み上げ対象のテキストチャンネルを再設定する```!mdn c```'
        mdn_e = f'ㅤ\n🎤 読み上げを終了する```!mdn e```'
        embed.add_field(name=help_talk, value=mdn_s + mdn_c + mdn_e, inline=False)

        help_ohter = f'ㅤ\n■ その他'
        mdn_j = f'ㅤ\n✌️ ジャンケンで遊ぶ```!mdn j```'
        mdn_u = f'ㅤ\n🔮 もだねちゃん占い```!mdn u```'
        mdn_h = f'ㅤ\n❓ ヘルプを表示する```!mdn h```'
        embed.add_field(name=help_ohter, value=mdn_j + mdn_u + mdn_h, inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))