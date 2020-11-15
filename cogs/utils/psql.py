##### PostgreSQL 操作用モジュール #####
# coding: utf-8
import os
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2


##### 関数の定義 #####
# DB接続用関数
def get_connection():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    return psycopg2.connect(DATABASE_URL)