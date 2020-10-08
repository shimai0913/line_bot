# 自作モジュール
import scrape as scrape
import weather as weather
import reply as reply
import db_connect as db_connect

# ========================================================================== #
#  関数名：check_word
# -------------------------------------------------------------------------- #
#  説明：入力wordに対してルート選択
# ========================================================================== #
def check_word(event, word):
    # ヘルプメッセージ作成
    if word == "help" or word == "ヘルプ":
        msg = f"「#○○」でニュース検索\n"
        msg += "帰るときは連絡して！\n"
        msg += "天気が知りたいときは言ってね！\n"
        msg += "voiceメッセージも勉強したよ。"
        reply.reply(event, "help", msg)

    # ニュース検索
    elif word[0] == "#":
        word = word[1:]
        result = scrape.getGoogleNews(word)
        reply.reply(event, "news", result)

    # 天気予報
    elif "天気" in word or "天気予報" in word or "てんき" in word:
        msg = weather.weather_func()
        reply.reply(event, "weather", msg)

    # 帰宅
    elif "帰る" in word or "帰り" in word or "帰って" in word:
        reply.reply(event, "home", None)

    elif "ラクダス" in word or "rakudasu" in word:
        db_connect.check_today_data(3)

    # その他 オウム返し
    else:
        reply.reply(event, "other", word)
