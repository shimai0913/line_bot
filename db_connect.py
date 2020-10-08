import os
import json
import time
import datetime
import calendar
import psycopg2
import pytz

from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage,
    FlexSendMessage,
    PostbackEvent,
    PostbackAction,
    Postback,
    PostbackTemplateAction,
    DatetimePickerAction,
    DatetimePickerTemplateAction,
)

import rakudasu as rakudasu

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)
line_user_key = "U88d9bc073add3169f2e41e580fa48fe7"

# ========================================================================== #
#  関数名：send_flex_message
# -------------------------------------------------------------------------- #
#  説明：フレックスメッセージ送信
# ========================================================================== #
def send_flex_message(jsonfile):
    try:
        json_open = open(jsonfile, "r")
        json_load = json.load(json_open)
        container_obj = FlexSendMessage.new_from_json_dict(json_load)
        line_bot_api.push_message(line_user_key, messages=container_obj)
    except Exception as e:
        print("=== エラー内容 ===")
        print(e)


# ========================================================================== #
#  関数名：send_m
# -------------------------------------------------------------------------- #
#  説明：一言送信
# ========================================================================== #
def send_m(msg):
    line_bot_api.push_message(line_user_key, TextSendMessage(text=msg))


# ========================================================================== #
#  関数名：get_connection
# -------------------------------------------------------------------------- #
#  説明：DB接続
# ========================================================================== #
def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    return psycopg2.connect(db_url, sslmode="require")


# ========================================================================== #
#  関数名：check_today_data
# -------------------------------------------------------------------------- #
#  説明：今日の時刻が登録されてるか確認
# ========================================================================== #
def check_today_data(flag):
    today = datetime.date.today()

    # DB 接続
    with get_connection() as conn:
        with conn.cursor() as cur:
            while True:
                try:
                    cur.execute(
                        f"SELECT start_time, end_time FROM times WHERE day = '{today}'"
                    )
                    (start_time, end_time) = cur.fetchone()

                    if flag == 1:
                        if not start_time:
                            send_m("今日何時から仕事してたの" + chr(0x100036))
                            send_flex_message("start_time.json")
                        if not end_time:
                            send_m("今日何時まで仕事してたの" + chr(0x100036))
                            send_flex_message("end_time.json")
                    if flag == 2:
                        if start_time and end_time:
                            rakudasu.add_data_rakudasu(start_time, end_time)
                            send_m(
                                "OK" + chr(0x100039) + "\nラクダスにも登録しといたよ" + chr(0x10007F)
                            )
                    if flag == 3:
                        if start_time and end_time:
                            send_m(
                                f"今日は{start_time}~{end_time}って登録されてるよ" + chr(0x10009C)
                            )
                        elif start_time and not end_time:
                            send_m(f"今日は開始時刻だけ{start_time}って登録されてるよ" + chr(0x10009C))
                        elif not start_time and end_time:
                            send_m(f"今日は終了時刻だけ{end_time}って登録されてるよ" + chr(0x10009C))
                        else:
                            send_m(f"今日はまだ登録されてない" + chr(0x100083))
                            time.sleep(2)
                            send_m("登録してきてあげるから時間教えて" + chr(0x100026))
                            send_flex_message("start_time.json")
                            send_flex_message("end_time.json")

                    break
                except:
                    cur.execute(f"INSERT INTO times (day) VALUES ('{today}')")
                    conn.commit()


if __name__ == "__main__":
    weekday = datetime.date.today().weekday()
    weekday_name = calendar.day_name[weekday]

    if weekday_name != "Saturday" and weekday_name != "Sunday":
        check_today_data(1)
