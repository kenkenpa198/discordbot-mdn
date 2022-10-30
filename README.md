<!-- omit in toc -->
# ![おしゃべりぼっと！もだねちゃん](images/kv.png)

<p align="center"><b>おしゃべりぼっと！もだねちゃん</b></p>

<!-- omit in toc -->
## 目次

- [1. もだねちゃんとは？](#1-もだねちゃんとは)
- [2. 招待 URL・使い方](#2-招待-url使い方)
- [3. 使用ソフトウェア](#3-使用ソフトウェア)
- [4. 稼働環境](#4-稼働環境)
    - [4.1. 概観図](#41-概観図)
    - [4.2. 稼働環境の変遷](#42-稼働環境の変遷)
- [5. ローカル PC 上での実行](#5-ローカル-pc-上での実行)
    - [5.1. 必要なもの](#51-必要なもの)
    - [5.2. 実行手順](#52-実行手順)
- [6. ライセンス](#6-ライセンス)
- [7. その他](#7-その他)
- [8. 参考文献](#8-参考文献)

## 1. もだねちゃんとは？

もだねちゃんは、ボイスチャットツール Discord 上で働いてくれる読み上げ Bot です。  
テキストチャンネルに投稿された文章をボイスチャンネルで読み上げてくれます。

「しゃべるのが恥ずかしい」「深夜なので声を出しにくい」などの理由でお声を出しづらい方でも、お友達と楽しく会話することができます。

働いている様子はこちら🌸（Youtube へ移動します）

[<img src="images/movie_thumbnail.jpg" alt="読み上げbot もだねちゃん 紹介動画" width="70%">](https://youtu.be/cRBdej7tsGc)

## 2. 招待 URL・使い方

[📙 お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック) をご覧ください。

## 3. 使用ソフトウェア

- [alkana.py](https://github.com/cod-sushi/alkana.py)
- [discord.py](https://discordpy.readthedocs.io/)
- [Docker](https://www.docker.com)
    - [emptypage/open_jtalk:22.04-1.11](https://hub.docker.com/layers/emptypage/open_jtalk/22.04-1.11/images/sha256-16f1ee83f32f019c5a44eb14fd557fa36a3ff00b89e064c65e47d81f193c9601?context=explore)
    - [postgres:14.5-alpine3.16](https://hub.docker.com/layers/library/postgres/14.5-alpine3.16/images/sha256-9ece045f37060bf6b0a36ffbd5afa4f56636370791abae5062ed6005ec0e5110?context=explore)
- [jtalkbot](https://bitbucket.org/emptypage/jtalkbot/src/master/)
- [Open JTalk](http://open-jtalk.sourceforge.net)
- [Opus](https://opus-codec.org)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)

## 4. 稼働環境

[Google Cloud](https://console.cloud.google.com/) 上に構築したサーバーにて稼働中です。

### 4.1. 概観図

<!-- TODO: 図を作成する -->

### 4.2. 稼働環境の変遷

初公開から約2年間の間は [Heroku](https://www.heroku.com) の無料プランを利用していました。  
[Heroku サービスの有料化](https://blog.heroku.com/next-chapter) に伴い、Google Cloud 上での稼働に移行しました。  

| 日付       | タグ             | プラットフォーム        | 備考                                                                    |
|------------|------------------|-------------------------|-------------------------------------------------------------------------|
| 2020-09-12 | -                | Local -> Heroku         | Heroku にて稼働を開始。                                                 |
| 2022-08-21 | v0.17.0          | Heroku                  | Heroku 上での稼働最終バージョン。                                       |
| 2022-08-25 | -                | -                       | Heroku サービスの有料化が発表。                                         |
| 2022-10-22 | v0.18.0          | Heroku -> Railway       | 引っ越し先の検討のため [Railway](https://railway.app/) を一時的に利用。 |
| 2022-11-05 | v1.0.0           | Railway -> Google Cloud | Google Cloud にて稼働開始。                                             |

## 5. ローカル PC 上での実行

ローカル PC 上での実行は以下の手順で行います。  
実行に関しては自己責任でお願いします。

### 5.1. 必要なもの

- Docker および Docker Compose が実行可能な環境（手順は WSL2 上での実行）
- 約 850 MB 以上の空き容量（下記内訳）
    - `discordbot-mdn_main` : 546 MB
    - `postgres` : 217 MB
    - `discordbot-mdn_db-volume` : 50 MB ～
- Discord Bot のトークン

### 5.2. 実行手順

1. リポジトリをクローン。

    ```shell
    $ git clone https://github.com/kenkenpa198/discordbot-mdn.git
    ```

2. リポジトリのルートディレクトリへ移動。

    ```shell
    $ cd discordbot-mdn
    ```

3. `.env` ファイルを作成し、パスワードとトークンを変更。

    ```shell
    $ cp .env.sample .env
    $ vim .env
    ```

    ```properties
    # PostgreSQL イメージ用の環境変数
    POSTGRES_USER=discordbot_mdn
    POSTGRES_PASSWORD=__ENTER_PG_PASSWORD_HERE__ # 好みのパスワードを記述
    POSTGRES_DB=discordbot_mdn_db

    # PostgreSQL の接続用 URL
    DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}

    # bot のトークン
    BOT_TOKEN=__ENTER_BOT_TOKEN_HERE__           # Discord Bot のアクセストークンを記述
    ```

4. `docker-compose` コマンドでコンテナを立ち上げ。

    ```shell
    $ docker-compose up -d
    ```

5. コンテナが起動していることを確認。

    ```shell
    $ docker ps
    $ docker-compose logs -f
    ```

6. Bot を招待したサーバーで実行確認。  
参考: [📙 お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック)

## 6. ライセンス

[MIT License](LICENSE)

## 7. その他

- 古いコミットに Bot のトークンの記述が残っていますが、既に無効化済みです。
    - Git をプライベート設定で運用していた頃の名残です。
    - 現在の仕様ではホスト OS の環境変数もしくは設定ファイル `.env` へ書き込まれた値をコンテナへ渡しています。

## 8. 参考文献

- [discord.py へようこそ。](https://discordpy.readthedocs.io/ja/latest/#)
- [Pythonで実用Discord Bot(discordpy解説) - Qiita](https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f)
- [Discord Botアカウント初期設定ガイド for Developer - Qiita](https://qiita.com/1ntegrale9/items/cb285053f2fa5d0cccdf)
- [DiscordBot開発実践入門 - cod-sushi - BOOTH](https://cod-sushi.booth.pm/items/2391223)
- [DiscordBot運営実践入門 - cod-sushi - BOOTH](https://booth.pm/ja/items/1533599)
- [psycopg2 メモ - Qiita](https://qiita.com/hitsumabushi845/items/a421aff1bcd7999f7e40)
- [【Docker】PostgreSQLの起動時に初期データをセットアップ | 素人エンジニアの苦悩](https://amateur-engineer.com/docker-compose-postgresql/)
- [postgresql - Error when running psql command in /docker-entrypoint-initdb.d/db_init.sh (psql: could not connect to server: Connection refused) - Stack Overflow](https://stackoverflow.com/questions/51659972/error-when-running-psql-command-in-docker-entrypoint-initdb-d-db-init-sh-psql)
- [Postgres公式Dockerイメージのパスワードの扱いについて](https://zenn.dev/dowanna6/articles/6cc31869346a06)
- [社内のDockerfileのベストプラクティスを公開します│FORCIA CUBE│フォルシア株式会社](https://www.forcia.com/blog/002273.html)
- [Dockerイメージのレイヤの考え方とイメージの軽量化について - ネットワークエンジニアを目指して](https://www.itbook.info/network/docker02.html)
- [docker-composeでサービス運用しているなら設定しておきたいログローテート - Qiita](https://qiita.com/harachan/items/fa306cc1e6b497e592c3)
