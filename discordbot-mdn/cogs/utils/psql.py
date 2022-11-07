"""PostgreSQL modules"""

import logging
import os

import psycopg2


def get_connection():
    """
    データベースへ接続する

    Returns
    -------
    con : psycopg2.extensions.connection
        PostgreSQL への接続情報を持ったオブジェクト
    """
    logging.info('データベースへ接続')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    return psycopg2.connect(DATABASE_URL)

def get_query(query_file_path):
    """
    SQL クエリを外部ファイルから読み込む

    Parameters
    ----------
    query_file_path : str
        読み込み対象とする SQL クエリのファイルパス

    Returns
    -------
    query : str
        読み込んだ SQL 文
    """
    with open(query_file_path, 'r', encoding='utf-8') as f:
        query = f.read()

    logging.info('クエリを読み込み: %s', query_file_path)
    logging.debug('取得したクエリ:\n%s', query)

    return query

def do_query(query_file_path, bind_dict=None):
    """
    SQL クエリを実行する

    Parameters
    ----------
    query_file_path : str
        読み込み対象とする SQL クエリのファイルパス
    bind_dict : dict
        SQL 文内のバインド変数を置き換える文字列を辞書形式で記述

    Notes
    -----
    プレースホルダが記述されたクエリを指定する場合、引数2つ目にバインド変数を辞書形式で記述する。
    プレースホルダが記述されていない場合、バインド変数は省略できる。

    Examples
    --------
    >>> do_query('./sql/uranai/delete_user_id.sql')
    >>> do_query('./sql/uranai/insert_user_id.sql', {'user_id': user_id})
    >>> do_query(
            './sql/talk/upsert_target_id.sql',
            {'guild_id': guild_id, 'vc_id': vc_id, 'channel_id': channel_id}
        )
    """
    # 引数が与えられなかったら空の辞書で初期化
    if bind_dict is None:
        bind_dict = {}

    # 実行する SQL 文を取得
    query = get_query(query_file_path)
    logging.debug('実行するクエリ:\n%s', query % bind_dict)

    # クエリを実行
    with get_connection() as conn:
        with conn.cursor() as cur:
            logging.info('クエリを実行')
            cur.execute(query % bind_dict)
        conn.commit()

def do_query_fetch_one(query_file_path, bind_dict=None):
    """
    SQL クエリを実行し結果1つを取得する

    Parameters
    ----------
    query_file_path : str
        読み込み対象とする SQL クエリのファイルパス
    bind_dict : dict
        SQL 文内のバインド変数を置き換える文字列を辞書形式で記述

    Returns
    -------
    result : str
        SELECT された結果
    """
    # 引数が与えられなかったら空の辞書で初期化
    if bind_dict is None:
        bind_dict = {}

    # 実行する SQL 文を取得
    query = get_query(query_file_path)
    logging.debug('実行するクエリ:\n%s', query % bind_dict)

    # クエリを実行
    with get_connection() as conn:
        with conn.cursor() as cur:
            logging.info('クエリを実行')
            cur.execute(query % bind_dict)
            # 結果から1件のみを取得し1つ目のみを保持
            (result,) = cur.fetchone()
        conn.commit()
    return result

def do_query_fetch_list(query_file_path, bind_dict=None):
    """
    SQL クエリを実行し行をリストで返す

    Parameters
    ----------
    query_file_path : str
        読み込み対象とする SQL クエリのファイルパス
    bind_dict : dict
        SQL 文内のバインド変数を置き換える文字列を辞書形式で記述

    Returns
    -------
    result_list : list
        SELECT された結果のリスト
    """
    # 引数が与えられなかったら空の辞書で初期化
    if bind_dict is None:
        bind_dict = {}

    # 実行する SQL 文を取得
    query = get_query(query_file_path)
    logging.debug('実行するクエリ:\n%s', query % bind_dict)

    # クエリを実行
    with get_connection() as conn:
        with conn.cursor() as cur:
            logging.info('クエリを実行')
            cur.execute(query % bind_dict)
            # リストを作成して行を順番に代入
            result_list = []
            for row in cur:
                result_list.append(str(row[0]))
        conn.commit()
    return result_list
