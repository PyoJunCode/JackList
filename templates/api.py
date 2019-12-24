
from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

#@app.route('/')
#def homepage():
#
# search=requests.get('https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword=パソコン&applicationId=1036855640468891236').json()
#
#
# search=requests.get('https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&keyword=%E3%83%9D%E3%82%B1%E3%83%83%E3%83%88%E3%83%A2%E3%83%B3%E3%82%B9%E3%82%BF%E3%83%BC&applicationId=1036855640468891236').json()
#
# return render_template('list.html', Items=search['Items'])
#
#if __name__ == '__main__':
#  app.run(host='0.0.0.0', debug=False)








