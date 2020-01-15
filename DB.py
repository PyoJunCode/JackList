from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, desc, BigInteger
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref, aliased
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import ModelSchema
from selenium import webdriver
from bs4 import BeautifulSoup
import marshmallow as ma
from flask import jsonify
import datetime
import time
import threading
import xmltodict
import re
import logging
import logging.config

import pandas as encjson
import requests
import json


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('takeattendanceLogger')

url ='mysql://root:@localhost:3306/jacklist?charset=utf8'
engine = create_engine(url, pool_size = 20, pool_recycle= 500)
Base = declarative_base()



##==================================================ORM CLASS===============================================

##FUNCTION ORDER : RAKUTEN - YAHOO - AMAZON  ,,,, CATEGORY - PRODUCT - PRODUCT RANKING
##Comments

class rakuten_Category(Base):

    __tablename__ = 'rakuten_category'
    id = Column(Integer, primary_key=True)
    genreId = Column(Integer) #category ID from API
    cateName = Column(String(50)) # category Name from API
    parentId = Column(Integer, ForeignKey('rakuten_category.id')) #parent category ID
    depth = Column(Integer) # now depth
    children = relationship('rakuten_Category', remote_side=[parentId])


    def __init__(self, genreId, cateName, parentId, depth): #init model

        self.genreId = genreId
        self.cateName = cateName
        self.parentId = parentId
        self.depth = depth

    def __repr__(self): # create table when table not exists
        return "<rakuten_Category(genreId = '%s', cateName = '%s' parentId = '%s', depth = '%s')>" % (self.genreId, self.cateName, self.parentId, self.depth)


class rakuten_Product(Base):

    __tablename__ = 'rakuten_product'
    id = Column(Integer, primary_key=True)
    itemCode = Column(String(50),  unique=True) # item code from API
    mediumImageUrls = Column(String(200)) # item image from API
    itemPrice = Column(String(50)) # itemPrice from API
    itemName = Column(String(255)) # item name from API
    itemUrl = Column(String(200)) # item URL from API
    reviewCount = Column(Integer) # item reviewCOunt from API
    reviewAverage = Column(String(5)) # item reviewAverage from API
    itemInfo = relationship('rakuten_Ranking' , back_populates='product')

    def __init__(self, itemCode, mediumImageUrls, itemPrice, itemName, itemUrl, reviewCount, reviewAverage):

        self.itemCode = itemCode
        self.mediumImageUrls = mediumImageUrls
        self.itemPrice = itemPrice
        self.itemName = itemName
        self.itemUrl = itemUrl
        self.reviewCount = reviewCount
        self.reviewAverage = reviewAverage
     


    def __repr__(self):
        return "<rakuten_Product(itemCode = '%s' mediumImageUrls = '%s', itemPrice = '%s' itemName = '%s', itemUrl='%s', reviewCount = '%s', reviewAVERAGE = '%s', genreId = '%s')>" % (self.itemCode,     self.mediumImageUrls, self.itemPrice, self.itemName, self.itemUrl, self.reviewCount, self.reviewAverage)

class rakuten_Ranking(Base):

    __tablename__ = 'rakuten_product_ranking'
    id = Column(Integer, primary_key=True)
    itemCode = Column(String(50), ForeignKey('rakuten_product.itemCode'))
    ranking = Column(Integer)
    genreId = Column(Integer)
    date = Column(BigInteger) # saved time
    product = relationship('rakuten_Product', back_populates='itemInfo', foreign_keys=[itemCode])


    def __init__(self,itemCode, ranking, genreId, date):

        self.itemCode = itemCode
        self.ranking = ranking
        self.genreId = genreId
        self.date = date


    def __repr__(self):
        return "<rakuten_Product(itemCode = '%s', ranking = '%s', genreId = '%s',date = '%s')>" % (self.itemCode, self.ranking, self.genreId, self.date)


class yahoo_Category(Base):

    __tablename__ = 'yahoo_category'
    id = Column(Integer, primary_key=True)
    genreId = Column(Integer)
    cateName = Column(String(50))
    parentId = Column(Integer, ForeignKey('yahoo_category.id'))
    depth = Column(Integer)
    children = relationship('yahoo_Category', remote_side=[parentId])


    def __init__(self, genreId, cateName, parentId, depth):

        self.genreId = genreId
        self.cateName = cateName
        self.parentId = parentId
        self.depth = depth

    def __repr__(self):
        return "<yahoo_Category(genreId = '%s', cateName = '%s' parentId = '%s', depth = '%s')>" % (self.genreId, self.cateName, self.parentId, self.depth)
 
