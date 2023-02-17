from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import sys
from datetime import datetime

urls = []
dates = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]

for date in dates:
  #왕십리 cgv url
  url = f'http://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0074&date=202302{str(date)}'
  #url = f'https://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0013&date=202302{str(date)}'
  urls.append(url)

def find(urls):

  options = Options()
  options.headless = True
  driver = webdriver.Firefox(executable_path='driver/geckodriver.exe',options=options)
  data = []
  for url in urls:
    driver.get(url)
    driver.implicitly_wait(1)
    #time.sleep(3)
    driver.switch_to.frame('ifrm_movie_time_table')
    iframe = driver.page_source

    soup = BeautifulSoup(iframe, 'html.parser')
    data.append(soup.title)
  driver.close()
  driver.quit()

  return data

#soup.title이 None이라면 ifrm_movie_time_table이 등장하지 않은것
#IP가 차단당했다고 봐도 괜찮음
print("최초 실행 시간 : ", datetime.now())
sleep_time = 60
while True:
  start = datetime.now()
  data = find(urls)
  if None in data:
    print('date의 크기 : ', len(dates))
    print('sleep time : ', sleep_time)
    print("IP 차단 당함")
    sys.exit()

  print('date의 크기 : ', len(dates))
  print('sleep time : ', sleep_time)
  print("OK")
  end = datetime.now()
  print("시간 : ", end-start)
  time.sleep(sleep_time)
  
  