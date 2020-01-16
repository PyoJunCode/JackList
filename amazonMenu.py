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
    
    url = 'https://www.amazon.co.jp/gp/bestsellers/pet-supplies/2153204051/ref=zg_bs_pg_1?ie=UTF8&pg=1'
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    #zg-ordered-list > li:nth-child(2) > span > div > span > a > div
    
    
    # #zg-ordered-list > li:nth-child(1) > span > div > div > span.a-size-small.aok-float-left.zg-badge-body.zg-badge-color > span #ranking
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    menu = soup.select('.a-list-item > div')
    #zg-ordered-list > li:nth-child(1) > span > div >/// span > a > span > div > img
    #zg-ordered-list > li:nth-child(1) > span > div > span > div.a-icon-row.a-spacing-none > a:nth-child(1) > i > span
    print(url)
    for item in  menu :
        print('title: ' + item.select('.p13n-sc-truncated')[0].text.strip())
        if(len(item.select('a.a-size-small'))>0):
          print('reviewAvg: ' + item.select('span.a-icon-alt')[0].text)
          print('reviewCnt: ' + item.select('a.a-size-small')[0].text)
        print('price: ' + item.select('.p13n-sc-price')[0].text)
        print('link: ' + item.select('a.a-link-normal')[0]['href'])
        print('img: ' + item.select('span > a > span > div > img')[0]['src'])
        print(item.select('.zg-badge-text')[0].text) #ranking
        print(' ')
        print(' ')

one()
