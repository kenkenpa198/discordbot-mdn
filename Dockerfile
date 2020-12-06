# Docker image を pull
FROM emptypage/open_jtalk:20.4_1.11

# 実行環境の構築
RUN set -x && \
    apt-get update -y && \
    # Ubuntu 版 pip / Opus ライブラリのインストール
    apt-get install -y python3-pip libopus-dev && \
    # アーカイブファイルの削除
    apt-get clean -y && rm -rf /var/lib/apt/lists/* && \
    # pip パッケージのインストール
    pip3 install jtalkbot==0.5.0 && \
    pip3 install discord.py==1.5.1

# discordbot-mdn の構築
RUN set -x && \
    mkdir /discordbot-mdn && \
    mkdir /discordbot-mdn/cogs && \
    mkdir -p /usr/local/Cellar/open-jtalk/1.11 && \
    # シンボリックリンクの作成
    ln -s /usr/local/lib/open_jtalk/dic /usr/local/Cellar/open-jtalk/1.11 && \
    ln -s /usr/local/lib/open_jtalk/voice /usr/local/Cellar/open-jtalk/1.11
WORKDIR /discordbot-mdn
COPY mdn.py /discordbot-mdn
COPY cogs/ /discordbot-mdn/cogs/

# docker-compose.yml / heroku.yml から渡された環境変数の読み込み
ARG TZ
ENV HOME=/${TZ}
ARG BOT_TOKEN
ENV HOME=/${BOT_TOKEN}