#!/bin/sh

# デバッグ情報を出力
set -x

# psql の実行コマンドを定義
psql_cmd="psql -U $POSTGRES_USER $POSTGRES_DB"

# 読み上げチャンネルテーブルの作成
$psql_cmd -c "\
CREATE TABLE talk_channels (
    guild_id   CHAR(19) NOT NULL,
    vc_id      CHAR(19) NOT NULL,
    channel_id CHAR(19) NOT NULL,
    updated_at timestamp without time zone NOT NULL,

    PRIMARY KEY (guild_id)
);\
"

# 占い済みユーザーテーブルの作成
$psql_cmd -c "\
CREATE TABLE played_fortune_users (
    user_id CHAR(19) NOT NULL,
    updated_at timestamp without time zone NOT NULL,

    PRIMARY KEY (user_id)
);\
"
