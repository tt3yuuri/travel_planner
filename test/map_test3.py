import streamlit as st
import folium
from streamlit_folium import st_folium

# 複数の場所のデータ
locations = [
    {"name": "東京タワー", "lat": 35.6586, "lon": 139.7454},
    {"name": "浅草寺", "lat": 35.7148, "lon": 139.7967},
    {"name": "秋葉原", "lat": 35.6984, "lon": 139.7745}
]

# 地図を作成
m = folium.Map(location=[35.6586, 139.7454], zoom_start=12)

# 各場所にマーカーを追加
for location in locations:
    folium.Marker([location['lat'], location['lon']], popup=location['name']).add_to(m)

# 地図をStreamlitに表示
st_folium(m, width=700)
