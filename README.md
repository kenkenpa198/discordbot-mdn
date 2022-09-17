![おしゃべりぼっと！もだねちゃん](https://user-images.githubusercontent.com/75349575/120725676-7439e800-c511-11eb-8503-e8a98999a57e.png)
<p align="center"><b>おしゃべりぼっと！もだねちゃん</b></p>

---

## 1. もだねちゃんとは？

もだねちゃんは、ボイスチャットツール Discord 上で働いてくれる読み上げ bot です。  
テキストチャンネルに投稿された文章を、ボイスチャンネルで読み上げてくれます。

「しゃべるのが恥ずかしい」「深夜なので声を出しにくい」などの理由で  
お声を出しづらい方でも、お友達と楽しく会話することができます。

機能の詳細や使い方・導入方法は [📙 お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック) をご覧ください。  

## 2. 紹介動画

働いている様子はこちら🌸（ Youtube へ移動します）

[<img src="https://user-images.githubusercontent.com/75349575/101226033-75ab6480-36d6-11eb-877d-f63e33409883.jpg" alt="読み上げbot もだねちゃん 紹介動画" width="70%">](https://youtu.be/cRBdej7tsGc)

## 3. 招待 URL

[https://example.com/](https://example.com/)

※ ご協力いただいている少数のサーバーにて試験運用中のため、現在 bot の一般公開は行っておりません。

## 4. 使用ソフトウェア

- [discord.py](https://discordpy.readthedocs.io/)
- [alkana.py](https://github.com/cod-sushi/alkana.py)
- [jtalkbot](https://bitbucket.org/emptypage/jtalkbot/src/master/)
- [Open JTalk](http://open-jtalk.sourceforge.net)
- [Opus](https://opus-codec.org)
- [psycopg2](https://github.com/psycopg/psycopg2)

## 5. 実行環境

- ~[Heroku](https://www.heroku.com)~
    - ~[Heroku Dynos](https://jp.heroku.com/dynos)~
    - ~[Heroku Postgres](https://jp.heroku.com/postgres)~
- [Docker](https://www.docker.com)
    - Bot: [emptypage/open_jtalk:22.04-1.11](https://hub.docker.com/layers/emptypage/open_jtalk/22.04-1.11/images/sha256-16f1ee83f32f019c5a44eb14fd557fa36a3ff00b89e064c65e47d81f193c9601?context=explore)
    - Database: [postgres:14.5-alpine3.16](https://hub.docker.com/layers/library/postgres/14.5-alpine3.16/images/sha256-9ece045f37060bf6b0a36ffbd5afa4f56636370791abae5062ed6005ec0e5110?context=explore)

（2022年09月追記）[利用していた Heroku サービスの有料化](https://blog.heroku.com/next-chapter) に伴い、実行環境をラズパイ上の Docker コンテナに移行しました。  

## 6. ライセンス

[MIT License](LICENSE)

## 7. 補足

- 過去の Commit に bot のトークンの記述が残っていますが、トークンは既に無効化済みです（Git をプライベート設定で運用していた頃の名残）。現在の仕様では環境変数の設定ファイル `.env` へ記述を行います。

## 8. リンク

- [📙 お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック)  
当 bot の使い方や導入方法をまとめています。
