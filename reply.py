# 標準モジュール
import os

# pipモジュール
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageMessage,
    AudioMessage,
    AudioSendMessage,
    LocationMessage,
    MessageImagemapAction,
    ImagemapArea,
    ImagemapSendMessage,
    BaseSize,
    LocationSendMessage,
)

# ========================================================================== #
#  グローバル変数
# ========================================================================== #
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

# ========================================================================== #
#  関数名：reply
# -------------------------------------------------------------------------- #
#  説明：返信
# ========================================================================== #
def reply(event, flag, msg):
    if flag == "help":
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=msg),])

    elif flag == "news":
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=msg)])

    elif flag == "weather":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="天気ですね" + chr(0x10002D) + "\n調べてきます。。。"),
                TextSendMessage(text=msg),
            ],
        )

    elif flag == "home":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="お疲れ様です" + chr(0x10002D)),
                TextSendMessage(text="位置情報を送ってもらうと近くの駅を教えますよ" + chr(0x10008D)),
                TextSendMessage(text="line://nv/location"),
            ],
        )

    elif flag == "rakudasu":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="平日全部 9:30~18:30 で申請しておきました" + chr(0x10002D)),
        )

    elif flag == "other":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="「" + msg + "」っていう言葉はまだ勉強できてないです" + chr(0x100029) + chr(0x100098)
            ),
        )

    elif flag == "location":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=msg[0][0].text + "が一番近いですね！" + chr(0x10002D)),
                TextSendMessage(
                    text="歩いて約" + str(msg[1]) + "分。距離は約" + str(msg[2]) + "kmです。"
                ),
            ],
        )

    elif flag == "image":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="画像をありがとう"))

    elif flag == "voice_t":
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=msg),])

    elif flag == "voice_f":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="音声をありがとう" + chr(0x10002D) + "\nでも聞き取れないです（笑）"),],
        )

    elif flag == "test":
        line_bot_api.reply_message(
            event.reply_token, [TextSendMessage(text=msg),],
        )
