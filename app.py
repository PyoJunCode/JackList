from flask import Flask

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column , desc
from flask_cors import CORS
from flask import jsonify, request
from marshmallow_sqlalchemy import ModelSchema
import marshmallow as ma


import pandas as encjson
import requests
import json



url ='mysql://root:@localhost:3306/jacklist?charset=utf8mb4'


app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)




rakuten_categories = None
yahoo_categories = None
amazon_categories = None
itemRanking = None

#===========================Database Model===================================
class rakuten_Category(db.Model):

    __tablename__ = 'rakuten_category'
    id = db.Column(db.Integer, primary_key=True)
    genreId = db.Column(db.Integer)
    cateName = db.Column(db.String(50))
    parentId = db.Column(db.Integer, db.ForeignKey('rakuten_category.id'))
    depth = db.Column(db.Integer)
    children = db.relationship('rakuten_Category', remote_side=[parentId])
   
class rakuten_CateSchema(ModelSchema):
   
    class Meta(ModelSchema.Meta):
        model = rakuten_Category
        #dump_only = ('id',)

class yahoo_Category(db.Model):

    __tablename__ = 'yahoo_category'
    id = db.Column(db.Integer, primary_key=True)
    genreId = db.Column(db.Integer)
    cateName = db.Column(db.String(50))
    parentId = db.Column(db.Integer, db.ForeignKey('yahoo_category.id'))
    depth = db.Column(db.Integer)
    children = db.relationship('yahoo_Category', remote_side=[parentId])


class yahoo_CateSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = yahoo_Category
        #dump_only = ('id',)


class amazon_Category(db.Model):

     __tablename__ = 'amazon_category'
     id = Column(db.Integer, primary_key=True)
     url = Column(db.String(150))
     cateName = Column(db.String(50))
     parentId = Column(db.Integer, ForeignKey('amazon_category.id'))
     depth = Column(db.Integer)
     children = relationship('amazon_Category', remote_side=[parentId])

class amazon_CateSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = amazon_Category
        #dump_only = ('id',)

class RankList(db.Model):

    __tablename__ = 'ranklist'
    id = Column(db.Integer, primary_key=True)
    date = Column(db.BigInteger)
    lock = Column(db.Integer)


#==============================================================================

engine = create_engine(url, pool_size = 20, pool_recycle= 500)
session_factory = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Session = scoped_session(session_factory)
session = Session()

#===========================Functions==========================================

def get_date(): # get latest date
    
  try:
    session.commit()# update query date
    selected_date = ' AND r.date = ' +  str(session.query(RankList).filter_by(lock = 0).order_by(desc('date')).first().id)
  except: # if all date locked
    return ' '
  print(selected_date)
  return selected_date
    
def get_order(sort): # determine sorting method

    if(sort == '1'):
        order = ' ORDER BY itemPrice ASC'
    elif(sort == '2'):
        order = ' ORDER BY itemPrice DESC'
    elif(sort == '3'):
        order = ' ORDER BY reviewCount DESC'
    elif(sort == '4'):
        order = ' ORDER BY reviewAverage DESC'
    else:
        order = ' ORDER BY ranking ASC' ## default
        
    return order

def get_rakuten_cate(): ## load rakuten category
    
    data = rakuten_Category.query.all()
    category_schema = rakuten_CateSchema(many=True)
    output = category_schema.dump(data)
    
    return output

def get_yahoo_cate(): ## load yahoo category

    data = yahoo_Category.query.all()
    category_schema = yahoo_CateSchema(many=True)
    output = category_schema.dump(data)
    
    return output

def get_amazon_cate():## load amazon category

    data = amazon_Category.query.all()
    category_schema = amazon_CateSchema(many=True)
    output = category_schema.dump(data)
    
    return output

    

def get_rakuten_selected_ranking(data = '0', sort = '0'):
    
    
    order = get_order(sort)
    
    selected_date = get_date()
    
    ##select latest date from query
    
    
    if data == '0': # 0 means all. set category to 'ALL'
      selected_genre = str(len(rakuten_categories) + 1)
    else:
      selected_genre = data
    
    
    
    
    query = 'SELECT DISTINCT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product, r.itemCode  FROM rakuten_product AS p INNER JOIN rakuten_product_ranking AS r ON p.id = r.itemCode WHERE r.genreId = ' # join query
    
    
    data = encjson.read_sql_query(query + selected_genre + selected_date + order, engine)
  
    
    return json.loads(data.to_json(orient='records'))
    

def get_yahoo_selected_ranking(data = '0', sort = '0'):

    
    order = get_order(sort)
    
    selected_date = get_date()
     ##select latest date from query
     
     
    if data == '0': # set category to 'ALL'
      selected_genre = str(len(yahoo_categories) + 1)
    else:
      selected_genre = data
    
    
   
    
    query = 'SELECT DISTINCT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product,  r.itemCode  FROM yahoo_product AS p INNER JOIN yahoo_product_ranking AS r ON p.id = r.itemCode WHERE r.genreId = '
    
    #print(query + selected_genre + selected_date)
    data = encjson.read_sql_query(query + selected_genre + selected_date + order, engine)
    
    return json.loads(data.to_json(orient='records'))

def get_amazon_selected_ranking(data = '0', sort = '0'):

    order = get_order(sort)
    
    selected_date = get_date()
     ##select latest date from query
     
     
     
    if data == None: # amazon DON"T HAVE ALL
      data = 0
    else:
      selected_genre = data
    
    
    query = 'SELECT DISTINCT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product,  r.itemCode  FROM amazon_product AS p INNER JOIN amazon_product_ranking AS r ON p.id = r.itemCode WHERE r.genreId = '
    
   
    data = encjson.read_sql_query(query + selected_genre + selected_date + order, engine)
    
    return json.loads(data.to_json(orient='records'))


