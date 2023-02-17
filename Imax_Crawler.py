from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timedelta
import time
class Crawler:
  def __init__(self, check_days):
    self.check_days = check_days
    options = Options()
    options.headless = True
    self.driver = webdriver.Firefox(executable_path='driver/geckodriver.exe',options=options)
    #self.driver = self._proxy('127.0.0.1', 9150)
    self.dates = self._get_dates()
    self.urls = self._get_urls()
  def _proxy(self, HOST, PORT):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', HOST)
    profile.set_preference('network.proxy.socks_port', PORT)
    profile.update_preferences()
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path='driver/geckodriver.exe', options=options, firefox_profile=profile)
    return driver
  def _get_dates(self):
    """
    추적해야할 날짜 정보를 받아오는 함수
    오늘이 2022년 11월 30일이라면 추적해야하는 날은
    2022년 12월 10일, 11일, 12일, 13일 등등

    """
    #추적해야할 날짜를 저장할 리스트
    dates = []
    #오늘날짜 받아오기
    now = datetime.now()
    #현재 날짜 기준으로 며칠뒤에 추적해야할지 저장한 리스트
    #self.check_days = [1,7,8,9,10,14,15,16,17,18,30]
    
    for days in self.check_days:
      #현재 날짜에서 추적해야할 날짜를 더하여 새로운 날짜를 생성
      after_date = now + timedelta(days=days)
      year = str(after_date.year)
      month = str(after_date.month)
      day = str(after_date.day)
      #날짜형태를 맞추어 주기 위하여
      #1~9일경우에 앞에 0을 더해줌
      if int(month) < 10:
        month = '0' + month
      if int(day) < 10:
        day = '0'+day
      date = year+month+day
      dates.append(date)
    return dates
  def _url(self, date):
    return f'https://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0013&date={date}'

  def _get_urls(self):
    urls = []
    for date in self.dates:
      url = self._url(date)
      urls.append(url)
    return urls
  
  def _get_tracking_time(self):
    tracking_time = datetime.now()
    tracking_time = tracking_time.strftime("%Y-%m-%d %H:%M:%S")
    return tracking_time

  def find_imax(self):
    data = set()
    imaxs_info = []
    titles = []
    for url, date in zip(self.urls, self.dates):
      self.driver.get(url)
      self.driver.implicitly_wait(1)
      time.sleep(3)
      self.driver.switch_to.frame('ifrm_movie_time_table')
      iframe = self.driver.page_source

      soup = BeautifulSoup(iframe, 'html.parser')
      imaxs = soup.select('span.imax')
      titles.append(soup.title)
      imaxs_info.append((imaxs, date))
    self.driver.close()
    self.driver.quit()

    #추적 날짜에 아이맥스 영화의 정보가 존재한다면
    ###추적 날짜 모두 아이맥스 영화가 존재하지 않을 수 있음
    if imaxs_info != []:
      for imaxs, date in imaxs_info:
        #아이맥스의 정보가 존재한다면
        if len(imaxs)> 0:
          for imax in imaxs:
            col_times = imax.find_parent('div', class_ = 'col-times')
            showtimes_wrap = imax.find_parent('div', class_='showtimes-wrap')
            for i in range(1,4):
              year = showtimes_wrap.select_one(f'#slider > div:nth-child({i}) > ul > li.on > div > a > span')
              month = showtimes_wrap.select_one(f'#slider > div:nth-child({i}) > ul > li.on > div > a > strong')
              if year != None and month != None:
                year = year.text.strip()[:-1]
                month = month.text.strip()
                break
              else:
                continue
            
          #imax 영화 날짜와 추적 날짜가 동일하다면
          #정보를 확인
            if year+month == date[4:]:
              title = col_times.select_one('div.info-movie > a > strong').text.strip() 
              tracking_date = self._get_tracking_time()
              data.add((int(date), title, tracking_date))
    data = sorted(list(data),key=lambda x : x[0])
    return data, titles
  # def printtt(self):
  #   imaxs = self._find_imax()
  #   return imaxs








