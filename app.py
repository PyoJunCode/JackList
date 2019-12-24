from flask import Flask

from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column
from flask_cors import CORS
from flask import jsonify

import pandas as encjson
import requests
import json



app = Flask(__name__)
CORS(app)

url ='mysql://root:fhrmdls123@localhost:3306/rakuten?charset=utf8'
#app.config['SQLALCHEMY_DATABASE_URI'] = url

engine = create_engine(url)

def get_ranking():

    data =  encjson.read_sql_query("SELECT * FROM product", engine)
    
    #print(json.loads(data.to_json(orient='records')))
 
    return json.loads(data.to_json(orient='records'))
    
#print(get_ranking())

#db = SQLAlchemy(app)
 
search=requests.get('https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&keyword=%E3%83%9D%E3%82%B1%E3%83%83%E3%83%88%E3%83%A2%E3%83%B3%E3%82%B9%E3%82%BF%E3%83%BC&applicationId=1036855640468891236').json()

@app.route('/', methods=['GET',])
def index():
    
    return "<html><body><h1>working!</h1></body></html>"

@app.route('/test', methods=['GET',])
def test():
    return jsonify(get_ranking())