class yahoo_Product(Base):

    __tablename__ = 'yahoo_product'
    id = Column(Integer, primary_key=True)
    itemCode = Column(String(100),  unique=True)
    mediumImageUrls = Column(String(200))
    itemPrice = Column(String(50))
    itemName = Column(String(255))
    itemUrl = Column(String(200))
    reviewCount = Column(Integer)
    reviewAverage = Column(String(5))
    
    itemInfo = relationship('yahoo_Ranking' , back_populates='product')

    def __init__(self, itemCode, mediumImageUrls, itemPrice, itemName, itemUrl, reviewCount, reviewAverage):

        self.itemCode = itemCode
        self.mediumImageUrls = mediumImageUrls
        self.itemPrice = itemPrice
        self.itemName = itemName
        self.itemUrl = itemUrl
        self.reviewCount = reviewCount
        self.reviewAverage = reviewAverage
      

    def __repr__(self):
        return "<yahoo_Product(itemCode = '%s' mediumImageUrls = '%s', itemPrice = '%s', itemName = '%s', itemUrl='%s', reviewCount = '%s', reviewAVERAGE = '%s', genreId = '%s')>" % (self.itemCode,self.mediumImageUrls,  self.itemPrice, self.itemName, self.itemUrl, self.reviewCount, self.reviewAverage)

class yahoo_Ranking(Base):

    __tablename__ = 'yahoo_product_ranking'
    id = Column(Integer, primary_key=True)
    itemCode = Column(String(100), ForeignKey('yahoo_product.itemCode'))
    ranking = Column(Integer)
    genreId = Column(Integer)
    date = Column(BigInteger)
    product = relationship('yahoo_Product', back_populates='itemInfo', foreign_keys=[itemCode])


    def __init__(self,itemCode, ranking, genreId, date):

        self.itemCode = itemCode
        self.ranking = ranking
        self.genreId = genreId
        self.date = date


    def __repr__(self):
        return "<yahoo_Ranking(itemCode = '%s', ranking = '%s', genreId = '%s',date = '%s')>" % (self.itemCode, self.ranking, self.genreId, self.date)

       
class amazon_Category(Base):

    __tablename__ = 'amazon_category'
    id = Column(Integer, primary_key=True)
    url = Column(String(150))
    cateName = Column(String(50))
    parentId = Column(Integer, ForeignKey('amazon_category.id'))
    depth = Column(Integer)
    children = relationship('amazon_Category', remote_side=[parentId])
    
    
    def __init__(self, url, cateName, parentId, depth):
    
        self.url = url
        self.cateName = cateName
        self.parentId = parentId
        self.depth = depth
    
    def __repr__(self):
        return "<amazon_Category(url = '%s', cateName = '%s' parentId = '%s', depth = '%s')>" % (self.url, self.cateName, self.parentId, self.depth)
    
class amazon_Product(Base):

    __tablename__ = 'amazon_product'
    id = Column(Integer, primary_key=True)
  
    mediumImageUrls = Column(String(200))
   
    itemName = Column(String(255), unique = True)
    itemUrl = Column(String(255))
   
    itemInfo = relationship('amazon_Ranking' , back_populates='product')
 
    def __init__(self,  mediumImageUrls,itemName, itemUrl):
 

        self.mediumImageUrls = mediumImageUrls
        self.itemName = itemName
        self.itemUrl = itemUrl

 
 
    def __repr__(self):
        return "<amazon_Product(mediumImageUrls = '%s', itemName = '%s', itemUrl='%s')>" % (   self.mediumImageUrls, self.itemName, self.itemUrl)

class amazon_Ranking(Base):

    __tablename__ = 'amazon_product_ranking'
    id = Column(Integer, primary_key=True)
    itemName = Column(String(100), ForeignKey('amazon_product.itemName'))
    ranking = Column(Integer)
    genreId = Column(Integer)
    date = Column(BigInteger)
    product = relationship('amazon_Product', back_populates='itemInfo', foreign_keys=[itemName])
    
    
    def __init__(self,itemName, ranking, genreId, date):
    
        self.itemName = itemName
        self.ranking = ranking
        self.genreId = genreId
        self.date = date
    
    
    def __repr__(self):
        return "<amazon_Ranking(itemName = '%s', ranking = '%s', genreId = '%s',date = '%s')>" % (self.itemName, self.ranking,   self.genreId, self.date)



