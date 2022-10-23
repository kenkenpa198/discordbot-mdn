-- データベースの切り替え
\c discordbot_mdn_db

-- 読み上げチャンネルテーブルの作成
CREATE TABLE talk_channels (
    guild_id   CHAR(18) NOT NULL,
    vc_id      CHAR(18) NOT NULL,
    channel_id CHAR(18) NOT NULL,
    updated_at timestamp without time zone NOT NULL,

    PRIMARY KEY (guild_id)
);

-- 占い済みユーザーテーブルの作成
CREATE TABLE played_fortune_users (
    user_id CHAR(18) NOT NULL,
    updated_at timestamp without time zone NOT NULL,

    PRIMARY KEY (user_id)
);
