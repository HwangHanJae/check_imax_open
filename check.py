from bs4 import BeautifulSoup
from selenium import webdriver

date = '20221210'
url = f'http://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0013&date={date}'
driver = webdriver.Chrome('./Chromedriver')
driver.get(url)
driver.implicitly_wait(1)

driver.switch_to.frame('ifrm_movie_time_table')
iframe = driver.page_source

soup = BeautifulSoup(iframe, 'html.parser')
imaxs = soup.select('span.imax')

if len(imaxs) > 0:
  for imax in imaxs:
    col_times = imax.find_parent('div', class_ = 'col-times')
    showtimes_wrap = imax.find_parent('div', class_='showtimes-wrap')
    year = showtimes_wrap.select_one('#slider > div:nth-child(1) > ul > li.on > div > a > span').text.strip()[:-1]
    month = showtimes_wrap.select_one('#slider > div:nth-child(1) > ul > li.on > div > a > strong').text.strip()
    title = col_times.select_one('div.info-movie > a > strong').text.strip()
    if year+month == date[4:]:
      send_text = f"{date}\n" + title + " IMAX 예매가 열렸습니다."
      print(send_text)