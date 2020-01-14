# JackList Internship Web Development
### Build ALL-IN-ONE online shopping site by using API
  Overall Structure : check PDF

## python dependency

  * SQLAlchemy
  
  * marshmallow-sqlalchemy
  
  * Flask-SQLAlchemy
  
  * Flask
  
  * Flask-Cors
  
  * mysqlclient
  
  * pandas
  
  * python-mysql

 
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
    - amazon: TOO MANY EXCEPTION => need None exception when len = 0

  * Todo
    - ranking tracker (using rank table)
    - Threading
    - gunicorn, supervisor
    - renewal amazon method
    - DB structure repair
    -
    

  * Issue
    - amazon index error => pass
    
