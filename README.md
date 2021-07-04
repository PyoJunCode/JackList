# JackList Internship 
### Build ALL-IN-ONE online shopping site by using API

**E-commerce 통합 비교 플랫폼**



<img src="https://user-images.githubusercontent.com/47979730/124391004-4c64bc80-dd29-11eb-86d9-dd36947e0876.PNG" alt="cover" style="zoom: 80%;" />

### Problem Definition

일본의 E-commerce 시장에는 한국의 다나와, 네이버 쇼핑처럼 여러 쇼핑몰간의 가격 비교 플랫폼이 정착하지 않았습니다.

<br>

따라서 통합적인 상품 정보 비교 플랫폼을 구축하기 위해 현재 일본에서 가장 규모가 큰 온라인 쇼핑몰인 **Rakuten, Amazon, Yahoo** 쇼핑의 데이터를 수집하였습니다.

<br>

통합된 Database를 **RESTful API**와 **website**를 통해 제공하여 사용자가 상품 정보를 손쉽게 검색하고 비교할 수 있게 해줍니다.

<br>

기존의 각각 쇼핑몰의 다른 상품 Data 구조 정보와, 그것들을 통합시킬 수 있는 새로운 Data 구조를 보유한 점을 이용해 부수적인 기능을 창출할 수 있습니다. (Outcome 참고)

<br>

  **더 자세한 Overall Structure : check [this PDF](https://github.com/PyoJunCode/JackList/blob/master/jacklist_backend.pdf)** <br>

  Rakuten, Yahoo shopping, Amazon 에서 상품 정보를 수집하여 전처리 과정을 거쳐 통일된 Database 생성 (MySQL) <br>
  FLASK 를 사용해 Restful API 서버 구축하여 사용자의 요청에 대한 Data를 얻기 위한 Query 생성/ Data 반환 <br>
  해당 Data를 node.js를 사용해 Parsing 후 Front-end로 전달 <br>



due : *2019/12 - 2020/03*

---

## Index

->[Crawling](https://github.com/PyoJunCode/JackList#Crawling)

->[Database](https://github.com/PyoJunCode/JackList#Database)

->[Flask API](https://github.com/PyoJunCode/JackList#Flask-RESTful-API)

->[Outcome](https://github.com/PyoJunCode/JackList#Outcome)

->[Info,Logs](https://github.com/PyoJunCode/JackList#python-dependency)

<br>

## Stacks

- **Data Crawling** : BeautifulSoup4, Selenium

- **Database** : MySQL

- **Back-end** : Flask, Node.js

- **Infra** : AWS EC2

<br>

## Files

DB.py

* 카테고리, 상품 랭킹과 각 상품의 정보를 크롤링하여 MySQL server에 저장합니다. <br>

app.py

* 사용자의 요청에 따라 그에 맞는 SQL문을 작성해 Data를 return해주는 Flask RESTful API Server입니다.

logging.conf

* Data를 Crawling할 때 남기는 log에대한 설정 파일

product_update.log

* error log

<br>

## Crawling

<img src="https://user-images.githubusercontent.com/47979730/124392948-10365980-dd33-11eb-9b9e-d91c8096dab8.PNG" alt="cate" style="zoom:50%;" />

**카테고리**

- 상위 카테고리부터 DFS 방식으로 탐색하며 하위 카테고리와의 Relation을 정의하였습니다.

- Rakuten, Yahoo의 경우에는 API에서 제공해주는 JSON내의 genre ID, parent ID, depth 정보를 이용하였습니다.

- Amazon의 경우에는 python 라이브러리 BeautifulSoup4를 이용하여 하위 3개 카테고리까지 Crawling하였습니다.<br>

<br>

![concat](https://user-images.githubusercontent.com/47979730/124392952-188e9480-dd33-11eb-83cb-992d0db922a4.png)

**상품**

- Rakuten, Yahoo의 경우 자체지원 API를 통해 적절한 파라미터와 함께 호출 후 Parsing을 하였습니다.
- Amazon의 경우 API를 지원하지 않고 상품 정보는 Javascript로 불러오기 때문에 Selenium으로 각 페이지를 탐색하며 Crawling 하였습니다.

<br>


## Database

1. categories

   3사 쇼핑몰의 통합된 카테고리 Table입니다.

2. product_ranking

   특정 시간의 상품 랭킹 정보를 가지고있습니다. date, itemCode, genreID의 Foreign key를 갖습니다.

3. 각 플랫폼의 product

   상품의 상세 정보를 가지고 잇습니다.



Category - Product 간의 직접적인 연관 관계는 없습니다.

하지만 Category table 의 genreID를 Foreign Key로 갖고, 각 플랫폼 product table의 item code를 Foreign key로 가져

둘 사이의 간접적인 연관 관계를 성립시킵니다.

 * https://www.erdcloud.com/d/aBCvizucRmM7xC7cw\

<br>

## Flask-RESTful-API

- 사용자의 요청에 따라 Flask API server(app.py)가 파라미터들을 parsing 한 뒤 그 에 맞는 Query문을 작성합니다.

- DB Server에 해당 쿼리문을 보내고 return 받은 정보를 JSON 형식으로 Dump 한 뒤 사용자에게 돌려줍니다.



API Call example

*패션 카테고리에 대해 3사의 랭킹 정보 동시에 호출*

1. RESTful API의 파라미터 분석
2. 랭킹 정보 함수 호출
3. 전달받은 genreid 쿼리문에 조합
4. RankList table의 제일 최근 date를 추출하여 쿼리문에 조합
5. 생성된 쿼리문을 Rakuten, Yahoo, Amazon 에 대해 모두 호출
6. return 받은 Data들을 모아 하나의 JSON으로 Dump 후 return 

![api](https://user-images.githubusercontent.com/47979730/124391990-41f8f180-dd2e-11eb-9e36-760dbb2975ce.PNG)

<br>

## Outcome

1. **통합 상품 비교 플랫폼**

   - 소비자들이 같은 상품에 대해서 **여러 쇼핑몰**의 가격을 한눈에 비교할 수 있습니다.
   - 각 쇼핑몰 별로 선택한 카테고리의 실시간 상품 랭킹을 한눈에 확인할 수 있습니다.

2. **RESTful API**

   - API를 통해 Database에서 원하는 정보를 가져올 수 있기 때문에 현재의 웹사이트뿐 만 아니라, 모바일 앱, 봇 등으로의 **높은 이식성**을 가지고 있습니다.

3. **Cross-platform 자동 판매 상품 등록 서비스**

   - **각 쇼핑몰**의 상품 데이터 형식과 그것들을 **통합할 수 있는** 데이터 형식을 가지고 있는점을 활용하여
     별도의 사이트에서 하나의 상품을 판매등록하면 **여러개의 사이트에 자동 등록**하는 기능 등의 확장성을 가지고 있습니다.

   

<br>

---



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

    - sudo pkill gunicorn

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
