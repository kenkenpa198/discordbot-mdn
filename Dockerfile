##### 実行環境の構築 #####
FROM emptypage/open_jtalk:20.4_1.11

# tzdata の入力を待たない
ENV DEBIAN_FRONTEND=noninteractive

RUN set -x && \
    apt-get update -y && \
    apt-get install -y python3-pip libopus-dev && \
    apt-get install -y tzdata && \
    apt-get install -y libpq-dev && \
    pip3 install --upgrade pip && \
    pip3 install jtalkbot==0.5.0 discord.py==1.6.0 psycopg2==2.8.6 alkana.py==0.0.1
# 環境変数の読み込み
# docker-compose.yml / heroku.yml から渡されたトークンなどを読み込む
ARG TZ
ENV HOME=/${TZ}
ARG BOT_TOKEN
ENV HOME=/${BOT_TOKEN}
ARG DATABASE_URL
ENV HOME=/${DATABASE_URL}

##### アプリ環境の構築 #####
RUN set -x && \
    mkdir /discordbot-mdn && \
    mkdir /discordbot-mdn/cogs && \
    mkdir -p /usr/local/Cellar/open-jtalk/1.11 && \
    # シンボリックリンクの作成
    ln -s /usr/local/lib/open_jtalk/dic /usr/local/Cellar/open-jtalk/1.11 && \
    ln -s /usr/local/lib/open_jtalk/voice /usr/local/Cellar/open-jtalk/1.11
WORKDIR /discordbot-mdn
COPY /discordbot-mdn/bot.py /discordbot-mdn/bot.py
COPY /discordbot-mdn/cogs/ /discordbot-mdn/cogs/

##### キャッシュの削除 #####
# TODO: python モジュールのキャッシュも削除したい
RUN set -x && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*