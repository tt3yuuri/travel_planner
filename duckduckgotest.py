from duckduckgo_search import DDGS

results = DDGS().text("ドラフト会議2024 速報",region="jp-jp",max_results=3)
print (results)