# ビルド
FROM emptypage/open_jtalk:22.04-1.11

# tzdata の入力を待たない
ENV DEBIAN_FRONTEND=noninteractive

# 環境構築
RUN set -x && \
    apt update -y && \
    apt install -y libopus-dev libpq-dev python3-pip tzdata && \
    pip3 install --upgrade pip && \
    pip3 install alkana==0.0.3 discord.py==1.7.3 jtalkbot==0.6.1.3 psycopg2==2.9.3

# キャッシュの削除
RUN set -x && \
    apt clean -y && \
    rm -rf /var/lib/apt/lists/*

# bot 用のディレクトリを作成
RUN mkdir /discordbot-mdn

# 新規ユーザーを作成・ディレクトリへ所有権と権限を設定
RUN useradd myuser && \
    chown -R myuser /discordbot-mdn

# bot のソースコードをコンテナ内へ複製
COPY /discordbot-mdn/bot.py /discordbot-mdn/bot.py
COPY /discordbot-mdn/cogs/ /discordbot-mdn/cogs/

# ユーザーを切り替え
USER myuser

# 作業ディレクトリを指定
WORKDIR /discordbot-mdn

# コンテナ稼働時の実行コマンドを定義
CMD /bin/sh -c "python3 -u bot.py"
