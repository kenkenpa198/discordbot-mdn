# Docker image を pull
FROM emptypage/open_jtalk:20.4_1.11

# 実行環境の構築
RUN set -x && \
    apt-get update -y && \
    # tz database のインストール（タイムゾーンの自動設定のため）
    apt-get install -y tzdata && \
    # Ubuntu 版 pip のインストール
    apt-get install -y python3-pip && \
    # 読み上げ機能用ソフトのインストール
    apt-get install -y libopus-dev ffmpeg alsa && \
    # アーカイブファイルの削除
    apt-get clean -y && rm -rf /var/lib/apt/lists/*

# discordbot-mdn ディレクトリの構築
RUN set -x && \
    mkdir /discordbot-mdn && \
    mkdir /discordbot-mdn/cogs && \
    mkdir -p /usr/local/Cellar/open-jtalk/1.11 && \
    # シンボリックリンクの作成
    ln -s /usr/local/lib/open_jtalk/dic /usr/local/Cellar/open-jtalk/1.11 && \
    ln -s /usr/local/lib/open_jtalk/voice /usr/local/Cellar/open-jtalk/1.11
WORKDIR /discordbot-mdn

# discordbot-mdn プログラムの構築
COPY mdn.py /discordbot-mdn
COPY cogs/ /discordbot-mdn/cogs/

# pip パッケージのインストール
COPY requirements.txt /discordbot-mdn
RUN set -x && \
    pip3 install -r requirements.txt

# docker-compose.yml, heroku.yml から渡された環境変数の読み込み
ARG BOT_TOKEN
ENV HOME=/${BOT_TOKEN}