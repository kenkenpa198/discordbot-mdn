from discord.ext import commands
import discord


##### コグ #####
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['h'])
    async def help(self, ctx):
        print('===== もだねちゃんヘルプを表示します =====')
        embed = discord.Embed(title='もだねちゃんヘルプ', description='もだねちゃんのお仕事コマンド一覧だよ！\nもっと詳しい操作方法は[ 📙 ガイドブック ](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック)を確認してみてね！', color=0xffd6e9)
        await ctx.send(embed=embed)

        embed = discord.Embed(title='読み上げ機能', color=0xffd6e9)

        help_name  = f'🎤 読み上げを開始する'
        help_value = f'```!mdn s```'
        embed.add_field(name=help_name, value=help_value, inline=False)

        help_name  = f'ㅤ\n🎤 読み上げを終了する'
        help_value = f'```!mdn e```'
        embed.add_field(name=help_name, value=help_value, inline=False)

        embed.set_footer(text='ㅤ\nヒント：\nもだねちゃんがボイスチャンネルにいる状態で「!mdn s」を送信すると、読み上げ対象チャンネルを再設定できます。\n読み上げたいチャンネルを変更したい時にご利用ください。')
        await ctx.send(embed=embed)

        embed = discord.Embed(title='その他の機能', color=0xffd6e9)
        help_name  = f'✌️ジャンケンで遊ぶ'
        help_value = f'```!mdn j```'
        embed.add_field(name=help_name, value=help_value, inline=False)

        help_name  = f'ㅤ\n🔮 もだねちゃん占い'
        help_value = f'```!mdn u```'
        embed.add_field(name=help_name, value=help_value, inline=False)

        help_name  = f'ㅤ\n❓ ヘルプを表示する'
        help_value = f'```!mdn h```'
        embed.add_field(name=help_name, value=help_value, inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))