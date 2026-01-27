import streamlit as st
import random

# 1. アカデミック単語データの準備
# 大学の講義や論文で頻出する、抽象度の高い語彙を選定しました。
WORD_DATA = {
    "Ambiguity": "曖昧さ", "Analogy": "類推", "Arbitrary": "任意の", "Cognitive": "認知の",
    "Conjecture": "推測", "Consensus": "合意", "Deduce": "演繹する", "Empirical": "経験的な",
    "Equivocal": "紛らわしい", "Hypothesis": "仮説", "Inherent": "固有の", "Innate": "先天的な",
    "Intrinsic": "本質的な", "Manifest": "明らかにする", "Objective": "客観的な", "Paradigm": "理論的枠組み",
    "Pragmatic": "実用的な", "Prevalent": "普及している", "Qualitative": "質的な", "Quantitative": "量的な",
    "Rational": "合理的な", "Redundant": "冗長な", "Substantiate": "実証する", "Synthesis": "統合",
    "Theoretical": "理論的な", "Validity": "妥当性", "Acquisition": "習得", "Advocate": "提唱する",
    "Correlation": "相関関係", "Deviation": "逸脱", "Eradicate": "根絶する", "Fluctuation": "変動",
    "Implication": "示唆", "Infrastructure": "基盤", "Legitimate": "正当な", "Marginal": "わずかな",
    "Perspective": "観点", "Phenomenon": "現象", "Preliminary": "予備の", "Resilient": "回復力のある",
    "Simultaneous": "同時の", "Speculate": "推測する", "Transformation": "変容", "Underlie": "根底にある",
    "Versatile": "多才な", "Viable": "実行可能な", "Warrant": "正当化する", "Yield": "産出する",
    "Altruism": "利他主義", "Paradox": "逆説"
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
    """学術単語リストから次の問題セットを生成"""
    word = random.choice(list(WORD_DATA.keys()))
    correct_ans = WORD_DATA[word]
    
    # 誤選択肢の生成
    others = [v for v in WORD_DATA.values() if v != correct_ans]
    wrong_answers = random.sample(others, 3)
    
    options = [correct_ans] + wrong_answers
    random.shuffle(options)
    
    st.session_state.current_word = word
    st.session_state.options = options
    st.session_state.answered = False
    st.session_state.feedback = ""

if st.session_state.current_word is None:
    next_question()

# 3. UI構成
st.set_page_config(page_title="Academic Vocabulary Quiz", page_icon="🎓")
st.title("🎓 Academic Vocabulary Challenge")
st.caption("大学教育や研究論文レベルの高度な英単語クイズ")

# サイドバー統計
st.sidebar.header("Statistics")
accuracy = (st.session_state.score / st.session_state.total * 100) if st.session_state.total > 0 else 0
st.sidebar.metric("Score", f"{st.session_state.score} / {st.session_state.total}")
st.sidebar.progress(accuracy / 100)
st.sidebar.write(f"正解率: {accuracy:.1f}%")

# メインコンテンツ
st.write("---")
st.subheader("Select the appropriate definition:")
st.info(f"Term:  **{st.session_state.current_word}**", icon="📖")

# 選択肢ボタン
for option in st.session_state.options:
    if st.button(option, key=option, use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        
        if option == WORD_DATA[st.session_state.current_word]:
            st.session_state.score += 1
            st.session_state.feedback = "✅ Correct! Excellent understanding."
        else:
            correct = WORD_DATA[st.session_state.current_word]
            st.session_state.feedback = f"❌ Incorrect. The correct definition is: **{correct}**"
        
        st.rerun()

# フィードバックと遷移
if st.session_state.answered:
    st.markdown(st.session_state.feedback)
    if st.button("Proceed to Next Question ➡️"):
        next_question()
        st.rerun()

# リセット設定
st.sidebar.write("---")
if st.sidebar.button("Reset Session"):
    st.session_state.score = 0
    st.session_state.total = 0
    next_question()
    st.rerun()
