import streamlit as st
from  streamlit_folium import st_folium
import folium

# 地図の表示箇所とズームレベルを指定してマップデータを作成
# attr（アトリビュート）は地図右下に表示する文字列。
# デフォルトマップの場合は省略可能

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
    

if __name__ == '__main__':
  accurate_map()