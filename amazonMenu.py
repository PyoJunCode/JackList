import base64
import requests
import logging
import logging.config
import json


from bs4 import BeautifulSoup

#url = 'https://www.amazon.co.jp/gp/bestsellers/ref=zg_bs_tab'
#
#req = requests.get(url)
#soup = BeautifulSoup(req.text, 'html.parser')
#
#menu = soup.select('#zg_browseRoot > ul >li > a')
#hmenu-content > ul.hmenu.hmenu-visible > li:nth-child(12) > a > div
#zg_browseRoot > ul > li:nth-child(1) > a

#print(menu)

search = requests.get('https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword=ポケットモンスター&applicationId=1036855640468891236').json()


for item in search['Items']:

   print(item['Item']['tagIds'])
   print('\n')
 
