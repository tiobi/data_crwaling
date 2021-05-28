#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import shutil

baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome(executable_path = "C:\chromedriver\chromedriver_win32\chromedriver.exe")
driver.get(url)

time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html)

imgList = []
urlList = []

for i in range(0, 200):
    image = soup.select('.v1Nh3.kIKUG._bz0w')
    for i in image:
        urlList.append('https://www.instagram.com'+ i.a['href'])
        imgUrl = i.select_one('.KL4Bh').img['src']
        imgList.append(imgUrl)
        imgList = list(set(imgList))
        html = driver.page_source
        soup = BeautifulSoup(html)
        image = soup.select('.v1Nh3.kIKUG._bz0w')
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

n = 1
for image_url in imgList:
    resp = requests.get(image_url, stream = True)
    local_file = open('./img/' + plusUrl + str(n) + '.jpg', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    n += 1
    del resp
    
driver.close()