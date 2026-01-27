import streamlit as st
import random

# --- 1. ページ設定 (必ず最初に実行) ---
st.set_page_config(
    page_title="Eiken Pre-1 Quiz",
    page_icon="📝",
    layout="centered"
)

# --- 2. 語彙データの準備 ---
# データ量が増える場合は別ファイル(JSONなど)に分けるのが理想的です
EIKEN_PRE1_DATA = {
    "Abundant": {"meaning": "豊富な、潤沢な", "example": "The region is abundant in natural resources like gold and copper."},
    "Adjacent": {"meaning": "隣接した、近隣の", "example": "The school is located adjacent to a large public park."},
    "Coincide": {"meaning": "同時に起こる、一致する", "example": "My vacation plans coincide with my brother's wedding."},
    "Deteriorate": {"meaning": "悪化する、低下する", "example": "The weather conditions began to deteriorate rapidly after sunset."},
    "Eliminate": {"meaning": "排除する、除去する", "example": "We need to eliminate unnecessary expenses to save money."},
    "Feasible": {"meaning": "実行可能な、実現可能な", "example": "The committee is checking if the new project is financially feasible."},
    "Inevitably": {"meaning": "必然的に、避けられないことに", "example": "Technological progress inevitably leads to changes in our lifestyle."},
    "Magnificent": {"meaning": "壮大な、見事な", "example": "The view from the top of the mountain was absolutely magnificent."},
    "Obscure": {"meaning": "曖昧な、世に知られていない", "example": "The origins of the manuscript remain obscure to this day."},
    "Prevalent": {"meaning": "普及している、一般的な", "example": "Flu infections are more prevalent during the winter months."},
    "Reluctant": {"meaning": "気が進まない、渋っている", "example": "She was reluctant to admit that she had made a mistake."},
    "Substantial": {"meaning": "かなりの、実質的な", "example": "The company reported a substantial increase in profits this year."},
}

# --- 3. セッション状態の初期化 ---
if 'current_word' not in st.session_state:
    st.session_state.current_word = None
    st.session_state.options = []
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.answered = False
    st.session_state.feedback = None

# --- 4. ロジック関数 ---
def next_question():
    word = random.choice(list(EIKEN_PRE1_DATA.keys()))
    correct_ans = EIKEN_PRE1_DATA[word]["meaning"]
    
    # 誤答の作成
    others = [info["meaning"] for w, info in EIKEN_PRE1_DATA.items() if w != word]
    wrong_answers = random.sample(others, min(len(others), 3))
    
    options = [correct_ans] + wrong_answers
    random.shuffle(options)
    
    st.session_state.current_word = word
    st.session_state.options = options
    st.session_state.answered = False
    st.session_state.feedback = None

def handle_answer(selected_option):
    st.session_state.answered = True
    st.session_state.total += 1
    correct_ans = EIKEN_PRE1_DATA[st.session_state.current_word]["meaning"]
    
    if selected_option == correct_ans:
        st.session_state.score += 1
        st.session_state.feedback = ("success", "🎯 正解！")
    else:
        st.session_state.feedback = ("error", f"⚠️ 不正解... 正解は「{correct_ans}」")

# 初回問題セット
if st.session_state.current_word is None:
    next_question()

# --- 5. UI構成 ---
st.title("📝 英検準1級 単語チャレンジ")

# サイドバー：進捗管理
with st.sidebar:
    st.header("📊 学習進捗")
    accuracy = (st.session_state.score / st.session_state.total * 100) if st.session_state.total > 0 else 0
    st.metric("正答率", f"{accuracy:.1f}%", delta=f"{st.session_state.score}問正解")
    st.progress(min(accuracy / 100, 1.0))
    st.write(f"解答数: {st.session_state.total}")
    
    st.divider()
    if st.button("進捗をリセット"):
        st.session_state.score = 0
        st.session_state.total = 0
        next_question()
        st.rerun()

# メインコンテンツ
st.write("---")
# 単語表示部分のデザイン改善
st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 25px;">
        <p style="color: #555; margin-bottom: 5px;">この単語の意味は？</p>
        <h1 style="margin-top: 0; color: #1E3A8A;">{st.session_state.current_word}</h1>
    </div>
""", unsafe_allow_html=True)

# 回答ボタン
cols = st.columns(2)
for i, option in enumerate(st.session_state.options):
    with cols[i % 2]:
        if st.button(option, key=f"btn_{i}", use_container_width=True, disabled=st.session_state.answered):
            handle_answer(option)
            st.rerun()

# フィードバック表示
if st.session_state.answered:
    status, msg = st.session_state.feedback
    if status == "success":
        st.success(msg)
    else:
        st.error(msg)
    
    # 解説と次の問題ボタン
    with st.container():
        st.markdown("### 📖 解説")
        word_info = EIKEN_PRE1_DATA[st.session_state.current_word]
        st.info(f"**{st.session_state.current_word}**: {word_info['meaning']}")
        st.write(f"**Example:**\n{word_info['example']}")
        
        if st.button("次の問題へ進む ⏩", type="primary", use_container_width=True):
            next_question()
            st.rerun()
