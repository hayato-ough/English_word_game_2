import streamlit as st
import random

# 1. Ensure the `words` list is defined and globally accessible.
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
    {"en": "cat", "jp" : "猫"},
    {"en": "dog", "jp" : "犬"},
    {"en": "apple", "jp" : "りんご"},
    {"en": "teacher", "jp" : "先生"},
    {"en": "student", "jp" : "生徒"}
]

# Initialize session state variables if they don't exist
# This ensures game state persists across reruns
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'current_word_pair' not in st.session_state:
    st.session_state.current_word_pair = None
if 'choices' not in st.session_state:
    st.session_state.choices = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_number' not in st.session_state:
    st.session_state.question_number = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = ''

# 2. Review `generate_new_question` function
def generate_new_question():
    selected_word_pair = random.choice(words)
    correct_japanese = selected_word_pair["jp"]

    all_japanese_words = [d["jp"] for d in words]
    incorrect_options = [jp for jp in all_japanese_words if jp != correct_japanese]
    random.shuffle(incorrect_options)

    num_choices = min(len(incorrect_options), 2) # Get up to 2 incorrect options
    chosen_incorrect_options = random.sample(incorrect_options, num_choices)

    choices = chosen_incorrect_options + [correct_japanese]
    random.shuffle(choices)

    st.session_state.current_word_pair = selected_word_pair
    st.session_state.choices = choices
    st.session_state.question_number += 1
    st.session_state.feedback = '' # Clear previous feedback

# 3. Review `process_answer` function
def process_answer(selected_choice):
    correct_japanese = st.session_state.current_word_pair["jp"]

    if selected_choice == correct_japanese:
        st.session_state.feedback = f"正解です！ '{st.session_state.current_word_pair['en']}' は '{correct_japanese}' です。"
        st.session_state.score += 1
    else:
        st.session_state.feedback = f"不正解です。'{st.session_state.current_word_pair['en']}' の正解は '{correct_japanese}' でした。"

    generate_new_question()


# 4. Verify main Streamlit application logic
st.title("英単語暗記ゲーム")

if not st.session_state.game_started:
    st.subheader("Streamlit版にようこそ！")
    st.write("下のボタンを押してゲームを開始してください。")
    if st.button("ゲーム開始"): # This button will also reset the game if re-run
        st.session_state.game_started = True
        st.session_state.score = 0
        st.session_state.question_number = 0
        st.session_state.feedback = ''
        generate_new_question()
        st.rerun() # Rerun to display the first question

if st.session_state.game_started:
    st.write(f"スコア: {st.session_state.score}")
    st.write(f"問題 {st.session_state.question_number}")

    if st.session_state.current_word_pair:
        st.write(f"### 問題: {st.session_state.current_word_pair['en']} の日本語訳は何ですか？")

        # Display choices as buttons. Streamlit reruns the script on button click.
        for i, choice in enumerate(st.session_state.choices):
            # A unique key is crucial for Streamlit buttons within a loop
            if st.button(f"{i+1}. {choice}", key=f"choice_{st.session_state.question_number}_{i}"):
                process_answer(choice)
                st.rerun() # Rerun to update the question and feedback

    if st.session_state.feedback:
        st.info(st.session_state.feedback)

    # Add a restart button while the game is ongoing
    if st.button("ゲームをリスタート"): # Reset game_started to false to show the initial start button
        st.session_state.game_started = False
        st.session_state.score = 0
        st.session_state.question_number = 0
        st.session_state.feedback = ''
        st.session_state.current_word_pair = None
        st.session_state.choices = []
        st.rerun()
