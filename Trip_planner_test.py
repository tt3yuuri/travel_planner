import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
import pandas as pd

def redirect():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=https://www.google.com">
        <p>リダイレクトしています...</p>
    """, unsafe_allow_html=True)


# 緯度と経度を設定
latitude = -35.681236 # 例として東京駅の緯度
longitude = 139.767125 # 例として東京駅の経度

# 緯度と経度から地図用のデータフレームを作成
data = pd.DataFrame()

# 地図を表示
def Chat(llm):

    # チャット履歴の初期化
        if "messages" not in st.session_state:
            st.session_state.messages = [
                SystemMessage(content="You are a trip planner and can provide you with great trip plans.")
        ]

        # ユーザーの入力を監視
        if user_input := st.chat_input("聞きたいことを入力して下さい"):
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("ChatGPT is typing ..."):
                response = st.llm(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))

        # チャット履歴の表示
        messages = st.session_state.get('messages', [])
        for message in messages:
            if isinstance(message, AIMessage):
                with st.chat_message('assistant'):
                    st.markdown(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message('user'):
                    st.markdown(message.content)
            #else:  # isinstance(message, SystemMessage):
                #st.write(f"System message: {message.content}")


def main():
    llm = ChatOpenAI(temperature=0)

    st.set_page_config(
        page_title="Trip Planner",
        page_icon="🧳"
    )
    st.header("Trip Planner")
    st.text("・このサイトは、皆さんのバカンスを最高なものにするために開発されました。")
    st.text("・まずは目的地.グルメ.観光地などの気になる条件から入力してみましょう！")

    # Sidebarの選択肢を定義する
    
    
# Sidebarの選択肢を定義する
    options = ["START","MAP", "MEMO", "EXIT"]
    choice = st.sidebar.selectbox("Select an option", options)
    budget = st.sidebar.number_input("予算（円）", min_value=1000, max_value=100000000, value=10000, step=1000)
    date = st.date_input("Pick a date")
    days = st.radio(
        'How many days will you stay?', 
        ['1', '2', '3', '4', '5',]
    )
    traffic = st.radio(
        'Which transportation', 
        ['飛行機', '船', '新幹線', 'タクシー', 'レンタカー','マイカー']
    )
    num_of_people = st.radio(
        'How many people?', 
        ['1', '2', '3', '4', '5',]
    )
    # Mainコンテンツの表示を変える

    if  choice == "START":
        st.write("You selected START")
        
        st.write("滞在日数:",days)
        st.write("人数:",num_of_people)
        st.write("予算:",budget)
        st.write("交通機関:",traffic)
        st.write("日付:",date)
        if st.button('Search for this content'):
            search_contents = ("滞在日数は",days,"日,",
                              "人数は",num_of_people,"人,","予算は",budget,"円,",
                              "交通機関は",traffic,"の旅行プランを計画してください")
            
            if "messages" not in st.session_state:
                st.session_state.messages = [
                SystemMessage(content="You are a trip planner and can provide you with great trip plans.")
        ]
            llm = ChatOpenAI(temperature=0)
            st.session_state.messages.append(HumanMessage(content=search_contents))
            with st.spinner("ChatGPT is typing ..."):
                response = st.llm(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))

            messages = st.session_state.get('messages', [])

            for message in messages:
                if isinstance(message, AIMessage):
                    with st.chat_message('assistant'):
                        st.markdown(message.content)
                elif isinstance(message, HumanMessage):
                    with st.chat_message('user'):
                        st.markdown(message.content)

    elif choice == "MAP":
        st.write("You selected MAP")
        st.map(data)
    elif choice == "MEMO":
        st.write("You selected MEMO")
        Chat()
    else:
        st.write("You selected EXIT")
        redirect()
    

if __name__ == '__main__':
    main()
