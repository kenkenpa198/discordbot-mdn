##### PostgreSQL 操作用モジュール #####
# coding: utf-8
import os
from os.path import join, dirname
import psycopg2


##### 関数の定義 #####
# DB 接続用関数
def get_connection():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    return psycopg2.connect(DATABASE_URL, sslmode='require')