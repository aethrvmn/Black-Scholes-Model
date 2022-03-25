import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div',{'class':class_path})
    try:
        streamers = web_content_div[0].findall('fin-streamer')
        texts = [item.get_text() for item in streamers]
    except IndexError:
        texts=[]
    return texts


def real_time_price(stock_code):
    url = 'https://finance.yahoo.com/quote/' + stock_code +'?p=' + stock_code +'&.tsrc=fin-srch'
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, 'My(6px) Pos(r) smartphone_Mt(6px) W(100%) ')
        if texts != []:
            price, price_change = texts[0], texts[1]
        else:
            price, price_change = ['0'], ['0']
    except ConnectionError:
        price, price_change = ['1'], ['1']

    return price, price_change


Stock = ['AAPL']

print(real_time_price('AAPL'))