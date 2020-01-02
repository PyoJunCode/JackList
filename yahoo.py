import requests
import json

resp = requests.get('https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&query=vaio').json()

print(resp['ResultSet']['0']['Result']['2'])
