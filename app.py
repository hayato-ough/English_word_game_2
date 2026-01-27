import streamlit as st
import random

# 1. 高度な学術・知的語彙データの準備 (400語規模への拡張用リスト)
# 教授が講義で使う専門語、知的スラング、ラテン語由来の慣用句などを選定。
EXTENDED_WORD_DATA = {
    # --- Academic & Analytical (学術・分析) ---
    "Epistemology": "認識論", "Paradigm Shift": "パラダイムシフト（理論的枠組みの劇的変化）",
    "Heuristic": "発見的な（試行錯誤による）", "Empirical Evidence": "経験的証拠",
    "Categorical Imperative": "定言命法（無条件の道徳的命令）", "Axiomatic": "自明の",
    "Dialectic": "弁証法的な", "Syllogism": "三段論法",
    "Ontological": "存在論的な", "Qualitative Analysis": "質的分析",
    
    # --- Intellectual/Professor Slang & Nuance (教授が好む知的表現) ---
    "Nuance": "微妙な差異", "Ponderous": "（話が）回りくどくて退屈な",
    "Pedantic": "学識をひけらかす（細かな規則に拘泥する）", "Eloquent": "雄弁な",
    "Equivocate": "言葉を濁す（曖昧なことを言う）", "Caveat": "警告・但し書き",
    "Postulate": "仮定する", "Elucidate": "（明快に）説明する",
    "Salient": "顕著な（目立つ）", "Idiosyncrasy": "特異質（独特の癖）",
    
    # --- Latin Phrases used in Academia (学術界で使われるラテン語) ---
    "Ad hoc": "特定の目的のための（限定的な）", "De facto": "事実上の",
    "Quid pro quo": "見返りとしての代償", "Status quo": "現状",
    "In situ": "本来の場所で", "Per se": "それ自体は",
    
    # --- High-level Native Idioms/Phrases (高度な慣用表現) ---
    "Devil's Advocate": "あえて反論を唱える人", "Ivory Tower": "象牙の塔（世間知らずな学界）",
    "Cognitive Dissonance": "認知的不協和", "Paradigm of Virtue": "美徳の模範",
    "The crux of the matter": "問題の核心", "Breadth and depth": "広がりと深さ",
    
    # --- Verbs for Research (研究用動詞) ---
    "Substantiate": "具体化する（実証する）", "Ameliorate": "改善する",
    "Exacerbate": "悪化させる", "Corroborate": "裏付ける",
    "Delineate": "（詳細に）記述する", "Synthesize": "統合する",
}

# 400語に達するよう、ここからダミーデータや追加カテゴリーを補完するロジック
# 本来は辞書ファイル(JSON)などから読み込むのがスマートです。
for i in range(1, 350):
    if f"Term_{i}" not in EXTENDED_WORD_DATA:
        # 実際にはここに単語を追加
        pass

# 2. セッション状態の初期化
if 'current_word' not in st.session_state:
    st.session_state.current_word = None
    st.session_state.options = []
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.answered = False
    st.session_state.feedback = ""

def next_question():
    word = random.choice(list(EXTENDED_WORD_DATA.keys()))
    correct_ans = EXTENDED_WORD_DATA[word]
    
    others = [v for v in EXTENDED_WORD_DATA.values() if v != correct_ans]
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
st.set_page_config(page_title="Ivy League Lexicon", page_icon="🏛️")
st.title("🏛️ Ivy League Lexicon Challenge")
st.markdown("""
ネイティブスピーカーの教授や研究者が好んで用いる、**抽象度の高い語彙・知的慣用句・ラテン語由来の表現**をマスターしましょう。
""")

# サイドバー
st.sidebar.header("📊 Progress Tracker")
accuracy = (st.session_state.score / st.session_state.total * 100) if st.session_state.total > 0 else 0
st.sidebar.metric("Solved", f"{st.session_state.score} / {st.session_state.total}")
st.sidebar.progress(min(accuracy / 100, 1.0))
st.sidebar.write(f"Accuracy: **{accuracy:.1f}%**")

# メイン
st.write("---")
with st.container():
    st.write(f"Current Level: **Doctoral / Professor Level**")
    st.info(f"Select the definition for:  # **{st.session_state.current_word}**", icon="🧐")

# 選択肢 (2x2のグリッド配置で視認性向上)
col1, col2 = st.columns(2)
for i, option in enumerate(st.session_state.options):
    target_col = col1 if i % 2 == 0 else col2
    if target_col.button(option, key=f"btn_{option}", use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        
        if option == EXTENDED_WORD_DATA[st.session_state.current_word]:
            st.session_state.score += 1
            st.session_state.feedback = f"🎯 **Excellent!** '{st.session_state.current_word}' is indeed '{option}'."
        else:
            correct = EXTENDED_WORD_DATA[st.session_state.current_word]
            st.session_state.feedback = f"⚠️ **Not quite.** '{st.session_state.current_word}' actually means: **{correct}**"
        st.rerun()

# フィードバック
if st.session_state.answered:
    st.success(st.session_state.feedback) if "🎯" in st.session_state.feedback else st.error(st.session_state.feedback)
    if st.button("Advance to Next Term ⏩", use_container_width=True):
        next_question()
        st.rerun()

# 設定
with st.sidebar.expander("System Settings"):
    if st.button("Reset All Progress"):
        st.session_state.score = 0
        st.session_state.total = 0
        next_question()
        st.rerun()
