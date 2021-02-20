##### PostgreSQL 操作用モジュール #####
import os
from os.path import join, dirname
import psycopg2


# DB 接続用関数
def get_connection():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# SQL クエリ読込
def get_query(query_file_path):
    with open(query_file_path, 'r') as f:
        query = f.read()
    return query

# SQL クエリ読込 -> 実行
def run_query(query_file_path):
    with psql.get_connection() as conn:
        with conn.cursor() as cur:
            query = get_query(query_file_path)
            cur.execute(query)
        conn.commit()