import base64
import requests
import logging
import logging.config
import json


from bs4 import BeautifulSoup

url = 'https://paypaymall.yahoo.co.jp/store/seedcoms/item/ag6-1pr/'

req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')

#menu = soup.select('dd.ItemPrice_price')
#itm > div.ItemPrice > dl > dd.ItemPrice_price

menu = soup.select('.ItemPrice_price')
print(menu)

