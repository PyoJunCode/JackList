import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import xmltodict



def all():
    count = 0
    url = 'https://www.amazon.co.jp/gp/bestsellers'
    
    driver = webdriver.Chrome('/Users/seojunpyo/Downloads/chromedriver')
    driver.get(url)
    
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    menu = soup.select('#zg_browseRoot > ul > li > a')
    
    for item in menu:
        
        print(item.text)
        url2 = str(item['href'])
        driver.get(url2)
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        menu2 = soup2.select('#zg_browseRoot > ul > ul >li > a')
       
        if(len(soup2) > 70):
          count += 1
        for item2 in menu2:
            print("\t" + item2.text)
            
            url3 = str(item2['href'])
            driver.get(url3)
            soup3 = BeautifulSoup(driver.page_source, 'html.parser')
            menu3 = soup3.select('#zg_browseRoot > ul > ul > ul >li > a')
            
            for item3 in menu3:
                print("\t\t" + item3.text)
                print(' ')

    driver.quit()
    print(count)
    
    
def getlink():

    url = 'https://am-tb.tk/amaranrss/'
    
    driver = webdriver.Chrome('/Users/seojunpyo/Downloads/chromedriver')
    driver.get(url)
    driver.find_element_by_name('url').send_keys('https://www.amazon.co.jp/gp/bestsellers/mobile-apps/2386893051/ref=zg_bs_nav_mas_2_2386894051')
   
    driver.find_element_by_class_name('setbutton').click()
    
    link = driver.find_element_by_name('rss').get_attribute('value')
    
    


def getItem():

    url = 'https://am-tb.tk/amaranrss/get/?url=https%3A%2F%2Fwww.amazon.co.jp%2Fgp%2Fbestsellers%2Fmobile-apps%2F2386893051%2Fref%3Dzg_bs_nav_mas_2_2386894051'
    get = requests.get(url)
    
    dict = xmltodict.parse(get.text)
    
    for item in dict['rss']['channel']['item']:
        print(item['title'])
        print(' ')
    
getItem()
