import streamlit as st

# セッションステートを使ってボタンが押されたかどうかを追跡
if 'text' not in st.session_state:
    st.session_state.text = "最初のテキスト"  # 初期の表示テキスト

# ボタンが押されたかどうかを確認
if st.button('追加の文字を表示'):
    st.session_state.text += " 追加されたテキスト"

# 現在のテキストを表示
st.write(st.session_state.text)

import streamlit as st

# セッションステートに表示するテキストのリストを保持
if 'messages' not in st.session_state:
    st.session_state.messages = ["最初のテキスト"]  # 初期のテキストをリストで保持

# ボタンが押されたとき、新しいメッセージを追加
if st.button('次のメッセージを表示'):
    st.session_state.messages.append("新しいメッセージ")

# テキストを順番に表示
for message in st.session_state.messages:
    st.write(message)

