import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
import pandas as pd
from langchain.callbacks import get_openai_callback

def main():
    llm = ChatOpenAI(temperature=0)

    st.set_page_config(
        page_title="Trip Planner",
        page_icon="🧳"
    )
    st.title("旅行プランナー")
    st.text("・このサイトは、皆さんのバカンスを最高なものにするために開発されました。")
    st.text("・まずは目的地.グルメ.観光地などの気になる条件から入力してみましょう！")
    # Sidebarの選択肢を定義する
    options = ["MEMO", "MAP", "EXIT"]
    choice = st.sidebar.selectbox("Select an option", options)
    # Mainコンテンツの表示を変える
    if choice == "MAP":
        st.write("You selected MAP")
        MAP()
    elif choice == "MEMO":
        st.write("You selected MEMO")
        condition()
        AI()
    else:
        st.write("You selected EXIT")
        redirect()
    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a trip plannner.You should provide great trip plan.")
      ]


def redirect():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=https://www.google.com">
        <p>リダイレクトしています...</p>
    """, unsafe_allow_html=True)

def MAP():
    # 緯度と経度を設定
    latitude = 55 # 例として東京駅の緯度
    longitude = -3 # 例として東京駅の経度

    # 緯度と経度から地図用のデータフレームを作成
    data = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude]
    })
    st.map(data)
# 地図を表示

def AI():
    # ユーザーの入力を監視
    llm = ChatOpenAI(temperature=0)
    if user_input := st.chat_input("聞きたいことを入力して下さい"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            response = llm(st.session_state.messages)
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
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")
    #st.image("c:/Users/junakimichi/Pictures/Saved Picture/IMG_0356.JPG", use_column_width=True)


def condition():
    st.header("滞在条件の設定")
    global value
    value = st.slider('滞在日数', 1, 14, 1) # min, max, default
    global people
    people = st.radio(
        '人数', 
        ['1人', '2人', '3人',"4人","それ以上"]
    )
    global traffic
    traffic = st.radio(
        "交通",
        ["飛行機","船","新幹線","タクシー","レンタカー","自家用車"]
    )
    global cost
    cost = st.radio(
        "予算",
        ["1000~5000円","5000円~10000円","10000円~100000円","100000円~100000000円"]
        )
    global region
    todofuken = ["北海道地方","東北地方","関東地方","中部地方","近畿地方","中国地方","四国地方","九州地方","沖縄県"]
    region = st.selectbox("出発地",todofuken)
    global place
    place = st.radio(
        "目的地",
        ["海外","国内"]
        )

    st.write("滞在日数：",value)
    st.write("人数：",people)
    st.write("交通手段：",traffic)
    st.write("予算：",cost)
    st.write("出発地：",region)
    st.write("目的地：",place)

    if st.button("検索する"):
        question()

def question():
    global value,people,traffic,cost,region,place,sentence
    sentence = "滞在日数は"+str(value)+"日、人数は"+str(people)+"、交通手段は"+str(traffic)+"、予算は"+str(cost)+"で"+str(region)+"から出発して"+str(place)+"旅行に行きたいです。最適な旅行プランを考えて下さい。" 
    question_response()

def question_response():
    global sentence
    user_input = sentence+"please response in japanese. 応答は必ず日本語で生成してください"
    print(user_input)
    st.write("この条件で検索しています・・・")
    llm = ChatOpenAI(temperature=0)
    if user_input := sentence:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            response = llm(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")

if __name__ == '__main__':
    main()