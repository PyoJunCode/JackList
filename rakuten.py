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
class Category(Base):

    __tablename__ = 'rakuten_category'
    id = Column(Integer, primary_key=True)
    genreId = Column(Integer)
    cateName = Column(String(50))
    parentId = Column(Integer, ForeignKey('rakuten_category.id'))
    depth = Column(Integer)
    children = relationship('Category', remote_side=[parentId])


    def __init__(self, genreId, cateName, parentId, depth):

        self.genreId = genreId
        self.cateName = cateName
        self.parentId = parentId
        self.depth = depth

    def __repr__(self):
        return "<Category(genreId = '%s', cateName = '%s' parentId = '%s', depth = '%s', parent = '%s')>" % (self.genreId, self.cateName, self.parentId, self.depth)

class CateSchema(ModelSchema):
    class Meta:
        mode = Category

class Product(Base):

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
    itemInfo = relationship('Ranking' , back_populates='product')

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
        return "<Product(itemCode = '%s' mediumImageUrls = '%s', itemPrice = '%s' itemName = '%s', itemUrl='%s', reviewCount = '%s', reviewAVERAGE = '%s', genreId = '%s')>" % (self.itemCode,     self.mediumImageUrls, self.itemPrice, self.itemName, self.itemUrl, self.reviewCount, self.reviewAverage, self.genreId)

class Ranking(Base):

    __tablename__ = 'rakuten_product_ranking'
    id = Column(Integer, primary_key=True)
    itemCode = Column(String(50), ForeignKey('rakuten_product.itemCode'))
    ranking = Column(Integer)
    genreId = Column(Integer)
    date = Column(Integer)
    time = Column(String(10))
    product = relationship('Product', back_populates='itemInfo', foreign_keys=[itemCode])


    def __init__(self,itemCode, ranking, genreId, date, time):

        self.itemCode = itemCode
        self.ranking = ranking
        self.genreId = genreId
        self.date = date
        self.time = time


    def __repr__(self):
        return "<Product(itemCode = '%s', ranking = '%s', genreId = '%s',date = '%s', time = '%s')>" % (self.itemCode, self.ranking, self.genreId, self.date, self.time)


class RankList(Base):

    __tablename__ = 'rakuten_ranklist'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)


    def __init__(self, date):

        self.date = date



    def __repr__(self):
        return "<Product(date = '%s', ranking = '%s')>" % (self.date, self.ranking)

##====================================================

##=================initialize model===================

Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

##====================================================

##================ get data from api==================

rankingBaseUrl = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&genreId='
rankingParams = '&page='


genreBaseUrl = 'https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId='
genreParams = '&elements=parent%2Ccurrent%2Cchildren'


appId = '&applicationId=1036855640468891236'

search=requests.get('https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId=0&elements=parent%2Ccurrent%2Cchildren&applicationId=1036855640468891236').json() # root category

cate = search['children']

##=====================================================

##=====================Update Category Info=======================================
def updateCate():
    i = 0
    for child in cate:
        i+=1
        #print(child['child']['genreName'] + " id: " + str(child['child']['genreId']) + " depth : 1" +     "\n")
        addCate = Category(
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
        child2Cate = requests.get(genreBaseUrl+str(child['child']['genreId'])+ genreParams +appId).json()
        for child2 in child2Cate['children']:

            addCate2 = Category(
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


#            child3Cate = requests.get(genreBaseUrl+str(child2['child']['genreId'])+genreParams +appId).json()
#            for child3 in child3Cate['children']:
#                addCate3 = Category(
#                child3['child']['genreId'],
#                "    " + child3['child']['genreName'],
#                addCate2.id,
#                3
#                )
#                session.add(
#                addCate3
#                )
#                session.commit()
#            child4Cate = requests.get(genreBaseUrl+str(child3['child']['genreId'])+appId).json()
#            for child4 in child4Cate['children']:
#                addCate4 = Category(
#                child4['child']['genreId'],
#                "      " + child4['child']['genreName'],
#                addCate3.id,
#                4
#                )
#                session.add(
#                addCate4
#                )
#                session.commit()
#                child5Cate = requests.get(genreBaseUrl+str(child4['child']['genreId'])+appId).json()
#                for child5 in child5Cate['children']:
#                    addCate5 = Category(
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



def updateProducts():

    #filter = session.query(Product).filter(Category.parentId==1).join(Category.parentId, aliased=True).filter(Category.id==1)
    progress = 0
    selectGen = session.query(Category.genreId).all()

    genList = [value for (value,) in selectGen]
    genList.append(0) # add root cateogry
    errorList =[]
    
    
    for genre in genList:
      progress += 1

      for page in range(1,5): # 1~4page 120 products

        print(str(genre) + ' page '+ str(page)+ ' ing...\t' + str(progress) + '/' + str(len(genList)))
        getRanking = requests.get(rankingBaseUrl+ str(genre) + rankingParams + str(page) +appId).json()
        #for debug
        if('error' in getRanking):
          if(getRanking['error'] == 'not_found'):
            print('\terror in: '+str(genre) + ' page_not_found')
            errorList.append(genre)
            continue
          else:
            print('Too many requests. Sleep for 2 sec...')
            time.sleep(2)
            getRanking = requests.get(rankingBaseUrl+ str(genre) + rankingParams +appId).json()

        else:
            Items = getRanking['Items']

            now = datetime.datetime.now()
            nowDate = now.strftime('%Y%m%d')
            nowTime = now.strftime('%H:%M')

            for item in Items:
                exists = session.query(Product).filter_by(itemCode=item['Item']['itemCode'])

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
                    Product(
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
                Ranking(
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

def test():
    #filter = session.query(Ranking).filter(Ranking.genreId==101381).join(Product.itemName, aliased=True).filter(Product.genreId=='101381')
    order = session.query(RankList).order_by(desc('date')).first().date
    print(str(order))


#test()
#updateCate()
#updateProducts()

session.commit()
session.close()
