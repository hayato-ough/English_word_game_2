import streamlit as st
import random

# 1. 語彙データの準備（英検準一級レベル + 例文）
# 構造: "単語": {"meaning": "意味", "example": "例文"}
EIKEN_PRE1_DATA = {
    "Abundant": {
        "meaning": "豊富な、潤沢な",
        "example": "The region is abundant in natural resources like gold and copper."
    },
    "Adjacent": {
        "meaning": "隣接した、近隣の",
        "example": "The school is located adjacent to a large public park."
    },
    "Coincide": {
        "meaning": "同時に起こる、一致する",
        "example": "My vacation plans coincide with my brother's wedding."
    },
    "Deteriorate": {
        "meaning": "悪化する、低下する",
        "example": "The weather conditions began to deteriorate rapidly after sunset."
    },
    "Eliminate": {
        "meaning": "排除する、除去する",
        "example": "We need to eliminate unnecessary expenses to save money."
    },
    "Feasible": {
        "meaning": "実行可能な、実現可能な",
        "example": "The committee is checking if the new project is financially feasible."
    },
    "Inevitably": {
        "meaning": "必然的に、避けられないことに",
        "example": "Technological progress inevitably leads to changes in our lifestyle."
    },
    "Magnificent": {
        "meaning": "壮大な、見事な",
        "example": "The view from the top of the mountain was absolutely magnificent."
    },
    "Obscure": {
        "meaning": "曖昧な、世に知られていない",
        "example": "The origins of the manuscript remain obscure to this day."
    },
    "Prevalent": {
        "meaning": "普及している、一般的な",
        "example": "Flu infections are more prevalent during the winter months."
    },
    "Reluctant": {
        "meaning": "気が進まない、渋っている",
        "example": "She was reluctant to admit that she had made a mistake."
    },
    "Substantial": {
        "meaning": "かなりの、実質的な",
        "example": "The company reported a substantial increase in profits this year."
    },
}

# 2. セッション状態の初期化
if 'current_word' not in st.session_state:
    st.session_state.current_word = None
    st.session_state.options = []
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.answered = False
    st.session_state.feedback = ""

def next_question():
    word = random.choice(list(EIKEN_PRE1_DATA.keys()))
    correct_ans = EIKEN_PRE1_DATA[word]["meaning"]
    
    # 全ての意味リストから正解以外を抽出
    others = [info["meaning"] for w, info in EIKEN_PRE1_DATA.items() if w != word]
    wrong_answers = random.sample(others, 3)
    
    options = [correct_ans] + wrong_answers
    random.shuffle(options)
    
    st.session_state.current_word = word
    st.session_state.options = options
    st.session_state.answered = False
    st.session_state.feedback = ""

# 初回起動時
if st.session_state.current_word is None:
    next_question()

# 3. UI構成
st.set_page_config(page_title="Eiken Pre-1 Quiz", page_icon="📝")
st.title("📝 英検準1級 単語チャレンジ")

# サイドバー
st.sidebar.header("📊 学習進捗")
accuracy = (st.session_state.score / st.session_state.total * 100) if st.session_state.total > 0 else 0
st.sidebar.metric("正解数", f"{st.session_state.score} / {st.session_state.total}")
st.sidebar.progress(min(accuracy / 100, 1.0))
st.sidebar.write(f"正答率: **{accuracy:.1f}%**")

st.write("---")
st.info(f"次の単語の意味を選んでください:  \n# **{st.session_state.current_word}**", icon="🧐")

# 4. 回答処理ロジック
def handle_answer(selected_option):
    st.session_state.answered = True
    st.session_state.total += 1
    correct_ans = EIKEN_PRE1_DATA[st.session_state.current_word]["meaning"]
    
    if selected_option == correct_ans:
        st.session_state.score += 1
        st.session_state.feedback = ("success", f"🎯 **正解！**")
    else:
        st.session_state.feedback = ("error", f"⚠️ **不正解...** 正解は「**{correct_ans}**」でした。")

# 選択肢の表示
col1, col2 = st.columns(2)
for i, option in enumerate(st.session_state.options):
    target_col = col1 if i % 2 == 0 else col2
    if target_col.button(option, key=f"btn_{i}", use_container_width=True, disabled=st.session_state.answered):
        handle_answer(option)
        st.rerun()

# フィードバックと例文の表示
if st.session_state.answered:
    fb_type, fb_msg = st.session_state.feedback
    if fb_type == "success":
        st.success(fb_msg)
    else:
        st.error(fb_msg)
    
    # 例文セクションの追加
    with st.expander("📖 この単語の例文を見る", expanded=True):
        st.markdown(f"**Example:**")
        st.info(EIKEN_PRE1_DATA[st.session_state.current_word]["example"])
        
    if st.button("次の問題へ進む ⏩", use_container_width=True):
        next_question()
        st.rerun()

# 設定
with st.sidebar.expander("システム設定"):
    if st.button("進捗をリセットする"):
        st.session_state.score = 0
        st.session_state.total = 0
        next_question()
        st.rerun()
