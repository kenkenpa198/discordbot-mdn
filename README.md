![おしゃべりぼっと！もだねちゃん](https://user-images.githubusercontent.com/75349575/120725676-7439e800-c511-11eb-8503-e8a98999a57e.png)
<p align="center"><b>おしゃべりぼっと！もだねちゃん</b></p>

---

## 1. もだねちゃんとは？

もだねちゃんは、ボイスチャットツール Discord 上で働いてくれる読み上げ Bot です。  
テキストチャンネルに投稿された文章を、ボイスチャンネルで読み上げてくれます。

「しゃべるのが恥ずかしい」「深夜なので声を出しにくい」などの理由でお声を出しづらい方でも、お友達と楽しく会話することができます。

働いている様子はこちら🌸（Youtube へ移動します）

[<img src="https://user-images.githubusercontent.com/75349575/101226033-75ab6480-36d6-11eb-877d-f63e33409883.jpg" alt="読み上げbot もだねちゃん 紹介動画" width="70%">](https://youtu.be/cRBdej7tsGc)

## 2. 招待 URL

[https://example.com/](https://example.com/)

※ ご協力いただいている少数のサーバーにて試験運用中のため、現在 Bot の一般公開は行っておりません。

## 3. 使い方

[📙 お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック) をご覧ください。

## 4. 使用ソフトウェア

- [alkana.py](https://github.com/cod-sushi/alkana.py)
- [discord.py](https://discordpy.readthedocs.io/)
- [Docker](https://www.docker.com)
    - [emptypage/open_jtalk:22.04-1.11](https://hub.docker.com/layers/emptypage/open_jtalk/22.04-1.11/images/sha256-16f1ee83f32f019c5a44eb14fd557fa36a3ff00b89e064c65e47d81f193c9601?context=explore)
    - [postgres:14.5-alpine3.16](https://hub.docker.com/layers/library/postgres/14.5-alpine3.16/images/sha256-9ece045f37060bf6b0a36ffbd5afa4f56636370791abae5062ed6005ec0e5110?context=explore)
- [jtalkbot](https://bitbucket.org/emptypage/jtalkbot/src/master/)
- [Open JTalk](http://open-jtalk.sourceforge.net)
- [Opus](https://opus-codec.org)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)

## 5. 実行環境

初公開から2年間の間は Heroku の無料プランを利用していました。  
[Heroku サービスの有料化](https://blog.heroku.com/next-chapter) に伴い、Google Cloud 上での稼働に移行しました。  

### 5.1. 2022年10月21日まで

タグ: `v0.17.0` まで

- [Heroku](https://www.heroku.com)
    - [Heroku Dynos](https://jp.heroku.com/dynos)
    - [Heroku Postgres](https://jp.heroku.com/postgres)

### 5.2. 2022年10月22日 ～ 2022年MM月DD日 <!-- TODO: 日付の変更 -->

タグ: `v0.18.0` まで

- [Railway](https://railway.app/)
    - Heroku サービスの有料化にあたり、一時的に利用しました。

### 5.3. 2022年MM月DD日から <!-- TODO: 日付の変更 -->

タグ: `v1.0.0` ～ 現バージョン

- [Google Cloud](https://console.cloud.google.com/)

## 6. ローカル PC 上での実行

ローカル PC 上での実行は以下の手順で行います。  
実行に関しては自己責任でお願いします。

### 6.1. 必要なもの

- Docker および Docker Compose が実行可能な環境（手順は WSL2 上での実行）
- 約 850 MB 以上の空き容量（下記内訳）
    - `discordbot-mdn_main` : 546 MB
    - `postgres` : 217 MB
    - `discordbot-mdn_db-volume` : 50 MB ～
- Discord Bot のトークン

### 6.2. 実行手順

1. リポジトリをクローン・ルートディレクトリへ移動

    ```shell
    $ git clone https://github.com/kenkenpa198/discordbot-mdn.git
    $ cd discordbot-mdn
    ```

2. `.env` ファイルを作成し、パスワードとトークンを変更。

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

3. `docker-compose` コマンドでコンテナを立ち上げ。

    ```shell
    $ docker-compose up -d
    ```

4. コンテナが起動していることを確認。

    ```shell
    $ docker ps
    $ docker-compose logs -f
    ```

5. Bot を招待したサーバーで実行確認。  
参考: [📙 お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック)

## 7. ライセンス

[MIT License](LICENSE)

## 8. その他

- 古いコミットに Bot のトークンの記述が残っていますが、既に無効化済みです。
    - Git をプライベート設定で運用していた頃の名残です。
    - 現在の仕様ではホスト OS の環境変数もしくは設定ファイル `.env` へ書き込まれた値をコンテナへ渡しています。

## 9. 参考文献

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
