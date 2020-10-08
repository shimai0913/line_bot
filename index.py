# 標準モジュール
import os
import datetime

# pipモジュール
import psycopg2
import pytz
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    ImageMessage,
    AudioMessage,
    LocationMessage,
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    LeaveEvent,
    PostbackEvent,
)

# 自作モジュール
import station as station
import check_word as check_word
import reply as reply
import m4a_to_wav as m4a_to_wav
import db_connect as db_connect


app = Flask(__name__)

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


# テキスト
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    check_word.check_word(event, event.message.text)


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    lat = event.message.latitude  # 緯度
    lon = event.message.longitude  # 経度
    (
        url,
        station_list,
        direction_distance_min,
        direction_distance_kilo,
    ) = station.get_near_station(lat, lon)
    reslut_list = [station_list, direction_distance_min, direction_distance_kilo]
    reply.reply(event, "location", reslut_list)


# 画像
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    # message_idから画像のバイナリデータを取得
    image_content = line_bot_api.get_message_content(event.message.id)
    reply.reply(event, "image", None)


# 音声メッセージ
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    voice_content = line_bot_api.get_message_content(event.message.id)
    m4a_to_wav.save_m4a_file(voice_content)
    m4a_to_wav.make_wav_file()
    text = m4a_to_wav.to_googleSpeechApi()

    if text:
        reply.reply(event, "voice_t", text)
    else:
        reply.reply(event, "voice_f", text)


# フォロー
@handler.add(FollowEvent)
def handle_follow(event):
    reply.reply(event, "test", "フォローさんきゅー！")


# Postback
@handler.add(PostbackEvent)
def handle_postback(event):
    today = datetime.date.today()
    if event.postback.data == "start_time":
        with db_connect.get_connection() as conn:
            with conn.cursor() as cur:
                data = event.postback.params["time"]
                cur.execute(
                    f"UPDATE times SET start_time = '{data}' WHERE day = '{today}'"
                )
                conn.commit()
                db_connect.send_m(f"{data}から" + chr(0x100027))
                db_connect.check_today_data(2)
    if event.postback.data == "end_time":
        with db_connect.get_connection() as conn:
            with conn.cursor() as cur:
                data = event.postback.params["time"]
                cur.execute(
                    f"UPDATE times SET end_time = '{data}' WHERE day = '{today}'"
                )
                db_connect.send_m(f"{data}ね" + chr(0x100035) + "りょーかい" + chr(0x10002A))
                conn.commit()
                db_connect.check_today_data(2)


# create table times (id serial PRIMARY KEY, day DATE default Null, start_time text default Null, end_time text default Null);
# INSERT INTO times (day, start_time, end_time) VALUES ('2020-07-02', '8:55', '19:00');
# INSERT INTO times (day) VALUES ('2020-07-02');
# SELECT start_time, end_time FROM times WHERE day = '2020-07-02';
# UPDATE times SET start_time = '{data}' WHERE day = {today};
# UPDATE times SET start_time = '9:00' WHERE day = '2020-07-02';

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
