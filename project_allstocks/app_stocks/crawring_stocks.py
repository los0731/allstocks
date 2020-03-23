import numpy as np
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

stocks_url = 'http://marketdata.krx.co.kr/contents/MKD/04/0404/04040200/MKD04040200.jsp'
app_directory_path = '/Users/frank.io/Documents/workplace/allstocks/project_allstocks/app_stocks/'
download_path = '{}static/csv/'.format(app_directory_path)
file_path = '{}static/csv/data.csv'.format(app_directory_path)
prefs = {"download.default_directory": download_path}

if True:  # 한국거래서 웹사이트에서 전 종목을 시총순서대로 가져오기.
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--disable-gpu')

    time.sleep(3)
    browser_1 = webdriver.Chrome('{}chromedriver'.format(
        app_directory_path), options=chrome_options)
    browser_1.implicitly_wait(3)
    browser_1.set_window_size(900, 400)
    browser_1.get(stocks_url)

    if os.path.isfile(file_path):
        os.remove(file_path)

    WebDriverWait(browser_1, 5).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.button-mdi-group button:last-child'))).click()
    time.sleep(3)

    browser_1.quit()