class RankList(Base):

    __tablename__ = 'ranklist'
    id = Column(Integer, primary_key=True)
    date = Column(BigInteger)

    def __init__(self, date):
        self.date = date
    def __repr__(self):
        return "<RankList(date = '%s')>" % (self.date)



##===================================================================================

##===================================initialize model==================================

Base.metadata.create_all(engine)
session_factory = sessionmaker(autocommit = False, autoflush = False,bind = engine)
Session = scoped_session(session_factory)
session = Session()

#selenium setting
options = webdriver.ChromeOptions()
options.add_argument('headless') # for background
options.add_argument("disable-gpu")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36") # for fake agent

##========================================================================================






##================================= rakuten api links===================================================

rakuten_rankingBaseUrl = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&genreId='

rakuten_rankingParams = '&page=' # for page


rakuten_genreBaseUrl = 'https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId=' #category base url

rakuten_genreParmas = '&elements=parent%2Ccurrent%2Cchildren'#for filter api result


rakuten_appId = '&applicationId=1036855640468891236'

rakuten_root_cate = requests.get('https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId=0&elements=parent%2Ccurrent%2Cchildren&applicationId=1036855640468891236').json() # get root rakuten_Category

rakuten_cate = rakuten_root_cate['children'] # get actual categories list

#========================================== Yahoo api links ========================================

yahoo_rankingBaseUrl = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&category_id='

yahoo_itemBaseUrl = 'http://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemLookup?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&responsegroup=small&itemcode='

yahoo_genreBaseUrl ='https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categorySearch?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&category_id='

yahoo_root_cate = requests.get('https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categorySearch?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&category_id=1').json() # get root yahoo_Category

yahoo_cate = yahoo_root_cate['ResultSet']['0']['Result']['Categories']['Children']  # get actual categories list
##============================================================================================

##=============================Update Category Info===========================================


def update_rakuten_cate():

    rakuten_Category.__table__.drop(engine)
    rakuten_Category.__table__.create(engine) # drop table if already eixsts
   
    for child in rakuten_cate:# set target to category depth 1
       
        #push now category into ORM class
        addCate = rakuten_Category(
        child['child']['genreId'],
        child['child']['genreName'],
        None,
        1
        )
        #commit to DB
        session.add(
        addCate
        )
        session.commit()
        
        print('rakuten ' +str(addCate.id) + " " + child['child']['genreName'] + " completed") ## progress debug
        
        #set target to children category (depth 2)
        child2Cate = requests.get(rakuten_genreBaseUrl+str(child['child']['genreId'])+ rakuten_genreParmas +rakuten_appId).json()
        for child2 in child2Cate['children']:
            
            addCate2 = rakuten_Category(
            child2['child']['genreId'],
            "  " + child2['child']['genreName'],
            addCate.id,
            2
            )
            session.add(
            addCate2
            )
            session.commit()

                
            #=====================for 5 depth ================================================


            #            child3Cate = requests.get(rakuten_genreBaseUrl+str(child2['child']['genreId'])+rakuten_genreParmas +rakuten_appId).json()
            #            for child3 in child3Cate['children']:
            #                addCate3 = rakuten_Category(
            #                child3['child']['genreId'],
            #                "    " + child3['child']['genreName'],
            #                addCate2.id,
            #                3
            #                )
            #                session.add(
            #                addCate3
            #                )
            #                session.commit()
            #            child4Cate = requests.get(rakuten_genreBaseUrl+str(child3['child']['genreId'])+rakuten_appId).json()
            #            for child4 in child4Cate['children']:
            #                addCate4 = rakuten_Category(
            #                child4['child']['genreId'],
            #                "      " + child4['child']['genreName'],
            #                addCate3.id,
            #                4
            #                )
            #                session.add(
            #                addCate4
            #                )
            #                session.commit()
            #                child5Cate = requests.get(rakuten_genreBaseUrl+str(child4['child']['genreId'])+rakuten_appId).json()
            #                for child5 in child5Cate['children']:
            #                    addCate5 = rakuten_Category(
            #                    child5['child']['genreId'],
            #                    "        " + child5['child']['genreName'],
            #                    addCate4.id,
            #                    5
            #                    )
            #                    session.add(
            #                    addCate5
            #                    )
            #                    session.commit()


            ##============================================================================

            
 
