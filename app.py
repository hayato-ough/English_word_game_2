words = [
    {"en": "hello", "jp" : "こんにちは"},
    {"en": "bye", "jp" : "さようなら"},
    {"en": "thank you", "jp" : "ありがとう"},
    {"en": "disgusting", "jp": "気持ち悪い"},
    {"en": "yes", "jp" : "はい"},
    {"en": "no", "jp" : "いいえ"},
    {"en": "please", "jp" : "お願いします"},
    {"en": "excuse me", "jp" : "すみません"},
    {"en": "water", "jp" : "水"},
    {"en": "food", "jp" : "食べ物"},
    {"en": "book", "jp" : "本"},
    {"en": "cat", "jp": "猫"},
    {"en": "dog", "jp": "犬"},
    {"en": "apple", "jp": "りんご"},
    {"en": "teacher", "jp": "先生"},
    {"en": "student", "jp": "生徒"}
]

import random

def play_word_game(word_list):
    print("英単語暗記ゲームを始めます！")

    # 全ての日本語訳のリストを作成（不正解の選択肢用）
    all_japanese_words = [d["jp"] for d in word_list]

    while True:
        # ランダムに単語を選択
        selected_word_pair = random.choice(word_list)
        english_word = selected_word_pair["en"]
        correct_japanese = selected_word_pair["jp"]

        # 不正解の選択肢を生成
        incorrect_options = [jp for jp in all_japanese_words if jp != correct_japanese]
        random.shuffle(incorrect_options)

        # 最大3つの不正解の選択肢を選ぶ
        num_choices = min(len(incorrect_options), 2) # 最大2つの不正解オプション
        chosen_incorrect_options = random.sample(incorrect_options, num_choices)

        # 正解と不正解の選択肢を結合し、シャッフル
        choices = chosen_incorrect_options + [correct_japanese]
        random.shuffle(choices)

        print(f"問題: {english_word} の日本語訳は何ですか？")
        for i, choice in enumerate(choices):
            print(f"{i+1}. {choice}")

        while True:
            try:
                user_answer_index = int(input("あなたの答え (番号で入力): "))
                if 1 <= user_answer_index <= len(choices):
                    break
                else:
                    print("無効な入力です。表示された番号から選んでください。")
            except ValueError:
                print("無効な入力です。数字を入力してください。")

        if choices[user_answer_index - 1] == correct_japanese:
            print("正解です！")
        else:
            print(f"不正解です。正解は {correct_japanese} でした。")

        play_again = input("もう一度プレイしますか？ (はい/いいえ): ")
        if play_again.lower() != 'はい':
            print("ゲームを終了します。")
            break

# ゲームを開始
play_word_game(words)
