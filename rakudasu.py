# 標準モジュール
import os

import time
import datetime

# pipモジュール
from selenium import webdriver


def add_data_rakudasu(start_time, end_time):
    # 1.操作するブラウザを開く
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver")
    # 2.操作するページを開く
    driver.get("https://rakudasu.jp")
    # ページが完全にロードされるまで最大で5秒間待つよう指定
    driver.set_page_load_timeout(5)
    # 3.操作する要素を指定。その要素を操作する
    # メアドとパスワード欄に入力したいtextをいれる
    driver.find_element_by_id("UserMail").send_keys("s-simai@y-i-group.co.jp")
    driver.find_element_by_id("UserPass").send_keys("shimai0913")
    time.sleep(0.5)
    # ログイン
    driver.find_element_by_class_name("submitBtn").click()
    driver.set_page_load_timeout(5)
    driver.get("https://rakudasu.jp/Attendances")
    driver.set_page_load_timeout(5)
    # 4.今日の日付をクリック
    checkbox_list = driver.find_elements_by_name("checked_days")
    dt_now = datetime.datetime.now()

    today = dt_now.day
    box_day = checkbox_list[int(today) - 1]
    box_day.click()
    try:
        # 一括登録ボタンクリック
        driver.find_element_by_id("multi-registration-btn").click()
        time.sleep(1)

        # 開始、終了、休憩時間を入力
        driver.find_element_by_class_name("work-type-9").click()
        time.sleep(1)
        driver.find_element_by_name("opening_time").click()
        driver.find_element_by_name("opening_time").clear()
        driver.find_element_by_name("opening_time").send_keys(start_time)
        driver.find_element_by_class_name("ui-timepicker-close").click()
        time.sleep(1)

        driver.find_element_by_name("closing_time").click()
        driver.find_element_by_name("closing_time").clear()
        driver.find_element_by_name("closing_time").send_keys(end_time)
        driver.find_element_by_class_name("ui-timepicker-close").click()
        time.sleep(1)

        driver.find_element_by_name("break_time").click()
        driver.find_element_by_name("break_time").clear()
        driver.find_element_by_name("break_time").send_keys("01:00")
        driver.find_element_by_class_name("ui-timepicker-close").click()
        time.sleep(1)

        # 申請ボタンクリック
        driver.find_element_by_id("multi-attendance-apply").click()
    except:
        pass
