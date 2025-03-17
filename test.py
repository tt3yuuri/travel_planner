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
import pyautogui as pg

def main():
    # セッションステートに現在のページを保持
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'HOME'  # 初期ページはHOME
    
    st.set_page_config(
        page_title="Trip Planner",
        page_icon="🧳"
    )
    
    st.title("旅行プランナー")
    st.text("・このサイトは、皆さんのバカンスを最高なものにするために開発されました。")
    st.text("・まずは目的地.グルメ.観光地などの気になる条件から入力してみましょう！")
    
    # Sidebarの選択肢を定義する
    options = ["⌂ HOME", "AI", "AI_plus", "TRAFFIC", "DESTINATION", "MAP", "EXIT"]
    choice = st.sidebar.selectbox("Select an option", options)
    
    # 現在のページをセッションステートで管理
    st.session_state.current_page = choice
    
    # Mainコンテンツの表示を変える
    if st.session_state.current_page == "MAP":
        MAP()
    elif st.session_state.current_page == "⌂ HOME":
        HOME()
    elif st.session_state.current_page == "AI":
        condition()
        AI()
    elif st.session_state.current_page == "AI_plus":
        AI_plus()
    elif st.session_state.current_page == "TRAFFIC":
        DUCK_airplane()
    elif st.session_state.current_page == "DESTINATION":
        DUCK_DESTINATION()
    else:
        redirect()


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

    
# CSSファイルを読み込む関数
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def HOME():
    load_css()
    st.image("mukakinojisan.jpg", use_column_width=True)
    chooselist = [
        st.button("AI"),
        st.button("AI_plus"),
        st.button("TRAFFIC"),
        st.button("DESTINATION"),
        st.button("MAP"),
        st.button("EXIT")
    ]
    
    # ボタンが押された場合、そのページに遷移
    if chooselist[0]:
        st.session_state.current_page = "AI"
    elif chooselist[1]:
        st.session_state.current_page = "AI_plus"
    elif chooselist[2]:
        st.session_state.current_page = "TRAFFIC"
    elif chooselist[3]:
        st.session_state.current_page = "DESTINATION"
    elif chooselist[4]:
        st.session_state.current_page = "MAP"
    elif chooselist[5]:
        redirect()


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

def AI_plus():
    st.write("このページでは、AIに対して自由に質問できます。何でも聞いてみましょう!")
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
    
    # すでにセッションステートに情報が保存されていればその値を使う
    if 'date' not in st.session_state:
        st.session_state.date = datetime.date(2025, 1, 1)
    if 'date2' not in st.session_state:
        st.session_state.date2 = datetime.date(2025, 1, 1)
    if 'people' not in st.session_state:
        st.session_state.people = '1人'
    if 'traffic' not in st.session_state:
        st.session_state.traffic = '飛行機'
    if 'cost' not in st.session_state:
        st.session_state.cost = ''
    if 'region' not in st.session_state:
        st.session_state.region = ''
    if 'place' not in st.session_state:
        st.session_state.place = ''
    
    # ユーザー入力をセッションステートに保存
    min_date = datetime.date(2025, 1, 1)
    max_date = datetime.date(2030, 12, 31)
    
    st.session_state.date = st.date_input('出発日', st.session_state.date, min_value=min_date, max_value=max_date)
    st.session_state.date2 = st.date_input('到着日', st.session_state.date2, min_value=min_date, max_value=max_date)

    st.session_state.people = st.radio(
        '人数', 
        ['1人', '2人', '3人', "4人", "それ以上"],
        index=['1人', '2人', '3人', "4人", "それ以上"].index(st.session_state.people)
    )

    st.session_state.traffic = st.radio(
        "交通",
        ["飛行機", "船", "新幹線", "タクシー", "レンタカー", "自家用車"],
        index=["飛行機", "船", "新幹線", "タクシー", "レンタカー", "自家用車"].index(st.session_state.traffic)
    )

    st.session_state.cost = st.text_input("予算", value=st.session_state.cost, placeholder="(単位も表記してください。)")

    st.session_state.region = st.text_input("出発地", value=st.session_state.region, placeholder="成田空港")
    st.session_state.place = st.text_input("目的地", value=st.session_state.place, placeholder="沖縄県,フランス")

    # 現在の状態を表示
    st.write("日程：", st.session_state.date, "~", st.session_state.date2)
    st.write("人数：", st.session_state.people)
    st.write("交通手段：", st.session_state.traffic)
    st.write("予算：", st.session_state.cost)
    st.write("出発地：", st.session_state.region)
    st.write("目的地：", st.session_state.place)

    if st.button("検索する"):
        question()


        