def get_rakuten_searched(keyword, arr, sort = '0'):
   
    order = get_order(sort)
    
    selected_date = get_date()

    
    list = tuple(arr) ## contain Cateogry for search

    key= str(keyword)
    params = " AND itemName LIKE '%%" + key + "%%'"
    
    if '0' in list :  # if search in ALL category
      query = 'SELECT DISTINCT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product, r.itemCode  FROM rakuten_product AS p INNER JOIN rakuten_product_ranking AS r ON p.id = r.itemCode WHERE r.genreId  '
      data = encjson.read_sql_query(query + params + selected_date + order, engine)
    else:
      query = 'SELECT DISTINCT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product, r.itemCode  FROM rakuten_product AS p INNER JOIN rakuten_product_ranking AS r ON p.id = r.itemCode WHERE r.genreId IN '
      data = encjson.read_sql_query(query + str(list) + params + selected_date + order, engine)
      
      
    return json.loads(data.to_json(orient='records'))
    

def get_yahoo_searched(keyword, arr, sort = '0'):

    order = get_order(sort)
    
    selected_date = get_date()

        
    list = tuple(arr)  ## contain Cateogry for search

    key= str(keyword)
    params = " AND itemName LIKE '%%" + key + "%%'"
    
    if '0' in list :  # if search in ALL category
      query = 'SELECT DISTINCT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product, r.itemCode  FROM yahoo_product AS p INNER JOIN yahoo_product_ranking AS r ON p.id = r.itemCode WHERE r.genreId  '
      data = encjson.read_sql_query(query + params + selected_date + order, engine)
    else:
      query = 'SELECT DISTINCT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product, r.itemCode  FROM yahoo_product AS p INNER JOIN yahoo_product_ranking AS r ON p.id = r.itemCode WHERE r.genreId IN '
      data = encjson.read_sql_query(query + str(list) + params + selected_date + order , engine)
      
    return json.loads(data.to_json(orient='records'))


def get_amazon_searched(keyword,arr, sort = '0'):
    
    
    order = get_order(sort)
    
    selected_date = get_date()

        
    list = tuple(arr)  ## contain Cateogry for search
 
    
    
    key= str(keyword)
    params = " AND p.itemName LIKE '%%" + key + "%%'"
    
    if '0' in list : # if search in ALL category
      query = 'SELECT DISTINCT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product, r.itemCode  FROM amazon_product AS p INNER JOIN amazon_product_ranking AS r ON p.id = r.itemCode WHERE r.genreId  '
      data = encjson.read_sql_query(query + params + selected_date + order, engine)
      
    else:
      query = 'SELECT DISTINCT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product, r.itemCode  FROM amazon_product AS p INNER JOIN amazon_product_ranking AS r ON p.id = r.itemCode WHERE r.genreId IN '
      data = encjson.read_sql_query(query + str(list) + params + selected_date + order, engine)
     
    
    return json.loads(data.to_json(orient='records'))
 

##========================load data =============================
def load_data():

    global rakuten_categories
    global yahoo_categories
    global amazon_categories
   
    yahoo_categories = get_yahoo_cate()
    rakuten_categories = get_rakuten_cate()
    amazon_categories = get_amazon_cate()
   
    
    print('\tData load complete !!!')

#====================================================================

#=================================Routing===========================
load_data()


@app.route('/', methods=['GET',])
def index():
    return "<html><body><h1>working!</h1></body></html>"


    
@app.route('/rakuten_cate', methods=['GET',])
def rakuten_cate():
    
    
    return jsonify(rakuten_categories)
    

@app.route('/yahoo_cate', methods=['GET',])
def yahoo_cate():
    
   
    return jsonify(yahoo_categories)
    

@app.route('/amazon_cate', methods=['GET',])
def amazon_cate():
    
    return jsonify(amazon_categories)

##@params : sort = num for sorting option, data = category id for search

@app.route('/rakuten_selected_ranking', methods=['GET',])
def rakuten_selected_ranking():
    sort = request.args.get('sortnum')
    data = request.args.get('genreId')
    if request.args.get('genreId') == '':
      data = '0'
   
    return jsonify(get_rakuten_selected_ranking(data, sort))

@app.route('/yahoo_selected_ranking', methods=['GET',])
def yahoo_selected_ranking():
    sort = request.args.get('sortnum')
    data = request.args.get('genreId')
    if request.args.get('genreId') == '':
      data = '0'
    return jsonify(get_yahoo_selected_ranking(data, sort))

@app.route('/amazon_selected_ranking', methods=['GET',])
def amazon_selected_ranking():
    sort = request.args.get('sortnum')
    data = request.args.get('genreId')
    if request.args.get('genreId') == '':
      data = '0'
    return jsonify(get_amazon_selected_ranking(data, sort))
    
@app.route('/rakuten_searched', methods=['GET', 'POST',])
def rakuten_searched():
    sort = request.args.get('sortnum')
    keyword = str(request.args.get('keyword'))
    arr = request.json
    
    return jsonify(get_rakuten_searched(keyword, arr, sort))
    

@app.route('/yahoo_searched', methods=['GET', 'POST',])
def yahoo_searched():
    sort = request.args.get('sortnum')
    keyword = str(request.args.get('keyword'))
    arr = request.json
  
    return jsonify(get_yahoo_searched(keyword,arr, sort))
    

@app.route('/amazon_searched', methods=['GET', 'POST',])
def amazon_searched():
    sort = request.args.get('sortnum')
    keyword = str(request.args.get('keyword'))
    arr = request.json
    
      
    return jsonify(get_amazon_searched(keyword, arr, sort))
