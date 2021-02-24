##### PostgreSQL 操作用モジュール #####
import os
from os.path import join, dirname

import psycopg2


# DB 接続
def get_connection():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# SQL クエリ読込
def get_query(query_file_path):
    with open(query_file_path, 'r') as f:
        query = f.read()
    return query

# SQL クエリ実行
# 引数2つ目にはバインド変数を指定
# バインド変数は省略可能
def run_query(query_file_path, bind_var={}):
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = get_query(query_file_path)
            cur.execute(query % bind_var)
        conn.commit()

# SQL クエリを実行し、結果1つを返す
def run_query_to_var(query_file_path, bind_var={}):
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = get_query(query_file_path)
            cur.execute(query % bind_var)
            # 実行結果を変数へ格納
            (output,) = cur.fetchone()
        conn.commit()
    return output

# SQL クエリを実行し、行をリストの形式で返す
def run_query_to_list(query_file_path, bind_var={}):
    output_list = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = get_query(query_file_path)
            cur.execute(query % bind_var)
            # リストへ格納
            for row in cur:
                output_list.append(str(row[0])) # 取得したレコードをリストへ変換
        conn.commit()
    return output_list