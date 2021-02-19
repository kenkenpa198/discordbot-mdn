# coding: utf-8
import discord
from discord.ext import commands
import asyncio
from .utils import psql


##### 関数の定義 #####


##### コグ #####
class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ロールバック
    @commands.command()
    async def roll(self, ctx):
        print('===== ロールバックします =====')
        with psql.get_connection() as conn:
            conn.rollback()

        print('--- 実行完了 ---')

    # データベースを作成する
    @commands.command()
    async def db(self, ctx):
        print('===== DBを追加します =====')
        with psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE DATABASE mydb;")
            conn.commit()

        print('--- 実行完了 ---')

    # テーブルを作成する
    async def cretb(self, ctx):
        print('===== テーブルを作成します =====')
        with psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE test_tb (id serial PRIMARY KEY,user_id TEXT NOT NULL,display_name TEXT NOT NULL);")
            conn.commit()

        print('--- 実行完了 ---')

    # レコードを追加する
    @commands.command()
    async def add(self, ctx):
        print('===== レコードを追加します =====')
        with psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO test_tb(user_id, display_name) VALUES ('abc123', 'taro');")
            conn.commit()

        print('--- 実行完了 ---')

    # 抽出
    @commands.command()
    async def sel(self, ctx):
        print('===== レコードを抽出します =====')
        with psql.get_connection() as conn:
            with conn.cursor() as cur:
                record = cur.execute("SELECT * FROM test_tb;")
            conn.commit()

        print(record)
        print('--- 実行完了 ---')

    # 抽出
    # @commands.command()
    # async def sel(self, ctx):
    #     print('===== レコードを抽出します =====')
    #     conn = psql.get_connection()
    #     cur = conn.cursor()
    #     cur.execute('SELECT * FROM users')
    #     cur.close()
    #     conn.close()
    #     print('--- ###の実行 ---')
    #     pass


def setup(bot):
    bot.add_cog(Test(bot))