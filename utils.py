#coding: utf-8

##### ジャンケン用関数 #####
## 返答のチェック関数を定義
def janken_check(m):
	return m.content == '0' or m.content == '1' or m.content == '2' # 数値が0,1,2のどれかだったらOK

## メッセージをグーチョキパーの絵文字へ変換する
# handsはグーチョキパー3つのリスト
# 入力されたリストの番号（0,1,2）を受け取り、番号に対応した手を出力する
def rise_hand(hand):
	hands = [':fist:', ':v:', ':hand_splayed:'] # 0:グー 1:チョキ 2:パー
	return hands[hand]

## プレイヤーとコンピュータの手を比較してアイコの判定を戻り値として返す
def judge_aiko(player, computer):
	if player == computer:
		print('勝敗：アイコ')
		print('--- 繰り返します ---')
		return 'アイコだ！さあ、もう一回！\nジャンケン……'

## プレイヤーとコンピュータの手を比較して勝敗を戻り値として返す
def judge(player, computer):
	if player == 0 and computer == 1:
		print('勝敗：プレイヤーの勝ち')
		return 'わっ！キミの勝ち！'
	elif player == 1 and computer == 2:
		print('勝敗：プレイヤーの勝ち')
		return 'あー！キミの勝ちだっ！'
	elif player == 2 and computer == 0:
		print('勝敗：プレイヤーの勝ち')
		return 'おおっ！キミの勝ちだね！'
	else:
		print('勝敗：コンピュータの勝ち')
		return 'やったー！わたしの勝ち！'