def update_yahoo_cate():

    yahoo_Category.__table__.drop(engine)
    yahoo_Category.__table__.create(engine)

    for key,val in yahoo_cate.items():
      if(key[0] != '_'): ## filter
    
        print('yahoo ' + val['Title']['Short'] + ' id: ' + val['Id'])
        parent_id = val['Id']
        addCate = yahoo_Category(
               int(val['Id']),
               val['Title']['Short'],
               None,
               1
               )
        session.add(
        addCate
        )
        session.commit()
        depth2Cate = requests.get(yahoo_genreBaseUrl + str(parent_id)).json() # get children categories
        depth2Cate_json =depth2Cate['ResultSet']['0']['Result']['Categories']['Children'] # get list
        for key,val in depth2Cate_json.items():
          if(key[0] != '_'): ## filter
    
            print('\t'+val['Title']['Short'] + ' id: ' +val['Id']+' parent: ' +str(parent_id))
            addCate2 = yahoo_Category(
                   int(val['Id']),
                   "  " + val['Title']['Short'],
                   addCate.id,
                   2
                   )
            session.add(
            addCate2
            )
            session.commit()
     
##================for depth 3============================


     #        parent2_id = val['Id']
     #        depth3Cate = requests.get(yahoo_genreBaseUrl + str(parent2_id)).json()
     #        depth3Cate_json = depth3Cate['ResultSet']['0']['Result']['Categories']['Children']
     #        if(len(depth3Cate_json)>0):
     #          for key,val in depth3Cate_json.items():
     #            if(key[0] != '_'): ## filter
     #              i += 1
     #              print('\t\t'+val['Title']['Short'] +' parent: ' + str(parent2_id))
     #              parent_id = val['Id']
 
      
      

def update_amazon_cate():

    amazon_Category.__table__.drop(engine)
    amazon_Category.__table__.create(engine) ## drop if table exists
    
    count = 0 ## for debug
    url = 'https://www.amazon.co.jp/gp/bestsellers' #base category url
    
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
    driver.get(url)
    
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    menu = soup.select('#zg_browseRoot > ul > li > a') # css selector for menu name
    process = len(menu)
    
    for item in menu:
        count += 1
        print(item.text + ' ing...\t' + str(count) + '/' + str(process)) ## process debug
        url2 = str(item['href']) # category link
        
        addCate = amazon_Category(
        url2,
        item.text,
        None,
        1
        )
        session.add(
        addCate
        )
        session.commit()
        
#========================for depth 2==============================

        driver.get(url2) #open category link
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        menu2 = soup2.select('#zg_browseRoot > ul > ul >li > a')

        for item2 in menu2:
           # print("\t" + item2.text)
            url3 = str(item2['href'])

            addCate2 = amazon_Category(
            url3,
            item2.text,
            None,
            2
            )
            session.add(
            addCate2
            )
            
            
                
    session.commit()
    driver.quit()
    print(count)
    


