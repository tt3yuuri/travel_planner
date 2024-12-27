import streamlit as st

def pills(): 
    # 複数選択肢のリスト
    pill_options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']

    # 複数選択を可能にする
    selected_pills = st.multiselect('複数選択してください', pill_options)

    # 選択されたオプションを表示
    st.write(f"選択されたオプション: {selected_pills}")

pills()