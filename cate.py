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
class Category(Base):

    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    genreId = Column(Integer)
    cateName = Column(String(50))
    parentId = Column(Integer, ForeignKey('category.id'))
    depth = Column(Integer)
    children = relationship("Category",
     backref=backref('parent', remote_side=[id]))
    
    def __init__(self, genreId, cateName, parent, depth):
      
        self.genreId = genreId
        self.cateName = cateName
        self.parent = parent
        self.depth = depth

    def __repr__(self):
        return "<Category(genreId = '%s', cateName = '%s' parent = '%s', depth = '%s')>" % (self.genreId, self.cateName, self.parent, self.depth)
        

##====================================================

##=================initialize model===================

Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

##====================================================

##================ get data from api==================
baseUrl = 'https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId='
appId = '&elements=parent%2Ccurrent%2Cchildren&applicationId=1036855640468891236'



search=requests.get('https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId=0&elements=parent%2Ccurrent%2Cchildren&applicationId=1036855640468891236').json() # women

cate = search['children']
i = 0
##=====================================================

##=====================Update Category Info==============================
for child in cate:
    i+=1
    #print(child['child']['genreName'] + " id: " + str(child['child']['genreId']) + " depth : 1" + "\n")
    addCate = Category(
    child['child']['genreId'],
    child['child']['genreName'],
    0,
    1
    )
    session.add(
    addCate
    )
    session.commit()
    print(str(addCate.id) + " " + child['child']['genreName'] + " completed") ## progress debug
    child2Cate = requests.get(baseUrl+str(child['child']['genreId'])+appId).json()
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
        child3Cate = requests.get(baseUrl+str(child2['child']['genreId'])+appId).json()
        
        for child3 in child3Cate['children']:
            addCate3 = Category(
            child3['child']['genreId'],
            "    " + child3['child']['genreName'],
            addCate2.id,
            3
            )
            session.add(
            addCate3
            )
            session.commit()
            child4Cate = requests.get(baseUrl+str(child3['child']['genreId'])+appId).json()
            for child4 in child4Cate['children']:
                addCate4 = Category(
                child4['child']['genreId'],
                "      " + child4['child']['genreName'],
                addCate3.id,
                4
                )
                session.add(
                addCate4
                )
                session.commit()
                child5Cate = requests.get(baseUrl+str(child4['child']['genreId'])+appId).json()
                for child5 in child5Cate['children']:
                    addCate5 = Category(
                    child5['child']['genreId'],
                    "        " + child5['child']['genreName'],
                    addCate4.id,
                    5
                    )
                    session.add(
                    addCate5
                    )
                    session.commit()
           
##=====================================================================================

session.close()