def question():
    # セッションステートから条件を取得
    date = st.session_state.date
    date2 = st.session_state.date2
    people = st.session_state.people
    traffic = st.session_state.traffic
    cost = st.session_state.cost
    region = st.session_state.region
    place = st.session_state.place

    sentence = f"滞在するのは{date}~{date2}日、人数は{people}、交通手段は{traffic}、予算は{cost}で{region}から出発して{place}旅行に行きたいです。最適な旅行プランを考えて下さい。"
    
    question_response(sentence)


def question_response(sentence):
    st.write("この条件で検索しています・・・")
    llm = ChatOpenAI(temperature=0)
    st.session_state.messages.append(HumanMessage(content=sentence))
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



def DUCK_airplane():
    st.header("交通手段の検索")
    global date
    min_date = datetime.date(2025, 2, 1)
    max_date = datetime.date(2030, 12, 31)
    date = st.date_input('出発日', datetime.date(2025, 2, 1), min_value=min_date, max_value=max_date)
    global date2
    min_date = datetime.date(2025, 2, 1)
    max_date = datetime.date(2030, 12, 31)
    date2 = st.date_input('到着日', datetime.date(2025, 2, 1), min_value=min_date, max_value=max_date)
    global traffic
    traffic = st.radio(
        "交通",
        ["飛行機","船","新幹線","タクシー","レンタカー","自家用車"]
    )
    global region
    region = st.text_input("出発地",placeholder="成田空港")
    global place
    place = st.text_input("目的地",placeholder="沖縄県,フランス")

    st.write("日程：",date,"~",date2)
    st.write("交通手段：",traffic)
    st.write("出発地：",region)
    st.write("目的地：",place)

    global sentence_DUCK
    sentence0 = traffic+" "+region+"-"+place+"間"
    sentence_DUCK = sentence0+" "+str(date)+"~"+str(date2)
    if st.button("検索する"):
        duckduckgo()

def DUCK_DESTINATION():
    st.header("目的地の検索")
    global people
    people = st.radio(
        '人数', 
        ['1人', '2人', '3人',"4人","それ以上"]
    )
    cost = st.text_input("予算",placeholder="(単位も表記してください。)")
    place = st.text_input("目的地",placeholder="沖縄県,フランス")
    other1 = st.text_area("他にもリクエストがある場合はここに記入してください。特になければ、[なし]にチェックを入れてください。",placeholder="羽田空港発で、出来れば早朝の便は避けたいです。")
    other2 = st.checkbox("なし")

    if other1:
        other0 = other1
    else:
        other0 = "なし"

    st.write("人数：",people)
    st.write("予算：",cost)
    st.write("目的地：",place)
    st.write("リクエスト：",other0)

    global sentence_DUCK
    sensence00 = place+" "+cost+" "+other0
    sentence_DUCK = sensence00+" "+people+" おすすめ 観光地"
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
            #anothersearch = st.button("もっと見る")
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
    search_duckduckgo(query=sentence_DUCK)

def MEMO():

    # セッションステートにリストを初期化する
    if 'my_list' not in st.session_state:
        st.session_state.my_list = []

    # ユーザーが入力した値を追加する
    new_value = st.text_area('メモを入力してください。')

    if st.button("追加"):
        if new_value:
            st.session_state.my_list.append(new_value)

    # 現在のリストを表示
    st.write('保存したメモ:', st.session_state.my_list)


if __name__ == '__main__':
    main()