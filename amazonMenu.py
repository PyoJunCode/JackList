import base64
import requests
import logging
import logging.config
import json
import time

from bs4 import BeautifulSoup

def all():

    url = 'https://www.amazon.co.jp/gp/bestsellers'
    
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    #menu = soup.select('dd.ItemPrice_price')
    #itm > div.ItemPrice > dl > dd.ItemPrice_price
    #zg_browseRoot > ul > li:nth-child(1) > a
    #zg_browseRoot > ul > ul > li:nth-child(1) > a
    #zg_browseRoot > ul > ul > li:nth-child(1) > a
    menu = soup.select('#zg_browseRoot > ul > li > a')
    
    for item in menu:
        print(item['href'])
        url2 = str(item['href'])
        req2 = requests.get(url2)
        soup2 = BeautifulSoup(req2.content, 'html.parser')
    #    while len(soup2) < 70:
    #        print(len(soup2))
    #        req2 = requests.get(url2)
    #        time.sleep(1)
        print(len(soup2))
        menu2 = soup2.select('#zg_browseRoot > ul > ul >li > a')
        for item2 in menu2:
            print("\t" + item2.text)
            print(' ')
        print(' ')
    
def one():

    url = 'https://www.amazon.co.jp/gp/bestsellers/apparel'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    menu = soup.select('#zg_browseRoot > ul > ul > li > a')
    print(soup)
    for item in menu :
        print(item.text)
        
one()
