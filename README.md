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

- [Heroku](https://www.heroku.com)
    - [Heroku Dynos](https://jp.heroku.com/dynos)
    - [Heroku Postgres](https://jp.heroku.com/postgres)
- [Docker](https://www.docker.com)
    - ベースイメージ：[emptypage/open_jtalk](https://hub.docker.com/r/emptypage/open_jtalk)

## 6. ライセンス

このアプリケーションは MIT ライセンスの下リリースされています。  
[ライセンス全文はこちら](https://github.com/kenkenpa198/discordbot-mdn/blob/main/LICENSE)

## 7. 補足

- 過去の Commit に bot のトークンの記述が残っていますが、トークンは既に無効化済みです。Git をプライベート設定で運用していた頃の名残であり、現在はサーバーの環境変数へ記述したものを yml ファイルから連携する形で管理しています。
- 不具合やご要望など、お気づきの点がありましたらお気軽にご連絡ください。

## 8. リンク

- [📙 お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック)  
    当 bot の使い方や導入方法をまとめています。
