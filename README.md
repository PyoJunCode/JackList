# JackList Internship Web Development
### Build ALL-IN-ONE online shopping site by using API
   

## python dependency

  * SQLAlchemy
  
  * marshmallow-sqlalchemy
  
  * Flask-SQLAlchemy
  
  * Flask
  
  * Flask-Cors
  
  * mysqlclient
  
  * pandas
  
  * wsgi (not sure)

 
## ENV

* macOS Catalina 10.15.x
 
 * python 3.7.4
 
 * MySQL 5.7.28
 
 * apache 2.4.41
 
 * javascript


## Database

 * https://www.erdcloud.com/d/aBCvizucRmM7xC7cw
 
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
   -  get items info from latest date of rankling list 
