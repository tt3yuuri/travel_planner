import streamlit as st

#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
import pandas as pd
#from langchain.callbacks import get_openai_callback
from  streamlit_folium import st_folium
import folium
from duckduckgo_search import DDGS
import datetime

def main():
    #llm = ChatOpenAI(temperature=0)

    st.set_page_config(
        page_title="Trip Planner",
        page_icon="🧳"
    )
    st.title("旅行プランナー")
    st.text("・このサイトは、皆さんのバカンスを最高なものにするために開発されました。")
    st.text("・まずは目的地.グルメ.観光地などの気になる条件から入力してみましょう！")
    # Sidebarの選択肢を定義する
    options = ["MEMO","DUCK", "MAP", "EXIT"]
    choice = st.sidebar.selectbox("Select an option", options)
    # Mainコンテンツの表示を変える
    if choice == "MAP":
        st.write("You selected MAP")
        MAP()
    elif choice == "MEMO":
        st.write("You selected MEMO")
        condition()
        AI()
    elif choice == "DUCK":
        st.write("You selected DUCK")
        condition_DUCK()
    else:
        st.write("You selected EXIT")
        redirect()
    # チャット履歴の初期化をする
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
    def accurate_map():

        m = folium.Map(
            location=[35.17081269026154, 137.0339428258054],
            zoom_start=16,
            attr='Folium map'
        )

        # 地図上のクリックした場所にポップアップを表示する
        m.add_child(folium.LatLngPopup())

        # ユーザーのクリック情報を取得
        st_data = st_folium(m, width=725, height=500)

        # ユーザーが地図上をクリックした場合の処理
        if st_data["last_clicked"] is not None:
            clicked_lat = st_data["last_clicked"]["lat"]
            clicked_lng = st_data["last_clicked"]["lng"]

            st.write(f"クリックした場所の座標: 緯度 {clicked_lat}, 経度 {clicked_lng}")

            # 新しい地図を作成してクリックした場所にマーカーを追加
            m = folium.Map(
                location=[clicked_lat, clicked_lng],
                zoom_start=16,
                attr='Folium map'
            )
            # マーカーをクリックした場所に追加
            folium.Marker(
                location=[clicked_lat, clicked_lng],
                popup=f"Latitude: {clicked_lat}, Longitude: {clicked_lng}",
                tooltip="Click me!"
            ).add_to(m)

            # マップを再表示
            st_folium(m, width=725, height=500)

        
    accurate_map()

    

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
    global date
    min_date = datetime.date(2025, 1, 1)
    max_date = datetime.date(2030, 12, 31)
    date = st.date_input('出発日', datetime.date(2025, 1, 1), min_value=min_date, max_value=max_date)
    global date2
    min_date = datetime.date(2025, 1, 1)
    max_date = datetime.date(2030, 12, 31)
    date2 = st.date_input('到着日', datetime.date(2025, 1, 1), min_value=min_date, max_value=max_date)
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
    cost = st.text_input("予算",placeholder="(単位も表記してください。)")
    global region
    region = st.text_input("出発地",placeholder="成田空港")
    global place
    place = st.text_input("目的地",placeholder="沖縄県,フランス")

    st.write("日程：",date,"~",date2)
    st.write("人数：",people)
    st.write("交通手段：",traffic)
    st.write("予算：",cost)
    st.write("出発地：",region)
    st.write("目的地：",place)

    if st.button("検索する"):
        question()

def question():
    global date,date2,people,traffic,cost,region,place,sentence
    sentence = "滞在するのは"+str(date)+"~"+str(date2)+"日、人数は"+str(people)+"、交通手段は"+str(traffic)+"、予算は"+str(cost)+"で"+str(region)+"から出発して"+str(place)+"旅行に行きたいです。最適な旅行プランを考えて下さい。" 
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
    

def condition_DUCK():
    st.header("滞在条件の設定")
    global date
    min_date = datetime.date(2025, 1, 1)
    max_date = datetime.date(2030, 12, 31)
    date = st.date_input('出発日', datetime.date(2025, 1, 1), min_value=min_date, max_value=max_date)
    global date2
    min_date = datetime.date(2025, 1, 1)
    max_date = datetime.date(2030, 12, 31)
    date2 = st.date_input('到着日', datetime.date(2025, 1, 1), min_value=min_date, max_value=max_date)
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
    cost = st.text_input("予算","(単位も表記してください。)")
    global region
    todofuken = ["北海道地方","東北地方","関東地方","中部地方","近畿地方","中国地方","四国地方","九州地方","沖縄県"]
    region = st.selectbox("出発地",todofuken)
    global place
    place = st.radio(
        "目的地",
        ["海外","国内"]
        )
    other1 = st.text_area("他にもリクエストがある場合はここに記入してください。特になければ、[なし]にチェックを入れてください。",placeholder="羽田空港発で、出来れば早朝の便は避けたいです。")
    other2 = st.checkbox("なし")

    if other1:
        other0 = other1
    else:
        other0 = "なし"

    st.write("日程：",date,"~",date2)
    st.write("人数：",people)
    st.write("交通手段：",traffic)
    st.write("予算：",cost)
    st.write("出発地：",region)
    st.write("目的地：",place)
    st.write("リクエスト：",other0)

    global sentence_DUCK
    sentence_DUCK = str(date)+"~"+str(date2)+"の間 "+str(people)+"、交通手段は"+str(traffic)+"、予算は"+str(cost)+"で"+str(region)+"から出発して"+str(place)+"旅行に行きたいです。他のリクエストは「"+other0+"」"

    if st.button("検索する"):
        duckduckgo()


def duckduckgo():
    st.title("duckduckgo 検索結果")

    # 検索を実行する関数
    def search_duckduckgo(query):
        results = DDGS().text(query, region="jp-jp", max_results=5)
        # 検索結果があるかどうかチェックする
        if results:
            # 検索結果の最初の項目のタイトルとURLを取得する
            first_result = results[0]
            title = first_result['title']
            href = first_result['href']
            # タイトルとURLを表示する
            st.write(f"1: {title}")
            st.write(f"URL: {href}")
            # 検索結果の二番目の項目のタイトルとURLを取得する
            second_result = results[1]
            title2 = second_result['title']
            href2 = second_result['href']
            # タイトルとURLを表示する
            st.write(f"2: {title2}")
            st.write(f"URL: {href2}")
            # 検索結果の三番目の項目のタイトルとURLを取得する
            third_result = results[2]
            title3 = third_result['title']
            href3 = third_result['href']
            # タイトルとURLを表示する
            st.write(f"3: {title3}")
            st.write(f"URL: {href3}")
            anothersearch = st.button("もっと見る")
            if anothersearch:
                # 検索結果の四番目の項目のタイトルとURLを取得する
                four_result = results[3]
                title4 = four_result['title']
                href4 = four_result['href']
                # タイトルとURLを表示する
                st.write(f"4: {title4}")
                st.write(f"URL: {href4}")
                # 検索結果の四番目の項目のタイトルとURLを取得する
                five_result = results[4]
                title5 = five_result['title']
                href5 = five_result['href']
                # タイトルとURLを表示する
                st.write(f"5: {title5}")
                st.write(f"URL: {href5}")
        else:
            # 検索結果がなかった場合のメッセージを表示する
            st.write("検索結果が見つかりませんでした。")

    # 検索を実行する
    global sentence_DUCK
    search_duckduckgo(sentence_DUCK)


if __name__ == '__main__':
    main()