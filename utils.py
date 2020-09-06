#coding: utf-8
###ジャンケン！

## 入力された数値が0〜2の間か判定する
# def validate(hand):
# 	if hand < 0 or hand > 2:
# 		return False
# 	return True

## 「▼nameが出した手\n（手の絵文字）」を戻り値として返す
# handsはグーチョキパー3つのリスト
# 入力されたリストの番号（0,1,2）を受け取り、番号に対応した手を出力する
def rise_hand(hand, name='ゲスト'):
	hands = [':fist:', ':v:', ':hand_splayed:']#0:グー 1:チョキ 2:パー
	return '▼'+ name + 'が出した手\n' + hands[hand]

## プレイヤーとコンピュータの手を比較してアイコの判定を戻り値として返す
def judge_aiko(player, computer):
	if player == computer:
		print('勝敗：アイコ')
		print('--- 繰り返します ---')
		return 'アイコだ！さあ、もう一回！ジャンケン……\n\n'

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