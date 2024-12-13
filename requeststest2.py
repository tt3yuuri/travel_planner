import streamlit as st
import requests
from bs4 import BeautifulSoup

# 1. WebページのURL
url = 'https://coloria.jp/magazine/articles/uRHcM'
# 2. requestsでWebページを取得
response = requests.get(url)
# 3. BeautifulSoupでHTMLを解析
soup = BeautifulSoup(response.text, 'html.parser')
# 4. ページ内のすべてのテキストを取得
h1_tag = soup.find('h1')
#sitename = h1_tag.get_text() h1タグのみの取得
text = soup.get_text()
# 5. 抽出したテキストを表示
#st.write(sitename)　h1タグのみ取得
st.write(text)