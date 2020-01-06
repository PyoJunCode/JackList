from flask import Flask

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
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



url ='mysql://root:fhrmdls123@localhost:3306/rakuten?charset=utf8'


app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    load_data()


app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)


engine = create_engine(url)
Base = declarative_base()

Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

rakuten_categories = None
yahoo_categories = None
rakuten_itemRanking = None
selected_date = None

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
        dump_only = ('id',)

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
        dump_only = ('id',)

class RankList(Base):

    __tablename__ = 'ranklist'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)


    def __init__(self, date):
    
        self.date = date
    
    
    
    def __repr__(self):
        return "<Product(date = '%s', ranking = '%s')>" % (self.date, self.ranking)
#==============================================================================


#===========================Load Data==========================================

def get_rakuten_cate():
    
    data = rakuten_Category.query.all()
    category_schema = rakuten_CateSchema(many=True)
    output = category_schema.dump(data)
    return output

def get_yahoo_cate():

    data = yahoo_Category.query.all()
    category_schema = yahoo_CateSchema(many=True)
    output = category_schema.dump(data)
    return output


#def get_latest_ranking():

    

def get_rakuten_Ranking():

    data =  encjson.read_sql_query('SELECT * FROM ranklist', engine)
    return json.loads(data.to_json(orient='records'))
    



    
def get_rakuten_selected_ranking(data):

    session.commit()
    print(str(session.query(RankList).order_by(desc('date')).first().date))
    selected_date = ' AND r.date = ' + str(session.query(RankList).order_by(desc('date')).first().date)
    
    
    selected_genre = data
    
    
    #print('select from ' + str(session.query(RankList).order_by(desc('date')).first().date) )
    
    query = 'SELECT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product, r.itemCode  FROM rakuten_product AS p LEFT JOIN rakuten_product_ranking AS r ON p.itemCode = r.itemCode WHERE r.genreId = '
    
    
    data = encjson.read_sql_query(query + selected_genre + selected_date, engine)
    return json.loads(data.to_json(orient='records'))
    

def get_yahoo_selected_ranking(data):

    session.commit()
    print(str(session.query(RankList).order_by(desc('date')).first().date))
    selected_date = ' AND r.date = ' + str(session.query(RankList).order_by(desc('date')).first().date)
    
    
    selected_genre = data
    
    
    #print('select from ' + str(session.query(RankList).order_by(desc('date')).first().date) )
    
    query = 'SELECT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product,     r.itemCode  FROM yahoo_product AS p LEFT JOIN yahoo_product_ranking AS r ON p.itemCode = r.itemCode WHERE r.genreId =     '
    
    
    data = encjson.read_sql_query(query + selected_genre + selected_date, engine)
    return json.loads(data.to_json(orient='records'))


def test():
    arr = (1,2,3)
    query = 'SELECT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product, r.itemCode  FROM rakuten_product AS p LEFT JOIN rakuten_product_ranking AS r ON p.itemCode = r.itemCode WHERE r.genreId IN '
    
    print(query + str(arr))
    data = encjson.read_sql_query(query + str(arr), engine)
    

def load_data():

    global rakuten_categories
    global yahoo_categories
    global rakuten_itemRanking
    yahoo_categories = get_yahoo_cate()
    rakuten_categories = get_rakuten_cate()
    #yahoo_itemRanking = get_yahoo_Ranking()
    rakuten_itemRanking = get_rakuten_Ranking()



#==============================================================================

#=================================Routing======================================
load_data()
 
@app.route('/', methods=['GET',])
def index():
    return "<html><body><h1>working!</h1></body></html>"

@app.route('/ranking', methods=['GET',])
def ranking():
    
    return jsonify(get_rakuten_Ranking())
    
    
@app.route('/rakuten_cate', methods=['GET',])
def rakuten_cate():
    
    print(jsonify(rakuten_categories))
    return jsonify(rakuten_categories)
    

@app.route('/yahoo_cate', methods=['GET',])
def yahoo_cate():
    
    print(jsonify(yahoo_categories))
    return jsonify(yahoo_categories)
    

@app.route('/rakuten_selected_ranking', methods=['GET',])
def rakuten_selected_ranking():
    data = request.args.get('genreId')
    return jsonify(get_rakuten_selected_ranking(data))

@app.route('/yahoo_selected_ranking', methods=['GET',])
def yahoo_selected_ranking():
    data = request.args.get('genreId')
    return jsonify(get_yahoo_selected_ranking(data))
    
    
@app.route('/yahoo_searched', methods=['GET','POST']) # url, post both
def yahoo_searched():
    data = request.args.get('genreId')
    return jsonify(get_yahoo_selected_ranking(data))
