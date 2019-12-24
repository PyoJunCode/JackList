from sqlalchemy import create_engine, Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import requests
import json

url ='mysql://root:fhrmdls123@localhost:3306/rakuten?charset=utf8'
engine = create_engine(url)
Base = declarative_base()

##===================ORM CLASS=======================
class Product(Base):

    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    mediumImageUrls = Column(String(200))
    itemPrice = Column(String(50))
    itemName = Column(String(255))
    itemUrl = Column(String(200))
    reviewCount = Column(Integer)
    genreId = Column(Integer)
    
    def __repr__(self):
        return "<Product(mediumImageUrls = '%s', itemPrice = '%s' itemName = '%s', itemUrl='%s', reviewCount = '%s', genreId = '%s')>" % (self.mediumImageUrls, self.itemPrice, self.itemName, self.itemUrl, self.reviewCount, self.genreId)
        
##====================================================

##=================initialize model===================

Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

##====================================================

##================ get data from api==================

search=requests.get('https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&applicationId=1092533737641352415').json()
Items = search['Items']

##=====================================================



##================InsertSQL============================
for item in Items:
    #del(item['Item']['itemCaption'])
    #print(item['Item']['mediumImageUrls'][0]['imageUrl'])
    #print(item)
    session.add(
    Product(
    mediumImageUrls = item['Item']['mediumImageUrls'][0]['imageUrl'],
    itemPrice = item['Item']['itemPrice'],
    itemName = item['Item']['itemName'],
    itemUrl = item['Item']['itemUrl'],
    reviewCount = item['Item']['reviewCount'],
    genreId = item['Item']['genreId']
    )
    )
##======================================================
    
session.commit()
session.close()
