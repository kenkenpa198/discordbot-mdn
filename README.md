![おしゃべりぼっと！もだねちゃん](https://user-images.githubusercontent.com/75349575/120725676-7439e800-c511-11eb-8503-e8a98999a57e.png)
<p align="center"><b>おしゃべりぼっと！もだねちゃん</b></p>

---

## 1. もだねちゃんとは？

もだねちゃんは、ボイスチャットツール Discord 上で働いてくれる読み上げ bot です。  
テキストチャンネルに投稿された文章を、ボイスチャンネルで読み上げてくれます。

「しゃべるのが恥ずかしい」「深夜なので声を出しにくい」などの理由でお声を出しづらい方でも、お友達と楽しく会話することができます。

働いている様子はこちら🌸（ Youtube へ移動します）

[<img src="https://user-images.githubusercontent.com/75349575/101226033-75ab6480-36d6-11eb-877d-f63e33409883.jpg" alt="読み上げbot もだねちゃん 紹介動画" width="70%">](https://youtu.be/cRBdej7tsGc)

## 2. 招待 URL

[https://example.com/](https://example.com/)

※ ご協力いただいている少数のサーバーにて試験運用中のため、現在 bot の一般公開は行っておりません。

## 3. 使い方

[📙 お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック) をご覧ください。

## 4. 使用ソフトウェア

- [alkana.py](https://github.com/cod-sushi/alkana.py)
- [discord.py](https://discordpy.readthedocs.io/)
- [Docker](https://www.docker.com)
    - [emptypage/open_jtalk:22.04-1.11](https://hub.docker.com/layers/emptypage/open_jtalk/22.04-1.11/images/sha256-16f1ee83f32f019c5a44eb14fd557fa36a3ff00b89e064c65e47d81f193c9601?context=explore)
    - [postgres:14.5-alpine3.16](https://hub.docker.com/layers/library/postgres/14.5-alpine3.16/images/sha256-9ece045f37060bf6b0a36ffbd5afa4f56636370791abae5062ed6005ec0e5110?context=explore) ※ 開発環境でのみ使用
- [jtalkbot](https://bitbucket.org/emptypage/jtalkbot/src/master/)
- [Open JTalk](http://open-jtalk.sourceforge.net)
- [Opus](https://opus-codec.org)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)

## 5. 実行環境

### 5.1. 2022年10月21日まで

- [Heroku](https://www.heroku.com)
    - [Heroku Dynos](https://jp.heroku.com/dynos)
    - [Heroku Postgres](https://jp.heroku.com/postgres)

### 5.2. 2022年10月22日から

[Heroku サービスの有料化](https://blog.heroku.com/next-chapter) に伴い、実行環境を [Railway](https://railway.app/) に移行しました（仮）。  

- [Railway](https://railway.app/)

## 6. ライセンス

[MIT License](LICENSE)

## 7. その他

- 古いコミットに bot のトークンの記述が残っていますが既に無効化済みです。Git をプライベート設定で運用していた頃の名残です。
    - 現在の仕様ではホスト OS の環境変数もしくは設定ファイル `.env` へ記述を行っています。

## 8. 参考文献

- [discord.py へようこそ。](https://discordpy.readthedocs.io/ja/latest/#)
- [【Docker】PostgreSQLの起動時に初期データをセットアップ | 素人エンジニアの苦悩](https://amateur-engineer.com/docker-compose-postgresql/)
- [psycopg2 メモ - Qiita](https://qiita.com/hitsumabushi845/items/a421aff1bcd7999f7e40)
- [Dockerのコンテナ間通信をする方法をまとめる - きり丸の技術日記](https://nainaistar.hatenablog.com/entry/2021/06/14/120000)
- [社内のDockerfileのベストプラクティスを公開します│FORCIA CUBE│フォルシア株式会社](https://www.forcia.com/blog/002273.html)
- [Dockerイメージのレイヤの考え方とイメージの軽量化について - ネットワークエンジニアを目指して](https://www.itbook.info/network/docker02.html)
- [Postgres公式Dockerイメージのパスワードの扱いについて](https://zenn.dev/dowanna6/articles/6cc31869346a06)
