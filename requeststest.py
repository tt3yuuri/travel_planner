import requests
from bs4 import BeautifulSoup

# 1. WebページのURL
url = 'https://www.yahoo.co.jp/'

# 2. requestsでWebページを取得
response = requests.get(url)

# 3. BeautifulSoupでHTMLを解析
soup = BeautifulSoup(response.text, 'html.parser')

# 4. ページ内のすべてのテキストを取得
h1_tag = soup.find('h1')
print(h1_tag.get_text())

text = soup.get_text()

# 5. 抽出したテキストを表示
#print(text)
