import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
import pandas as pd
from  streamlit_folium import st_folium
import folium
from langchain_community.tools import DuckDuckGoSearchRun
from duckduckgo_search import DDGS

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

    # ユーザーがクリックした地図の情報を取得
    st_data = st_folium(m, width=725, height=500)

    if st_data["last_clicked"] is not None:
        clicked_lat = st_data["last_clicked"]["lat"]
        clicked_lng = st_data["last_clicked"]["lng"]

        # 新しい座標をセッション状態に保存し、前のマーカーをクリア
        st.session_state.map_data["location"] = [clicked_lat, clicked_lng]
        st.session_state.map_data["markers"] = [[clicked_lat, clicked_lng]]

        st.write(f"Coordinates: Latitude {clicked_lat}, Longitude {clicked_lng}")

        # 新しい地図を再描画
        m = folium.Map(location=st.session_state.map_data["location"], zoom_start=16)
        folium.Marker(location=[clicked_lat, clicked_lng], popup=f"Latitude: {clicked_lat}, Longitude: {clicked_lng}").add_to(m)
        st_folium(m, width=725, height=500)
