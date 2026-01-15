import streamlit as st
import random

# 1. クイズデータの準備（単語を自由に追加できます）
# 辞書形式で { "英単語": "日本語訳" } を用意します
WORD_DATA = {
    "Apple": "りんご", "Banana": "バナナ", "Cat": "猫", "Dog": "犬",
    "Elephant": "象", "Flower": "花", "Guitar": "ギター", "House": "家",
    "Island": "島", "Journey": "旅", "Knowledge": "知識", "Library": "図書館",
    "Mountain": "山", "Nature": "自然", "Ocean": "海", "Pencil": "鉛筆",
    "Queen": "女王", "River": "川", "Sun": "太陽", "Tree": "木",
    "Umbrella": "傘", "Village": "村", "Window": "窓", "Xylophone": "木琴",
    "Yellow": "黄色", "Zebra": "シマウマ", "Beautiful": "美しい", "Challenge": "挑戦",
    "Development": "開発", "Education": "教育", "Future": "未来", "Global": "世界的な",
    "Happiness": "幸せ", "Important": "重要な", "Justice": "正義", "Kitchen": "台所",
    "Language": "言語", "Memory": "記憶", "Notebook": "ノート", "Opportunity": "機会",
    "Practice": "練習", "Quality": "品質", "Respect": "尊敬", "Success": "成功",
    "Technology": "技術", "Universe": "宇宙", "Victory": "勝利", "Weather": "天気",
    "Young": "若い", "Zone": "地域"
}

# 2. セッション状態（データの保持）の初期化
# Streamlitは操作のたびにコードが上から再実行されるため、
# 現在の問題やスコアを st.session_state に保存して記憶させます。
if 'current_word' not in st.session_state:
    st.session_state.current_word = None
    st.session_state.options = []
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.answered = False
    st.session_state.feedback = ""

def next_question():
    """新しい問題を作成する関数"""
    # 全単語からランダムに1つ正解を選ぶ
    word = random.choice(list(WORD_DATA.keys()))
    correct_ans = WORD_DATA[word]
    
    # 不正解の選択肢を3つ選ぶ（正解を除いたリストからランダム抽出）
    others = [v for v in WORD_DATA.values() if v != correct_ans]
    wrong_answers = random.sample(others, 3)
    
    # 正解と不正解を混ぜてリストにする
    options = [correct_ans] + wrong_answers
    random.shuffle(options)
    
    # 状態を更新
    st.session_state.current_word = word
    st.session_state.options = options
    st.session_state.answered = False
    st.session_state.feedback = ""

# 初回実行時のみ問題を生成
if st.session_state.current_word is None:
    next_question()

# 3. アプリの画面構成
st.title("🔤 英単語 4択クイズ")

# スコア表示
st.sidebar.write(f"### スコア: {st.session_state.score} / {st.session_state.total}")

# 問題の表示
st.write("---")
st.write(f"### 次の単語の意味は何ですか？")
st.header(f"**{st.session_state.current_word}**")

# 選択肢ボタンの配置
for option in st.session_state.options:
    # ボタンが押された時の処理
    if st.button(option, key=option, use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        
        # 正誤判定
        if option == WORD_DATA[st.session_state.current_word]:
            st.session_state.score += 1
            st.session_state.feedback = "⭕ 正解！"
        else:
            st.session_state.feedback = f"❌ 残念！正解は「{WORD_DATA[st.session_state.current_word]}」でした。"
        
        # 画面をリフレッシュして結果を表示
        st.rerun()

# 結果と次の問題へのボタン
if st.session_state.answered:
    st.subheader(st.session_state.feedback)
    if st.button("次の問題へ ➡️"):
        next_question()
        st.rerun()

# リセットボタン
if st.sidebar.button("スコアをリセット"):
    st.session_state.score = 0
    st.session_state.total = 0
    next_question()
    st.rerun()
