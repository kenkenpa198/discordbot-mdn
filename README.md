![おしゃべりぼっと！もだねちゃん](https://user-images.githubusercontent.com/75349575/120725676-7439e800-c511-11eb-8503-e8a98999a57e.png)
<p align="center"><b>おしゃべりぼっと！もだねちゃん</b></p>

---

## **1. もだねちゃんとは？**
もだねちゃんは、ボイスチャットツール Discord 上で働いてくれる Discord bot です 🌸

一番の特徴は読み上げ機能です。テキストチャンネルに投稿された文章を、ボイスチャンネルで読み上げてくれます。  
働いている様子はこちら！（ Youtube へ移動します）

[<img src="https://user-images.githubusercontent.com/75349575/101226033-75ab6480-36d6-11eb-877d-f63e33409883.jpg" alt="読み上げbot もだねちゃん 紹介動画" width="70%">](https://youtu.be/cRBdej7tsGc)

「しゃべるのが恥ずかしい」「深夜なので声を出しにくい」などの理由でお声を出しづらい方でも、お友達と楽しく会話することができます。

その他、機能の詳細や使い方・導入方法は [📙 お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック) をご覧ください！  
※ 現在はご協力いただいている少数のサーバーにて試験運用中のため、bot の一般公開は行っておりません。

## **2. 各種情報**
bot の仕様やライセンスに関する情報を掲載しています。

### **💻 使用技術**
#### **言語**

- [Python 3.9](https://www.python.org)
- 外部モジュールは以下を使用させていただいています。
    - [discord.py](https://discordpy.readthedocs.io/)
    - [jtalkbot](https://bitbucket.org/emptypage/jtalkbot/src/master/)
    - [alkana.py](https://github.com/cod-sushi/alkana.py)
    - [psycopg2](https://github.com/psycopg/psycopg2)

#### **連携ソフトウェア**


- [Open JTalk](http://open-jtalk.sourceforge.net)
- [Opus](https://opus-codec.org)
- [PostgeSQL](https://www.postgresql.org)


#### **実行環境**

- [Heroku](https://www.heroku.com)
    - [Heroku Dynos](https://jp.heroku.com/dynos)
    - [Heroku Postgres](https://jp.heroku.com/postgres)
- [Docker](https://www.docker.com)
    - ベースイメージ：[emptypage/open_jtalk](https://hub.docker.com/r/emptypage/open_jtalk)

### **💳 ライセンス**
このアプリケーションは MIT ライセンスの下でリリースされています。  
[ライセンス全文はこちら](https://github.com/kenkenpa198/discordbot-mdn/blob/main/LICENSE)

### **📝 その他**

- 過去の Commit に bot のトークンの記述が残っていますが、トークンは既に無効化済みです。Git をプライベート設定で運用していた頃の名残です。現在は OS / サーバーの環境変数へ記述したものを yml ファイルから連携する形で管理しています。
- 不具合やご要望など、お気づきの点がありましたらお気軽にご連絡ください。


## **3. リンク集**
### **📖 Wiki**
- [📙 お仕事内容ガイドブック](https://github.com/kenkenpa198/discordbot-mdn/wiki/📙-お仕事内容ガイドブック)   
    当 bot の使い方や導入方法をまとめています。