##===============================update rakuten products======================
def update_rakuten_products(nowDate):

    logger.info('update_rakuten_products_start')
    progress = 0
    selectGen = session.query(rakuten_Category.genreId).all() # Load category list

    genList = [value for (value,) in selectGen]
    genList.append(0) # add root cateogry
    errorList =[]
    done = len(genList)
   
    
    for genre in genList:
      progress += 1

      for page in range(1,5): # 1~4page 120 products

        print('rakuten: ' + str(genre) + ' page '+ str(page)+ ' ing...\t' + str(progress) + '/' + str(done))
        getRanking = requests.get(rakuten_rankingBaseUrl+ str(genre) + rakuten_rankingParams + str(page) +rakuten_appId).json()
       
        #for debug
        if('error' in getRanking): # error case
          if(getRanking['error'] == 'not_found'): # error case : page not found => pass
            print('\terror in: '+str(genre) + ' page_not_found')
            errorList.append(genre)
            logger.info('\terror in: '+str(genre) + ' page_not_found')
            continue
          else: # error case : too many requests => sleep 2 second
            print('Too many requests. Sleep for 2 sec...')
            time.sleep(2)
            getRanking = requests.get(rakuten_rankingBaseUrl+ str(genre) + rakuten_rankingParams +rakuten_appId).json()

        else: # No error case
            Items = getRanking['Items']

 

            for item in Items:
                exists = session.query(rakuten_Product).filter_by(itemCode=item['Item']['itemCode'])
                title = (item['Item']['itemName'][:50] + '..') if len(item['Item']['itemName']) > 50 else item['Item']['itemName']

                if(exists.scalar()): # if product already exists
                    exists.first().itemName = title
                    exists.first().itemPrice = item['Item']['itemPrice']
                    exists.first().itemCode = item['Item']['itemCode']
                    exists.first().itemUrl = item['Item']['itemUrl']
                    exists.first().reviewCount = item['Item']['reviewCount']
                    exists.first().mediumImageUrls = item['Item']['mediumImageUrls'][0]['imageUrl']
                    exists.first().reviewAverage = item['Item']['reviewAverage']
                    session.commit()
                else: # if is new product
                    session.add(
                    rakuten_Product(
                    itemCode = item['Item']['itemCode'],
                    mediumImageUrls = item['Item']['mediumImageUrls'][0]['imageUrl'],
                    itemPrice = item['Item']['itemPrice'],
                    itemName = title,
                    itemUrl = item['Item']['itemUrl'],
                    reviewCount = item['Item']['reviewCount'],
                    reviewAverage = item['Item']['reviewAverage'],
 
                           )
                    )
                    session.commit()

                #insert Into ranking
                session.commit()
                session.add(
                rakuten_Ranking(
                       itemCode = item['Item']['itemCode'],
                       ranking = item['Item']['rank'],
                       genreId = genre,
                       date = int(nowDate)
                       )
                )
                session.commit()
               
    print('error list: ' + str(errorList))
    print('rakuten complete !!!')
    logger.info('yahoo_product_update_complete !!!')
    logger.info('error list: ' + errorItemList)

#================================ update Yahoo products======================================


def update_yahoo_products(nowDate):

    logger.info('update_yahoo_products_start')
    progress = 0
    
    selectGen = session.query(yahoo_Category.genreId).all()
   
    genList = [value for (value,) in selectGen]
    genList.append(1) # add root cateogry
    errorCateList =[]
    errorItemList = []
    done = len(genList)
    
    for genre in genList:
      progress += 1

      for page in range(0,5): # 1~4page 120 products

        print('Yahoo: '+str(genre) + ' page '+ str(page)+ ' ing...\t' + str(progress) + '/' + str(done))
        
        getRanking = requests.get(yahoo_rankingBaseUrl+ str(genre) + '&offset=' + str((page * 20))).json()
        yahoo_products = getRanking['ResultSet']['0']['Result']
        if(int(getRanking['ResultSet']['totalResultsAvailable']) != 0): # if result exists
          for key,val in yahoo_products.items():
            if(key[0] != 'R' and key[0] != '_' and key[0] != 'C'): # filter unnecessary elements
              exists = session.query(yahoo_Product).filter_by(itemCode=val['Code']) # check exists
              yahoo_itemInfo_url = requests.get(yahoo_itemBaseUrl + val['Code']).json()
              if(int(yahoo_itemInfo_url['ResultSet']['totalResultsReturned']) != 0):
               
                yahoo_itemInfo = yahoo_itemInfo_url['ResultSet']['0']['Result']['0']
                title = (val['Name'][:50] + '..') if len(val['Name']) > 50 else val['Name']
       
                if(exists.scalar()): #if exists
                    exists.first().itemName = title
                    exists.first().itemPrice = yahoo_itemInfo['Price']['_value']
                    exists.first().itemCode = val['Code']
                    exists.first().itemUrl = yahoo_itemInfo['Url']
                    exists.first().reviewCount = val['Review']['Count']
                    exists.first().mediumImageUrls = yahoo_itemInfo['Image']['Small']
                    exists.first().reviewAverage = val['Review']['Rate']
                    session.commit()
                else: # new
                    session.add(
                    yahoo_Product(
                    itemCode = val['Code'],
                    mediumImageUrls = yahoo_itemInfo['Image']['Small'],
                    itemPrice = yahoo_itemInfo['Price']['_value'],
                    itemName = title,
                    itemUrl = yahoo_itemInfo['Url'],
                    reviewCount = val['Review']['Count'],
                    reviewAverage = val['Review']['Rate']
       
                           )
                    )
                    session.commit()
                #insert Into ranking
                session.commit()
                session.add(
                yahoo_Ranking(
                       itemCode = val['Code'],
                       ranking = val['_attributes']['rank'],
                       genreId = genre,
                       date = 202001090149
                       )
                )
              else: #debug
                print(yahoo_itemInfo_url)
                logger.info('item_not_found ' + yahoo_itemInfo_url)
                errorItemList.append(val['Code'])
            session.commit()
   
             
        else: #if No result (error)
          print('There are no result for products')
          
    print('yahoo complete !!!')
    logger.info('yahoo_product_update_complete !!!')
    logger.info('error list: ' + errorItemList)

