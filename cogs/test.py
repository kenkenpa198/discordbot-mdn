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
                cur.execute('CREATE DATABASE mydb;')
            conn.commit()

        print('--- 実行完了 ---')

    # テーブルを作成する
    async def tbl(self, ctx):
        print('===== テーブルを作成します =====')
        with psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('CREATE TABLE sample (id serial PRIMARY KEY, name varchar, num integer);')
            conn.commit()

        print('--- 実行完了 ---')

    # レコードを追加する
    @commands.command()
    async def add(self, ctx):
        print('===== レコードを追加します =====')
        with psql.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO sample VALUES (1, kem198, 1)')
            conn.commit()

        print('--- 実行完了 ---')

    # 抽出
    @commands.command()
    async def slt(self, ctx):
        print('===== ###を開始します =====')
        conn = psql.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        cur.close()
        conn.close()
        print('--- ###の実行 ---')
        pass


def setup(bot):
    bot.add_cog(Test(bot))