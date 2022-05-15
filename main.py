import os
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup

file = open('base.json', 'w+')

os.environ['MOZ_HEADLESS'] = '1'

filterName = "world"
service = Service('geckodriver')

browser = webdriver.Firefox(service=service)
browser.get(f'https://store.steampowered.com/search/?term={filterName}')

result = dict()


def parse(src: str):
    global result
    bs4 = BeautifulSoup(src, "lxml")
    for page in bs4.find_all(class_='search_result_row'):
        name = page.find(class_='title').text
        result[name] = dict()
        result[name]['date'] = page.find(class_='col search_released responsive_secondrow').text
        try:
            price = "".join(filter(lambda x: x.isascii() and not x == '\n',
                                   page.find(class_='col search_price discounted responsive_secondrow').text))
            print(price)
            result[name]['price'] = list(filter(lambda x:x != '', price.strip().split('p.')))

        except AttributeError:
            result[name]['price'] = 'None'


for i in range(100):
    parse(browser.page_source)
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')

file.write(json.dumps(result))
file.close()

browser.close()
