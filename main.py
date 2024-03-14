import csv
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Chrome のヘッドレスモードを有効にする
options = Options()
options.add_argument("--headless")

# Selenium のバージョンが v4.6.0 以降 の場合は、パスを設定する必要はありません
# driver = webdriver.Chrome(
#     r"C:\Users\kawazoe\Desktop\file\webdriver\chromedriver-win64\chromedriver"
# )
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.co.jp/")

# 検索ボックスに入力
# seleniumのバージョン4.3.0から、find_element_by_*系のメソッドが廃止されて使えなくなった
# search_box = driver.find_element_by_name("q")
search_box = driver.find_element("name", "q")
search_box.send_keys("Python")

search_box.submit()

# 検索結果が表示されるまで待つ
# https://kurozumi.github.io/selenium-python/waits.html
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

csv_data = datetime.datetime.today().strftime("%Y%m%d")
csv_file_name = "csv/google_search_result_" + csv_data + ".csv"
with open(csv_file_name, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    csv_header = ["検索順位", "タイトル", "URL"]
    writer.writerow(csv_header)

    ranking = 1

    # seleniumのバージョン4.3.0から、find_element_by_*系のメソッドが廃止されて使えなくなった
    # for elem_h3 in driver.find_elements_by_xpath("//a/h3"):
    #     print(elem_h3.text)
    for elem_h3 in driver.find_elements("xpath", "//a/h3"):
        csv_list = []
        csv_list.append(str(ranking))
        csv_list.append(elem_h3.text)
        print(elem_h3.text)
        elem_a = elem_h3.find_element("xpath", "..")  # ".." は親要素を指定する
        csv_list.append(elem_a.get_attribute("href"))
        print(
            elem_a.get_attribute("href")
        )  # get_attribute(属性名)は要素の属性を取得する
        writer.writerow(csv_list)
        ranking += 1

    # vscodeのターミナルで実行すると、ブラウザが閉じてしまうので、5秒待つ
    # sleep(5)
