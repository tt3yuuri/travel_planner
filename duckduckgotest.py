from duckduckgo_search import DDGS

Question = "リンゴ"
results = DDGS().text(Question,region="jp-jp",max_results=3)
print (results)