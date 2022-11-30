import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


url = 'http://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0013&date=20221121'

driver = webdriver.Chrome('./Chromedriver')
driver.get(url)
driver.implicitly_wait(1)

driver.switch_to.frame('ifrm_movie_time_table')
r = driver.page_source

soup = BeautifulSoup(r, 'html.parser')
title_list =soup.select('div.info-movie')
for i in title_list:
  print(i.select_one('a > strong').text.strip())