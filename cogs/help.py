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

        help_name    = f'ㅤ\n🎤 読み上げ機能'
        help_value_1 = f'ㅤ- 読み上げを開始する```!mdn s```'
        help_value_2 = f'ㅤ\nㅤ- 読み上げ対象のテキストチャンネルを再設定する```!mdn c```'
        help_value_3 = f'ㅤ\nㅤ- 読み上げを終了する```!mdn e```'
        embed.add_field(name=help_name, value=help_value_1 + help_value_2 + help_value_3, inline=False)

        help_name    = f'ㅤ\n✌️ジャンケンで遊ぶ'
        help_value_1 = f'```!mdn j```'
        embed.add_field(name=help_name, value=help_value_1, inline=False)

        help_name    = f'ㅤ\n🔮 もだねちゃん占い'
        help_value_1 = f'```!mdn u```'
        embed.add_field(name=help_name, value=help_value_1, inline=False)

        help_name    = f'ㅤ\n❓ ヘルプを表示する'
        help_value_1 = f'```!mdn h```'
        embed.add_field(name=help_name, value=help_value_1, inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))