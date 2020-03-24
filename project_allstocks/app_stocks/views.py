from django.shortcuts import render
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


def stocks_list(request):
    return render(request, 'app_stocks/index.html', rendering_data)


# stocks list
stocks_url = 'http://marketdata.krx.co.kr/contents/MKD/04/0404/04040200/MKD04040200.jsp'
interest_rate_url = 'https://kisrating.com/ratingsStatistics/statics_spread.do'
# app_directory_path = '/Users/frank.io/Documents/workplace/allstocks/project_allstocks/app_stocks/'
app_directory_path = '                      /home/allstocks/allstocks/project_allstocks/app_stocks/'
download_path = '{}static/csv/'.format(app_directory_path)
file_path = '{}static/csv/data.csv'.format(app_directory_path)
prefs = {"download.default_directory": download_path}

if True:  # 한국거래서 웹사이트에서 전 종목을 시총순서대로 가져오기.
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--headless")

    browser_1 = webdriver.Chrome('{}chromedriver'.format(
        app_directory_path), options=chrome_options)
    browser_1.implicitly_wait(3)
    browser_1.set_window_size(900, 400)
    browser_1.get(stocks_url)

    soup = BeautifulSoup(browser_1.page_source, 'html.parser')
    stock_updated_time = soup.select(
        '.cal-area input[class="schdate"]')[0]['value']

    browser_1.quit()

time.sleep(3)
stocks_data = pd.read_csv(file_path)
all_stocks = stocks_data.loc[:, ['순위', '종목명', '종목코드', '현재가', '시가총액', '상장주식수']]
html_table_all_stocks = all_stocks.to_html(index=False)
list_stocks = []

for i in all_stocks.loc[:, '종목명']:
    list_stocks.append(i)

count_stocks = len(list_stocks)


# interest-rate spread
if True:  # 한국신용평가 웹사이트에서 회사채등급별 금리 수익률(BBB-/5년) 가져오기.
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--headless")

    browser_2 = webdriver.Chrome('{}chromedriver'.format(
        app_directory_path), options=chrome_options)
    browser_2.implicitly_wait(1)
    browser_2.set_window_size(900, 400)
    browser_2.get(interest_rate_url)

    soup = BeautifulSoup(browser_2.page_source, 'html.parser')
    interest_rate = soup.select(
        '#con_tab1 tbody tr:nth-child(11) td:last-child')[0].get_text(strip=True)
    interest_updated_date = soup.select('.date_box input#startDt')[0]['value']


# variables
rendering_data = {
    'list_stocks': list_stocks,
    'stock_updated_time': stock_updated_time,
    'count_stocks': count_stocks,
    'interest_rate': interest_rate,
    'interest_updated_date': interest_updated_date,
    'html_table_all_stocks': html_table_all_stocks,
}
