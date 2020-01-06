from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, desc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref, aliased
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import ModelSchema
import marshmallow as ma
from flask import jsonify
import datetime
import time

import pandas as encjson
import requests
import json




url ='mysql://root:fhrmdls123@localhost:3306/rakuten?charset=utf8'
engine = create_engine(url)
Base = declarative_base()


##===================ORM CLASS=======================
class rakuten_Category(Base):

    __tablename__ = 'rakuten_category'
    id = Column(Integer, primary_key=True)
    genreId = Column(Integer)
    cateName = Column(String(50))
    parentId = Column(Integer, ForeignKey('rakuten_category.id'))
    depth = Column(Integer)
    children = relationship('rakuten_Category', remote_side=[parentId])


    def __init__(self, genreId, cateName, parentId, depth):

        self.genreId = genreId
        self.cateName = cateName
        self.parentId = parentId
        self.depth = depth

    def __repr__(self):
        return "<rakuten_Category(genreId = '%s', cateName = '%s' parentId = '%s', depth = '%s')>" % (self.genreId, self.cateName, self.parentId, self.depth)

class rakuten_CateSchema(ModelSchema):
    class Meta:
        mode = rakuten_Category

class rakuten_Product(Base):

    __tablename__ = 'rakuten_product'
    id = Column(Integer, primary_key=True)
    itemCode = Column(String(50),  unique=True)
    mediumImageUrls = Column(String(200))
    itemPrice = Column(String(50))
    itemName = Column(String(255))
    itemUrl = Column(String(200))
    reviewCount = Column(Integer)
    reviewAverage = Column(String(5))
    genreId = Column(Integer)
    itemInfo = relationship('rakuten_Ranking' , back_populates='product')

    def __init__(self, itemCode, mediumImageUrls, itemPrice, itemName, itemUrl, reviewCount, reviewAverage, genreId):

        self.itemCode = itemCode
        self.mediumImageUrls = mediumImageUrls
        self.itemPrice = itemPrice
        self.itemName = itemName
        self.itemUrl = itemUrl
        self.reviewCount = reviewCount
        self.reviewAverage = reviewAverage
        self.genreId = genreId


    def __repr__(self):
        return "<rakuten_Product(itemCode = '%s' mediumImageUrls = '%s', itemPrice = '%s' itemName = '%s', itemUrl='%s', reviewCount = '%s', reviewAVERAGE = '%s', genreId = '%s')>" % (self.itemCode,     self.mediumImageUrls, self.itemPrice, self.itemName, self.itemUrl, self.reviewCount, self.reviewAverage, self.genreId)

class rakuten_Ranking(Base):

    __tablename__ = 'rakuten_product_ranking'
    id = Column(Integer, primary_key=True)
    itemCode = Column(String(50), ForeignKey('rakuten_product.itemCode'))
    ranking = Column(Integer)
    genreId = Column(Integer)
    date = Column(Integer)
    time = Column(String(10))
    product = relationship('rakuten_Product', back_populates='itemInfo', foreign_keys=[itemCode])


    def __init__(self,itemCode, ranking, genreId, date, time):

        self.itemCode = itemCode
        self.ranking = ranking
        self.genreId = genreId
        self.date = date
        self.time = time


    def __repr__(self):
        return "<rakuten_Product(itemCode = '%s', ranking = '%s', genreId = '%s',date = '%s', time = '%s')>" % (self.itemCode, self.ranking, self.genreId, self.date, self.time)


class RankList(Base):

    __tablename__ = 'ranklist'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)


    def __init__(self, date):

        self.date = date



    def __repr__(self):
        return "<rakuten_Product(date = '%s', ranking = '%s')>" % (self.date, self.ranking)


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

class yahoo_CateSchema(ModelSchema):
    class Meta:
        model = yahoo_Category
        
        

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
    date = Column(Integer)
    time = Column(String(10))
    product = relationship('yahoo_Product', back_populates='itemInfo', foreign_keys=[itemCode])


    def __init__(self,itemCode, ranking, genreId, date, time):

        self.itemCode = itemCode
        self.ranking = ranking
        self.genreId = genreId
        self.date = date
        self.time = time


    def __repr__(self):
        return "<yahoo_Product(itemCode = '%s', ranking = '%s', genreId = '%s',date = '%s', time = '%s')>" % (self.itemCode, self.ranking, self.genreId, self.date, self.time)

