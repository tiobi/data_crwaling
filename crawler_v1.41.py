'''
v1.2 divided chrome browser and downloader
v1.3: added retry, optionss
v1.4 added random time delay
v2.0 more usable in linux/terminal
v2.1 colored error messages


to do:
    카테고리 재 다운로드
'''



from selenium import webdriver
from datetime import date,timedelta
from urllib.request import urlretrieve
import time
import os
from tqdm import tqdm
from random import uniform as delay
from termcolor import colored

sy = int(input("Starting Year  : "))
sm = int(input("Starting Month : "))
sd = int(input("Starting Day   : "))
ey = int(input("Ending Year    : "))
em = int(input("Ending Month   : "))
ed = int(input("Ending Day     : "))
sdate = date(sy, sm, sd)
edate = date(sy, sm, ed)
delta = edate - sdate
print("\n\n")

SEARCH_LIST = ["스타벅스", "앤젤리너스", "탐앤탐스", 
               "투썸플레이스", "이디야", "공차", 
               "빽다방", "블루보틀", "폴바셋", 
               "할리스", "커피빈", "매머드커피"] #12개


options = webdriver.ChromeOptions() 
options.add_argument('headless') 
options.add_argument('window-size=1920x1080') 
options.add_argument("disable-gpu")


tolerance = 0
for i in range(delta.days + 1):
    print("crawling " + str(sdate + timedelta(days = i)))
    time.sleep(2)
    
    for SEARCH_TERM in tqdm(SEARCH_LIST):
        try:
            time.sleep(2)
            print("\n")
            print("Searching \t" + SEARCH_TERM)
            day = str(sdate + timedelta(days = i)).replace("-", "")
            browser = webdriver.Chrome('C:\chromedriver\chromedriver_win32\chromedriver.exe', options = options) 
            BASEURL = "https://search.daum.net/search?w=img&nil_search=btn&DA=NTB&enc=utf8&q=" + SEARCH_TERM
            URL = BASEURL + "&sd=" + day + "000000&ed=" + day + "235959&period=u"
            browser.get(URL)
            time.sleep(delay(1.5, 3))
            browser.implicitly_wait(delay(1, 2))
            
            while 1:
                try:
                    for _ in range(2000):
                        browser.execute_script("window.scrollBy(0,30000)")
                    browser.find_element_by_css_selector("a.expender.open").click()
                    continue
    
                except:
                    break
    
            
            count = 0
            photo_list = []
            photo_list = browser.find_elements_by_css_selector("img.thumb_img")
     
            
            links = []
            for photo in photo_list:
                link = photo.get_attribute("src")
                if "https" in link:
                    links.append(link)
                    
            if not os.path.exists(SEARCH_TERM):
                os.mkdir(SEARCH_TERM)
                
            
            print("Downloading \t" + SEARCH_TERM)
            time.sleep(2)
            for index, link in enumerate(links):
                time.sleep(delay(1.5, 3))
                file_name = "{0}_{1}_{2:03d}.jpg".format(SEARCH_TERM, day, index)
                urlretrieve(link, os.path.join(r".\\", SEARCH_TERM, file_name))
                
            time.sleep(delay(1, 5))
            tolerance = 0
            browser.quit()
            print("Downloading " + SEARCH_TERM + "Completed")

                
            
        except:
            tolerance = tolerance + 1
            if tolerance > 3:
                print(colored("\n\n time out. try again later\n\n", "red"))
                break
        
            print("\n")
            print(colored("*Downloading " + str(sdate + timedelta(days = i)) + " for [" + SEARCH_TERM + "] failed. Restarting in 10 mins.*", "yellow"))

            time.sleep(600)
            continue
