import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pickle
from pyquery import PyQuery as pq
from openpyxl import Workbook, load_workbook

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
url = 'https://taobao.com'


def get_cookie(url):
    browser.get(url)
    time.sleep(30)
    cookies = browser.get_cookies()
    with open('cookie.txt', 'wb') as f:
        pickle.dump(cookies, f)
    print('Get Cookies')


def set_cookie(url):
    browser.get(url)
    browser.delete_all_cookies()
    with open('cookie.txt', 'rb') as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        browser.add_cookie(cookie)
        print(cookie)

def search(url, keyword):
        browser.get(url)
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        input.send_keys(keyword)
        submit.click()

def parse_page():
    wait.until = (
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist'))
    )
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    product_value = []
    for item in items:
        product = {
            'name': item.find('.title').text(),
            'price': item.find('.price').text(),
            'shop': item.find('.shop').text(),
        }
        product_value.append(product)
    print(product_value)
    return product_value

def download_message(message):

    wb = load_workbook('products.xlsx')
    ws = wb.active
    ws.cell(row=1, column=1, value='name')
    ws.cell(row=1, column=2, value='price')
    ws.cell(row=1, column=3, value='shop')
    for x in range(2, len(message) + 2):
        ws.cell(column=1, row=x, value=message[x - 2]['name'])
    for x in range(2, len(message) + 2):
        ws.cell(column=2, row=x, value=message[x - 2]['price'])
    for x in range(2, len(message) + 2):
        ws.cell(column=3, row=x, value=message[x - 2]['shop'])

    wb.save('products.xlsx')

def main():
    #get_cookie(url)
    #set_cookie(url)

    browser.get(url)
    print('请手动登陆用户')
    time.sleep(40)

    print('开始搜索页面')
    search(url, 'Macbook PRO')
    product_message = parse_page()
    download_message(product_message)

if __name__ == '__main__':
    main()