##====================================================




##=================initialize model===================

Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

##====================================================





##================ rakuten api links=============================

rakuten_rankingBaseUrl = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&genreId='

rakuten_rankingParams = '&page='


rakuten_genreBaseUrl = 'https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId='

rakuten_genreParmas = '&elements=parent%2Ccurrent%2Cchildren'


rakuten_appId = '&applicationId=1036855640468891236'

rakuten_root_cate = requests.get('https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId=0&elements=parent%2Ccurrent%2Cchildren&applicationId=1036855640468891236').json() # root rakuten_Category

rakuten_cate = rakuten_root_cate['children']

#=================== Yahoo api links ===========================
yahoo_rankingBaseUrl = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&category_id='

yahoo_itemBaseUrl = 'http://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemLookup?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&responsegroup=small&itemcode='

yahoo_genreBaseUrl ='https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categorySearch?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&category_id='

yahoo_root_cate = requests.get('https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categorySearch?appid=dj00aiZpPTh4SUJUQkJvRGV5ZyZzPWNvbnN1bWVyc2VjcmV0Jng9MTU-&category_id=1').json() # root yahoo_Category

yahoo_cate = yahoo_root_cate['ResultSet']['0']['Result']['Categories']['Children']
##==============================================================

##=====================Update rakuten_Category Info==============
def update_yahoo_cate():
    
    for key,val in yahoo_cate.items():
      if(key[0] != '_'): ## filter
       
        print(val['Title']['Short'] + ' id: ' + val['Id'])
        parent_id = val['Id']
        addCate = yahoo_Category(
               int(val['Id']),
               val['Title']['Short'],
               1,
               1
               )
        session.add(
        addCate
        )
        session.commit()
        depth2Cate = requests.get(yahoo_genreBaseUrl + str(parent_id)).json()
        depth2Cate_json = depth2Cate['ResultSet']['0']['Result']['Categories']['Children']
        for key,val in depth2Cate_json.items():
          if(key[0] != '_'): ## filter
          
            print('\t'+val['Title']['Short'] + ' id: ' +val['Id']+' parent: ' + str(parent_id))
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
            
    
    #        parent2_id = val['Id']
    #        depth3Cate = requests.get(yahoo_genreBaseUrl + str(parent2_id)).json()
    #        depth3Cate_json = depth3Cate['ResultSet']['0']['Result']['Categories']['Children']
    #        if(len(depth3Cate_json)>0):
    #          for key,val in depth3Cate_json.items():
    #            if(key[0] != '_'): ## filter
    #              i += 1
    #              print('\t\t'+val['Title']['Short'] +' parent: ' + str(parent2_id))
    #              parent_id = val['Id']
    



def update_rakuten_cate():
   
    for child in rakuten_cate:
       
        #print(child['child']['genreName'] + " id: " + str(child['child']['genreId']) + " depth : 1" +     "\n")
        addCate = rakuten_Category(
        child['child']['genreId'],
        child['child']['genreName'],
        None,
        1
        )
        session.add(
        addCate
        )
        session.commit()
        print(str(addCate.id) + " " + child['child']['genreName'] + " completed") ## progress debug
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


