# 標準モジュール
import json
import sys
import os
import urllib.parse
import urllib.request
from datetime import datetime

# pipモジュール
import xmltodict
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

# 自作モジュール
import log as log

# ========================================================================== #
#  関数名：get_weather_info
# -------------------------------------------------------------------------- #
#  説明：今日、明日指定で天気関数実行
# ========================================================================== #
def weather_func():
    weather_json = get_weather_info()
    today = 0
    tomorrow = 1
    msg = set_weather_info(weather_json, today, tomorrow)
    return msg


# ========================================================================== #
#  関数名：get_weather_info
# -------------------------------------------------------------------------- #
#  説明：東京の天気取得
# ========================================================================== #
def get_weather_info():
    log.print_log("get_weather_info start.")

    url = "http://weather.livedoor.com/forecast/webservice/json/v1?city=130010"  # 東京
    try:
        html = urllib.request.urlopen(url)
        html_json = json.loads(html.read().decode("utf-8"))
        log.print_log("get_weather_info Success.")
    except Exception as e:
        log.print_log(f"get_weather_info Exception Error: {e}.")
        sys.exit(1)

    return html_json


# ========================================================================== #
#  関数名：set_weather_info
# -------------------------------------------------------------------------- #
#  説明：天気情報整形
# ========================================================================== #
def set_weather_info(weather_json, today, tomorrow):
    log.print_log("set_weather_info start.")
    weather_MAP = {
        "晴": chr(0x1000A9),
        "曇": chr(0x1000AC),
        "雨": chr(0x1000AA),
        "雪": chr(0x1000AB),
    }
    try:
        weather_today = weather_json["forecasts"][today]["telop"]
        weather_tomorrow = weather_json["forecasts"][tomorrow]["telop"]
        location = weather_json["location"]["prefecture"]  # 東京都
        time = weather_json["description"]["publicTime"]
        date = datetime.strptime(time.replace("+0900", ""), "%Y-%m-%dT%H:%M:%S")
        public_time = date.strftime("%Y/%m/%d %H:%M")  # 2020/03/10 22:32
        max_temperature = None
        min_temperature = None
        if weather_json["forecasts"][today]["temperature"]["max"] is not None:
            max_temperature = weather_json["forecasts"][today]["temperature"]["max"][
                "celsius"
            ]
        if weather_json["forecasts"][today]["temperature"]["min"] is not None:
            min_temperature = weather_json["forecasts"][today]["temperature"]["min"][
                "celsius"
            ]
        text = weather_json["description"]["text"]
    except TypeError:
        # temperature data is None etc...
        pass

    msg = "【{0}】\n{1} 現在の天気予報です。\n".format(location, public_time)
    msg = msg + "【今日】\n" + weather_today
    # if len(weather_today) > 2:
    #     msg = msg + weather_MAP[weather_today[0]] + "\n"
    # else:
    msg = (
        msg + weather_MAP[weather_today[0]] + weather_MAP[weather_today[-1]] + "\n"
        if len(weather_today) > 2
        else msg + weather_MAP[weather_today[0]] + "\n"
    )
    msg = msg + "最高 " + max_temperature + "\n" if max_temperature is not None else msg
    msg = msg + "最低 " + min_temperature + "\n" if min_temperature is not None else msg
    msg = msg + "【明日】\n" + weather_tomorrow
    msg = (
        msg
        + weather_MAP[weather_tomorrow[0]]
        + weather_MAP[weather_tomorrow[-1]]
        + "\n"
        if len(weather_tomorrow) > 2
        else msg + weather_MAP[weather_today[0]] + "\n"
    )
    # msg = msg + "【概況】\n" + text.replace('\n', '') #改行入れるか
    msg = msg + "【概況】\n" + text

    log.print_log("set_weather_info Success.")

    return msg


if __name__ == "__main__":
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
    line_bot_api = LineBotApi(channel_access_token)
    line_user_key = "U88d9bc073add3169f2e41e580fa48fe7"

    msg = weather_func()
    line_bot_api.push_message(line_user_key, TextSendMessage(text=msg))
