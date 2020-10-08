# pip モジュール
import logging


# フォーマットを定義
formatter = "%(levelname)s : %(message)s"
# ログレベルを DEBUG に変更
logging.basicConfig(level=logging.DEBUG, format=formatter)

# ========================================================================== #
#  関数名：print_log
# -------------------------------------------------------------------------- #
#  説明：ログ出力
# ========================================================================== #
def print_log(log_msg):
    logging.info("%s", log_msg)
