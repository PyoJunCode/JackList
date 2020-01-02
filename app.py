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

categories = None
itemRanking = None
selected_date = None

#===========================Database Model===================================
class Category(db.Model):

    __tablename__ = 'rakuten_category'
    id = db.Column(db.Integer, primary_key=True)
    genreId = db.Column(db.Integer)
    cateName = db.Column(db.String(50))
    parentId = db.Column(db.Integer, db.ForeignKey('rakuten_category.id'))
    depth = db.Column(db.Integer)
    children = db.relationship('Category', remote_side=[parentId])
   
class CateSchema(ModelSchema):
   
    class Meta(ModelSchema.Meta):
        model = Category
        dump_only = ('id',)


class RankList(Base):

    __tablename__ = 'rakuten_ranklist'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)


    def __init__(self, date):
    
        self.date = date
    
    
    
    def __repr__(self):
        return "<Product(date = '%s', ranking = '%s')>" % (self.date, self.ranking)
#==============================================================================


#===========================Load Data==========================================

def get_cate():
    
    data = Category.query.all()
    category_schema = CateSchema(many=True)
    output = category_schema.dump(data)
    return output

#def get_latest_ranking():

    

def get_ranking():

    
    data =  encjson.read_sql_query('SELECT * FROM rakuten_ranklist', engine)
    return json.loads(data.to_json(orient='records'))
    
def get_selected_ranking(data):

    session.commit()
    print(str(session.query(RankList).order_by(desc('date')).first().date))
    selected_date = ' AND r.date = ' + str(session.query(RankList).order_by(desc('date')).first().date)
    
    
    selected_genre = data
    
    
    print('select from ' + str(session.query(RankList).order_by(desc('date')).first().date) )
    
    query = 'SELECT p.mediumImageUrls, p.itemPrice, p.reviewCount, p.itemUrl, p.itemName, p.reviewAverage, r.ranking AS product, r.itemCode  FROM rakuten_product AS p LEFT JOIN rakuten_product_ranking AS r ON p.itemCode = r.itemCode WHERE r.genreId = '
    
    
    data = encjson.read_sql_query(query + selected_genre + selected_date, engine)
    return json.loads(data.to_json(orient='records'))
    
    

def load_data():

    global categories
    global itemRanking
    categories = get_cate()
    itemRanking = get_ranking()



#==============================================================================

#=================================Routing======================================
load_data()

 
@app.route('/', methods=['GET',])
def index():
    return "<html><body><h1>working!</h1></body></html>"

@app.route('/ranking', methods=['GET',])
def ranking():
    
    return jsonify(get_ranking())
    
    
@app.route('/cate', methods=['GET',])
def cate():
    
    print(jsonify(categories))
    return jsonify(categories)
    

@app.route('/selected_ranking', methods=['GET',])
def selected_ranking():
    data = request.args.get('genreId')
    return jsonify(get_selected_ranking(data))