##===============================update rakuten products======================
def update_rakuten_products():

    #filter = session.query(rakuten_Product).filter(rakuten_Category.parentId==1).join(rakuten_Category.parentId, aliased=True).filter(rakuten_Category.id==1)
    progress = 0
    selectGen = session.query(rakuten_Category.genreId).all()

    genList = [value for (value,) in selectGen]
    genList.append(0) # add root cateogry
    errorList =[]
    done = len(genList)
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')
    nowTime = now.strftime('%H:%M')
    
    
    for genre in genList:
      progress += 1

      for page in range(1,5): # 1~4page 120 products

        print(str(genre) + ' page '+ str(page)+ ' ing...\t' + str(progress) + '/' + str(done))
        getRanking = requests.get(rakuten_rankingBaseUrl+ str(genre) + rakuten_rankingParams + str(page) +rakuten_appId).json()
        #for debug
        if('error' in getRanking):
          if(getRanking['error'] == 'not_found'):
            print('\terror in: '+str(genre) + ' page_not_found')
            errorList.append(genre)
            continue
          else:
            print('Too many requests. Sleep for 2 sec...')
            time.sleep(2)
            getRanking = requests.get(rakuten_rankingBaseUrl+ str(genre) + rakuten_rankingParams +rakuten_appId).json()

        else:
            Items = getRanking['Items']

 

            for item in Items:
                exists = session.query(rakuten_Product).filter_by(itemCode=item['Item']['itemCode'])

                if(exists.scalar()):
                    exists.first().itemName = item['Item']['itemName']
                    exists.first().itemPrice = item['Item']['itemPrice'],
                    exists.first().itemCode = item['Item']['itemCode']
                    exists.first().itemUrl = item['Item']['itemUrl']
                    exists.first().reviewCount = item['Item']['reviewCount']
                    exists.first().genreId = item['Item']['genreId']
                    exists.first().mediumImageUrls = item['Item']['mediumImageUrls'][0]['imageUrl']
                    exists.first().reviewAverage = item['Item']['reviewAverage']
                    session.commit()
                else:
                    session.add(
                    rakuten_Product(
                    itemCode = item['Item']['itemCode'],
                    mediumImageUrls = item['Item']['mediumImageUrls'][0]['imageUrl'],
                    itemPrice = item['Item']['itemPrice'],
                    itemName = item['Item']['itemName'],
                    itemUrl = item['Item']['itemUrl'],
                    reviewCount = item['Item']['reviewCount'],
                    reviewAverage = item['Item']['reviewAverage'],
                    genreId = item['Item']['genreId']
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
                       date = int(nowDate),
                       time = nowTime
                       )
                )
                session.commit()

    session.add(
    RankList(
    date = int(nowDate)
    )
    )
    session.commit()
    print('error list: ' + str(errorList))
    print('complete !!!')

#================================update Yahoo products======================================


def update_yahoo_product():

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')
    nowTime = now.strftime('%H:%M')

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

        print(str(genre) + ' page '+ str(page)+ ' ing...\t' + str(progress) + '/' + str(done))
        
        getRanking = requests.get(yahoo_rankingBaseUrl+ str(genre) + '&offset=' + str((page * 20))).json()
        yahoo_products = getRanking['ResultSet']['0']['Result']
        if(int(getRanking['ResultSet']['totalResultsAvailable']) != 0):
          for key,val in yahoo_products.items():
            if(key[0] != 'R' and key[0] != '_' and key[0] != 'C'):
              exists = session.query(yahoo_Product).filter_by(itemCode=val['Code'])
              yahoo_itemInfo_url = requests.get(yahoo_itemBaseUrl + val['Code']).json()
              if(int(yahoo_itemInfo_url['ResultSet']['totalResultsReturned']) != 0):
               
                yahoo_itemInfo = yahoo_itemInfo_url['ResultSet']['0']['Result']['0']
                
       
                if(exists.scalar()):
                    exists.first().itemName = val['Name']
                    exists.first().itemPrice = yahoo_itemInfo['Price']['_value']
                    exists.first().itemCode = val['Code']
                    exists.first().itemUrl = yahoo_itemInfo['Url']
                    exists.first().reviewCount = val['Review']['Count']
                    exists.first().mediumImageUrls = yahoo_itemInfo['Image']['Small']
                    exists.first().reviewAverage = val['Review']['Rate']
                    session.commit()
                else:
                    session.add(
                    yahoo_Product(
                    itemCode = val['Code'],
                    mediumImageUrls = yahoo_itemInfo['Image']['Small'],
                    itemPrice = yahoo_itemInfo['Price']['_value'],
                    itemName = val['Name'],
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
                       date = int(nowDate),
                       time = nowTime
                       )
                )
              else: #debug
                print(yahoo_itemInfo_url)
                errorItemList.append(val['Code'])
            session.commit()
             
        else: #debug
          print(getRanking)
    print('complete !!!')

    
    
def test():
    #filter = session.query(rakuten_Ranking).filter(rakuten_Ranking.genreId==101381).join(rakuten_Product.itemName, aliased=True).filter(rakuten_Product.genreId=='101381')
    order = session.query(RankList).order_by(desc('date')).first().date
    print(str(order))


#test()
#update_rakuten_cate()
#update_rakuten_products()
#update_yahoo_cate()
update_yahoo_product()


session.commit()
session.close()




