# 標準モジュール
import os

# pipモジュール
import speech_recognition
from pydub import AudioSegment

# 自作モジュール
import log as log

# ========================================================================== #
#  関数名：save_m4a_file
# -------------------------------------------------------------------------- #
#  説明：受け取った音声データをm4aファイルとして保存
# ========================================================================== #
def save_m4a_file(content):
    log.print_log("save_m4a_file start.")
    try:
        current_dir = str(os.getcwd()) + "/audio.m4a"
        with open(current_dir, "wb") as fd:
            for chunk in content.iter_content():
                fd.write(chunk)
        os.listdir()
    except:
        pass
    log.print_log("save_m4a_file Success.")


# ========================================================================== #
#  関数名：make_wav_file
# -------------------------------------------------------------------------- #
#  説明：audio.m4aをwavに変換する
# ========================================================================== #
def make_wav_file():
    log.print_log("make_wav_file start.")
    try:
        m4a_file = AudioSegment.from_file("audio.m4a", format="m4a")
        m4a_file.export("audio.wav", format="wav")
        os.listdir()
        log.print_log("make_wav_file Success.")
    except:
        pass


# ========================================================================== #
#  関数名：make_wav_file
# -------------------------------------------------------------------------- #
#  説明：audio.wavをgoogle speech api に投げる
# ========================================================================== #
# google speech api
api_key = "AIzaSyAvhn6v5dWKpyuyj6UIV9t28W2C_GCjJlk"


def to_googleSpeechApi():
    log.print_log("to_googleSpeechApi start.")
    try:
        r = speech_recognition.Recognizer()
        with speech_recognition.AudioFile("audio.wav") as src:
            audio = r.record(src)
        text = r.recognize_google(audio, key=api_key, language="ja-JP")
        log.print_log("to_googleSpeechApi Success.")
        return text
    except:
        pass
