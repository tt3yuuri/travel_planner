from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
import pandas as pd
from  streamlit_folium import st_folium
import folium
from langchain_community.tools import DuckDuckGoSearchRun
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim  
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
from reportlab.lib.utils import simpleSplit
from fpdf import FPDF
import fitz  # PyMuPDF ライブラリ
import warnings


def main():
    llm = ChatOpenAI(temperature=0)

    st.set_page_config(
        page_title="Travel Planner",
        page_icon="🧳"
    )
    st.header("Travel Planner")
    st.text("・This site was developed to help you make the most of your vacation.")
    st.text("・First, enter the conditions you are interested in,")
    st.text("    such as your destination, gourmet food, tourist spots, etc.")
    
    # Sidebarの選択肢を定義する
    options = ["START","WEB","MAP", "MEMO", "EXIT"]
    choice = st.sidebar.selectbox("Select an option", options)

    if choice == "START":
        st.write("You selected START")
        web()
        AI()
        condition()
    elif choice == "WEB":
        st.write("You selected WEB")
        AI()
        condition_web()
    elif choice == "MAP":
        st.write("You selected MAP")
        MAP()
    elif choice == "MEMO":
        st.write("You selected MEMO")
        AI()
    else:
        st.write("You selected EXIT")
        redirect()