##===============================================================================================

##=================================update amazon products==============================================

def update_amazon_products(nowDate):

    progress = 0
    rss_url = 'https://am-tb.tk/amaranrss/'
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
    driver.get(rss_url)
    errorCateList = []
    list = []
    for cate in session.query(amazon_Category).all():
        dict = cate.__dict__
        dict.pop('_sa_instance_state', None)
        list.append(dict)

    done = len(list)
    print(list[33])
    for category in list:
          progress += 1
          
          if(len(category) < 1 ):
            errorCateList.append(progress)
            continue
          input_url = category['url'].rpartition('/')[0]

          print('cate: ' + category['cateName'] + '\t' + str(progress) + '/' + str(done))

          driver.find_element_by_name('url').send_keys(input_url)
          driver.find_element_by_class_name('setbutton').click()
          output_url = driver.find_element_by_name('rss').get_attribute('value')
          driver.find_element_by_name('url').clear()

          items = xmltodict.parse(requests.get(output_url).text)
          if('b' in items):
            print(items)
            errorCateList.append(category['cateName'])
          else:

            rank = 1
            id = category['id']
            for item in items['rss']['channel']['item']:
              pattern = re.compile('src="' + '.+' + '"')
              match = pattern.search(item['description'])
              if(match == None):
                continue
              url_result = match.group().split('"')[1]
              title = (item['title'][:50] + '..') if len(item['title']) > 50 else item['title']
              exists = session.query(amazon_Product).filter_by(itemName=title)
              url = item['link']
              
              if(exists.scalar()):

                 exists.first().itemName = title

                 exists.first().itemUrl = url

                 exists.first().mediumImageUrls = url_result

                 session.commit()
              else:
                 session.add(
                 amazon_Product(

                 itemName = title,
                 mediumImageUrls = url_result,
                 itemUrl = url

                        )
                 )
                 session.commit()
              session.add(
              amazon_Ranking(
              itemName = title,
              ranking = rank,
              genreId = id,
              date = nowDate
              )
              )
              rank += 1
              session.commit()
    session.commit()
    print('Complete')
    print('Error category list: ' + str(errorCateList))

##=====================================================================================================



def updateProducts():

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d%H%M')# get now date
   
    #add now date to rank date list
    session.add(
    RankList(
    date = int(nowDate)
    )
    )
    session.commit()
    
    update_rakuten_products(nowDate)
    update_yahoo_products(nowDate)
    update_amazon_products(nowDate)
    
#    th_rakuten_product = threading.Thread(target = update_rakuten_products, args=(nowDate,))
#    th_yahoo_product = threading.Thread(target = update_yahoo_products, args=(nowDate,))
#
#    th_rakuten_product.start()
#    th_yahoo_product.start()
#
#    th_rakuten_product.join()
#    th_yahoo_product.join()
    
    print('products update completed... ' + nowDate + ' data created')
    
    
def updateCategories():

    #update_rakuten_cate()
    #update_yahoo_cate()
    #update_amazon_cate()


#    th_rakuten_cate = threading.Thread(target = update_rakuten_cate)
#    th_yahoo_cate = threading.Thread(target = update_yahoo_cate)
#
#    th_rakuten_cate.start()
#    th_yahoo_cate.start()
#
#    th_rakuten_cate.join()
#    th_yahoo_cate.join()
    
    print('categories update completed')
    
    
    
    

#now = datetime.datetime.now()
#nowDate = now.strftime('%Y%m%d%H%M')

##============for testing==================

#update_rakuten_cate()
#update_rakuten_products(nowDate)
#update_yahoo_cate()
#update_yahoo_products(nowDate)
#update_amazon_cate()
#update_amazon_products(nowDate)

##=========================================

## 경고 : 카테고리가 존재해야 상품을 업데이트 할 수 있습니다.
#updateCategories()
#updateProducts()

session.commit()
session.close()




