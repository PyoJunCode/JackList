# JackList Internship Web Development
### Build ALL-IN-ONE online shopping site by using API
  Overall Structure : check [PDF](https://github.com/PyoJunCode/JackList/blob/master/jacklist_backend.pdf) <br>
  
  Rakuten, Yahoo shopping, Amazon 에서 상품 정보를 수집하여 전처리 과정을 거쳐 통일된 Database 생성 (MySQL) <br>
  FLASK 를 사용해 Restful API 서버 구축하여 사용자의 요청에 대한 Data를 얻기 위한 Query 생성/ Data 반환 <br>
  해당 Data를 node.js를 사용해 Parsing 후 Front-end로 전달 <br>
  
---

## Files

DB.py
* 카테고리, 상품 랭킹과 각 상품의 정보를 크롤링하여 MySQL server에 저장합니다. <br>

app.py
* 사용자의 요청에 따라 그에 맞는 SQL문을 작성해 Data를 return해주는 Flask RESTful API Server입니다.

logging.conf
* Data를 Crawling할 때 남기는 log에대한 설정 파일

product_update.log
* error log


## python dependency

  * SQLAlchemy
  
  * marshmallow-sqlalchemy
  
  * Flask-SQLAlchemy
  
  * Flask
  
  * Flask-Cors
  
  * mysqlclient
  
  * pandas
  
  * python-mysql
  
  * gunicorn3
    - gunicorn3 --bind 0.0.0.0:5000 app:app >> execute gunicorn
  
    - sudo supervisorctl restart flask_settings >> reload code
  
    - =supervisor load=
  
    -  sudo pkill gunicorn
  
    - sudo supervisorctl reread
  
    - sudo supervisorctl update
  
    - sudo supervisorctl start flask_settings
    
    - sudo supervisorctl stop

 
## ENV

* macOS Catalina 10.15.x
 
 * python 3.7.4
 
 * MySQL 5.7.28 *(utf8mb4 setting)*
 
 * apache 2.4.41
 
 * javascript




## Database

 * https://www.erdcloud.com/d/aBCvizucRmM7xC7cw
 
---
## Log

 * ~12/24
   - Fundamental Step:
     - environment settings, 
     - analyze API, 
     - make overall DB and Web Structures
 * 12/25 
   - Category get and push to MySQL DB
   - Category jasonify and return complete (apache <=> flask)
 * 12/26
   - modified Product, Ranking Table DB  structure
   - crawl products information for every category and push to DB
 * 12/27
   - DB : ranking <=> rankList <=> products relationship setting complete
   - update products info when already exists
   - changed overall DB structures
   - Flask : return selected_category's item ranking in JSON
   
 * 12/30
   - product table 'reviewAverage' added
   - rakuten products list per category:  30 -> 120 changed
   - rakuten API delay issue: interval 2 sec when JSON have 'error'
     - working well, but frequent sleep when process almost done(sleep per API)
     - take about 20 min (518cate * 4page API requests)  : need routing or threading?
   - get items info from latest date of rankling list 
   - root category added 
   
 * 1/2
   - Yahoo Api started
   - Yahoo! : *API returns JSONP type.* (JSON type : 2020 / 2 release and will be parameter change )
   - rename MySQL tables 
   
 * 1/3
   - Yahoo Category DB complete
   - rename ORM classes and variables for multi sites
   
 * 1/6
   - Yahoo complete:
     - API not contains product's price => need one more API step 
     - exist such differences with rakuten => equalization
     - product don't need genreId ? testing item info API size (small, large)
     - take too long time to update frequently
     - exception 
   - Flask modification for yahoo - complete

  * 1/7
    - keyword search complete
    - combine date & time format for select latest data ->  desc ordering and select
    - Threading issue
    - Amazon RSS (HARD)
      - No genreId, Img, price and cateogories API = > use selenium
      - Categories -> traverse by bs4 crawler : fail -> use selenium
      - different DB structure (NO genreId using id instead)
      - selenium: category URL -> rss input -> rss output -> parsing XML -> DB
      - Problem : rss not allow new request per 1 hour => only Big categories
        - partition original url with '/' -> working
      - products maybe not sorted by ranking?
      
  * 1/8
    - Drop category table if already exists when update
    - amazon update_products issue 
      - digital music category API not working
      - food category not working (can't read in For loop  WHY????????)
    -  flask server issue fixed (Base => db.Model)
    - key word search complete
    
  * 1/9
    - **Server migration setting complete**
    - duplicate product result when searching fixed
    - product sorted by ranking surely
    - *prototype complete*
    - update logger added
    
  * 1/14 
    - get amazon product : RSS => Crawling
    - amazon: TOO MANY EXCEPTION => pass product when exception occured
    
  * 1/15
    - DB overall structure: complement relationship ( compare column => ref by id (primary_key) )
    - overall category added lastly now : to get id = len( ) ==>> not efficient
    - amazon product structure updated (same as others)
    - table encoding type changed for emoticon in product title
    
  * 1/16
    - can update DB while running flask server
    - server DB recollected
    
    
  * 1/17
    - Yahoo page5 -> 0 changed (don't need 5 page)
    - Amazon product crawling :  Selenium => requests
    - sorting support
    - gunicorn, supervisor setting completed
    - DB fix => string to int (review count, price etc...)
    
  * 1/20
    - 'lock' column added for get valid DB during update
    - flask code beautify 
    - amazon DB fixed
    
  * 1/21
    - amazon logic modified => reduce lag, exception => '0'
    - DB semi final version
    
    
  * Todo
    - ranking tracker (using rank table)
    - Threading (server performance issue)
    - exception logic, update speed increase
    
---    

  * Issue
    - merge product and ranking table
    - can't merge tables because amazon's itemUrl too long 
    - amazon exception (no price, avg etc... => just pass now)
    - **crawling getting slower => server die**
    - amazon exception issue