def redirect():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=https://www.google.com">
        <p>Redirecting...</p>
    """, unsafe_allow_html=True)
#35.68123360506802, 139.76695041934764
def MAP():
    # セッション状態で地図データを管理
    if "map_data" not in st.session_state:
        st.session_state.map_data = {
            "location": [35.6812378, 139.7669852],  # 初期位置
            "markers": []  # マーカーのリスト
        }

    # 初期地図を生成
    m = folium.Map(location=st.session_state.map_data["location"], zoom_start=16)
    m.add_child(folium.LatLngPopup())

    # 既存のマーカーを地図に追加
    for marker in st.session_state.map_data["markers"]:
        folium.Marker(location=marker, popup=f"Latitude: {marker[0]}, Longitude: {marker[1]}").add_to(m)

    # 地図をクリックしたときの処理
    st_data = st_folium(m, width=725, height=500)
    if st_data and st_data["last_clicked"] is not None:
        clicked_lat = st_data["last_clicked"]["lat"]
        clicked_lng = st_data["last_clicked"]["lng"]
        st.session_state.map_data["location"] = [clicked_lat, clicked_lng]
        st.session_state.map_data["markers"].append([clicked_lat, clicked_lng])
        st.write(f"Clicked Location: Latitude {clicked_lat}, Longitude {clicked_lng}")

    # 観光地検索フォームを表示
    st.write("観光名所を検索")
    location_name = st.text_input("観光名所名または都市名を入力してください:")

    # 観光地の検索ボタン
    if st.button("検索してマップに追加"):
        if location_name.strip():
            geolocator = Nominatim(user_agent="my_trip_planner_app")  # ユニークなuser_agentを設定
            try:
                location = geolocator.geocode(location_name, language="ja")
                if location:
                    lat, lon = location.latitude, location.longitude
                    st.session_state.map_data["location"] = [lat, lon]
                    st.session_state.map_data["markers"].append([lat, lon])
                    st.success(f"Location found: {location_name} ({lat}, {lon})")
                else:
                    st.error(f"Location '{location_name}' not found. Please check the spelling or try another location.")
            except Exception as e:
                st.error(f"An error occurred while fetching the location: {e}")
        else:
            st.warning("Please enter a location name.")
    
def web():
    # 商品名またはブランドを入力してくださいというフィールドを定義する
    user_input_web = st.text_input("国名または都市名を入力してください.入力することで、行きたい国について、少し知ることができます.詳しく知りたい場合は、下の、'Enter your question'に.")
    
    # ユーザーが入力した値があれば検索をする
    if user_input_web:
        search = DuckDuckGoSearchRun()

        # DuckDuckGoSearchRunのrunメソッドにユーザーの入力を辞書で渡す
        response = search.run({"query": user_input_web, "language": "jp"})
        st.write(response)

def AI():
    llm = ChatOpenAI(temperature=0)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a trip planner. You should provide great trip plans.")
        ]

    if user_input := st.chat_input("Enter your question:"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            st.markdown(f"**Assistant:** {message.content}")
        elif isinstance(message, HumanMessage):
            st.markdown(f"**You:** {message.content}")


def condition():
    # 国を入力させるフィールドを追加
    # 国内か海外か選択
    destination_type = st.radio("国内旅行か海外旅行か選んでください", ['国内', '海外'])

    if destination_type == '国内':
        # 国内の地方を選択
        todofuken = ["北海道", "東北地方", "関東地方", "中部地方", "近畿地方", "中国地方", "四国地方", "九州地方", "沖縄県"]
        region = st.radio("行きたい地方", todofuken)
    else:
        # 海外の州（または国）を選択
        states = ["アジア", "アフリカ", "ヨーロッパ", "北アメリカ", "南アメリカ", "オセアニア"]  # 例としていくつかの国を追加
        region = st.radio("States I want to visit", states)# デフォルトを「日本」に設定
    days = st.slider('宿泊日数', 1, 14, 1)
    people = st.radio('人数', ['1人', '2人', '3人', '4人', 'それ以上'])
    traffic = st.radio('交通', ["飛行機", "船", "新幹線", "タクシー", "レンタカー", "自家用車"])
    cost = st.sidebar.number_input("予算（円）", min_value=1000, max_value=100000000, value=10000, step=1000)

    if st.button("検索する"):
        # 入力された国を検索条件に追加
        sentence = f"{destination_type}旅行を計画しています。行きたい場所は{region},滞在日数は{days}日, 人数は{people}, 予算は{cost}円, 交通機関は{traffic}の旅行プランを計画してください。"
        question(sentence)

def condition_web():
    global sentence_duck
    # 国を入力させるフィールドを追加
    # 国内か海外か選択
    destination_type = st.radio("国内旅行か海外旅行か選んでください", ['国内', '海外'])

    if destination_type == '国内':
        # 国内の地方を選択
        todofuken = ["北海道", "東北地方", "関東地方", "中部地方", "近畿地方", "中国地方", "四国地方", "九州地方", "沖縄県"]
        region = st.radio("行きたい地方", todofuken)
    else:
        # 海外の州（または国）を選択
        states = ["アジア", "アフリカ", "ヨーロッパ", "北アメリカ", "南アメリカ", "オセアニア"]  # 例としていくつかの国を追加
        region = st.radio("States I want to visit", states)# デフォルトを「日本」に設定
    days = st.slider('宿泊日数', 1, 14, 1)
    people = st.radio('人数', ['1人', '2人', '3人', '4人', 'それ以上'])
    traffic = st.radio('交通', ["飛行機", "船", "新幹線", "タクシー", "レンタカー", "自家用車"])
    cost = st.sidebar.number_input("予算（円）", min_value=1000, max_value=100000000, value=10000, step=1000)
    other1 = st.text_area("他にもリクエストがある場合はここに記入してください。特になければ、[なし]にチェックを入れてください。",placeholder="羽田空港発で、出来れば早朝の便は避けたいです。")
    other2 = st.checkbox("なし")

    if other1:
        other0 = other1
    else:
        other0 = "なし"
    if st.button("検索する"):
        # 入力された国を検索条件に追加
        sentence_duck = f"{destination_type}旅行を計画しています。行きたい場所は{region},滞在日数は{days}日, 人数は{people}, 予算は{cost}円, 交通機関は{traffic}の旅行プランを計画してください。他のリクエストは「{other0}」です。最適な旅行プランを考えて下さい。応答は必ず日本語でお願いします。"
        duckduckgo(sentence_duck)


def generate_pdf():
    warnings.filterwarnings("ignore", category=UserWarning, module="fpdf.ttfonts")
    pdf = FPDF()
    pdf.add_page()
    font_path = os.path.abspath("C:/Users/保坂 陸太/OneDrive/デスクトップ/Travel_Planner/fonts/ipaexg.ttf")  # 実際のパスに変更
    pdf.add_font("IPAexGothic", "", font_path)

    pdf.set_font("IPAexGothic", "", size=12)

    # コンテンツを追加（ここで旅行プランなどを挿入）
    pdf.cell(200, 10, "旅行プラン内容をここに記載", align="C")
    
    # PDFをファイルとして保存
    pdf_file_path = "旅行プラン.pdf"  # 保存するファイル名
    pdf.output(pdf_file_path)  # ファイル名を指定して保存

    # メモリ上のバッファを作成してPDFを返す
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer,"S")  # バッファに出力
    pdf_buffer.seek(0)  # バッファの位置を先頭に戻す

    return pdf_file_path, pdf_buffer  # ファイルパスとバッファを返す

def check_pdf(pdf_path):
    """生成した PDF の内容をチェックする"""
    try:
        doc = fitz.open(pdf_path)
        print(f"✅ '{pdf_path}' を開きました。ページ数: {len(doc)}")

        # 各ページのテキストと画像を確認
        for page_num, page in enumerate(doc):
            text = page.get_text("text")  # テキスト抽出
            image_list = page.get_images(full=True)  # 画像リスト取得

            print(f"\n📄 Page {page_num + 1}:")
            print(f"📝 テキストの有無: {'あり' if text else 'なし'}")
            print(f"🖼 画像の数: {len(image_list)}")
            print("-" * 40)

            # テキストがあれば表示（最初の500文字）
            if text:
                print(text[:500])

        doc.close()

    except Exception as e:
        print(f"❌ PDF を開く際にエラーが発生しました: {e}")

# PDFを生成して保存
pdf_file_path, pdf_buffer = generate_pdf()
check_pdf(pdf_file_path)

def question(sentence):
    global AI_messages
    user_input = sentence+"please response in japanese. 応答は必ず日本語で生成してください"
    #print(user_input)
    st.write("この条件で検索しています・・・")
    llm = ChatOpenAI(temperature=0)
    if user_input := sentence:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
        

    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
                AI_messages = message.content
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")   
   # **ダウンロードボタンを常に表示**
    st.download_button(
    label="📄 旅行プランをダウンロード",
    data=pdf_buffer,
    file_name="旅行プラン.pdf",  # ダウンロードするファイル名
    mime="application/pdf",
)
    

# URLの中身を取得してテキストを表示する関数
def display_url_content(url):
    global sentence_duck
    try:
        # URLからウェブページのコンテンツを取得する
        response = requests.get(url)
        response.raise_for_status()  # エラーがあれば例外を投げる
        #print(response)
        # HTMLを解析する
        soup = BeautifulSoup(response.content, 'html.parser')

        # ここでは例としてすべてのテキストを抽出していますが、
        # より詳細な情報が必要であれば、HTMLの特定の部分を指定することもできます
        text = soup.get_text()

        # テキストを表示する
        
        sentence_duck_2 = f"{text}を踏まえて{sentence_duck}"
        question(sentence_duck_2)  # このテキストをChatGPTに渡すことができます
        
    except requests.RequestException as e:
        # HTTPリクエストでエラーが発生した場合の処理
        st.write("エラーが発生しました。")
        st.write(e)

# 抽出したテキストをChatGPTに入力として使用するためには、
# 関数を実装してChatGPT APIにリクエストを送信し、
# 結果を取得して表示するロジックを追加する必要があります。

def duckduckgo(sentence_duck):
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
            display_url_content(href)
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
    
    search_duckduckgo(sentence_duck)

if __name__ == '__main__':
    main()