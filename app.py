from flask import Flask

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from flask_cors import CORS
from flask import jsonify
from marshmallow_sqlalchemy import ModelSchema
import marshmallow as ma


import pandas as encjson
import requests
import json

url ='mysql://root:fhrmdls123@localhost:3306/rakuten?charset=utf8'


app = Flask(__name__)
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

#===========================Database Model===================================
class Category(db.Model):

    __tablename__ = 'categoryTest'
    id = db.Column(db.Integer, primary_key=True)
    genreId = db.Column(db.Integer)
    cateName = db.Column(db.String(50))
    parentId = db.Column(db.Integer, db.ForeignKey('categoryTest.id'))
    depth = db.Column(db.Integer)
    children = db.relationship('Category', remote_side=[parentId])
   
class CateSchema(ModelSchema):
   
    class Meta(ModelSchema.Meta):
        model = Category
        dump_only = ('id',)

#==============================================================================


#===========================Load Data==========================================

def get_cate():
    
    data = Category.query.all()
    category_schema = CateSchema(many=True)
    output = category_schema.dump(data)
    return output
    

def get_ranking():


    data =  encjson.read_sql_query("SELECT * FROM product", engine)
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
    return jsonify(itemRanking)
    
    
@app.route('/cate', methods=['GET',])
def cate():
    print(jsonify(categories))
    return jsonify(categories)
