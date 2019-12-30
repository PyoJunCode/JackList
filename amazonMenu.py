import base64
import requests
import logging
import logging.config
import json


from bs4 import BeautifulSoup

url = 'https://www.amazon.co.jp/gp/bestsellers/ref=zg_bs_tab'

req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')

menu = soup.select('#zg_browseRoot > ul >li > a')


print(menu)

