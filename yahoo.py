import pandas as encjson
import requests
import json

resp = requests.get('https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&query=vaio').json()

cate = requests.get('https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categorySearch?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&category_id=1').json()

yahoo_genreBaseUrl ='https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categorySearch?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&category_id='

yahoo_genreParams = '&category_id='

cateChildren = cate['ResultSet']['0']['Result']['Categories']['Children']

i = 0


for key,val in cateChildren.items():
  if(key[0] != '_'): ## filter
    i += 1
    print(val['Title']['Short'] + ' id: ' + val['Id'])
    parent_id = val['Id']
    depth2Cate = requests.get(yahoo_genreBaseUrl + str(parent_id)).json()
    depth2Cate_json = depth2Cate['ResultSet']['0']['Result']['Categories']['Children']
    for key,val in depth2Cate_json.items():
      if(key[0] != '_'): ## filter
        i += 1
        print('\t'+val['Title']['Short'] + ' id: ' +val['Id']+' parent: ' + str(parent_id))
#        parent2_id = val['Id']
#        depth3Cate = requests.get(yahoo_genreBaseUrl + str(parent2_id)).json()
#        depth3Cate_json = depth3Cate['ResultSet']['0']['Result']['Categories']['Children']
#        if(len(depth3Cate_json)>0):
#          for key,val in depth3Cate_json.items():
#            if(key[0] != '_'): ## filter
#              i += 1
#              print('\t\t'+val['Title']['Short'] +' parent: ' + str(parent2_id))
#              parent_id = val['Id']


print(i)
