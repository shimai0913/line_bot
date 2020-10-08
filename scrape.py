# 標準モジュール
import json
import requests

# pip モジュール
from bs4 import BeautifulSoup

# 自作モジュール
import log as log

# ========================================================================== #
#  関数名：getGoogleNews
# -------------------------------------------------------------------------- #
#  説明：引数wordでgoogleニューススクレイピング
# ========================================================================== #
def getGoogleNews(word):
    log.print_log("getGoogleNews start.")
    headers = {"User-Agent": "hoge"}
    url = f"https://news.google.com/search?q={word}&hl=ja&gl=JP&ceid=JP%3Aja"
    res = requests.get(url, timeout=1, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    lists = soup.find_all("h3")

    topics = []
    for i in range(5):
        title = lists[i].find("a").text  # 記事タイトルを取得
        link = "https://news.google.com" + lists[i].find("a").get("href")  # 記事リンクを取得
        topics.append(title)
        topics.append(link)
        result = "\n".join(topics)  # 改行で区切る

    log.print_log("getGoogleNews OK.")

    return result
