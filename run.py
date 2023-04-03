from Message import MessageBot
from Imax_Scraping import Scrapper
from Data import DataBase
from datetime import datetime
import time
from selenium.common.exceptions import NoSuchElementException
import time

bot = MessageBot()
postgre = DataBase()
postgre.create_table()
print("최초 실행 시간 : ", str(datetime.now()))

scrapper = Scrapper('Yong-San')
scrapper.setting()

count = 0
div_number = 1
li_number = 1
while True:
  if li_number == 9:
    scrapper.click_next_btn()
    li_number = 1
    div_number += 1
  try:
    time.sleep(1)
    movie_info, cgv_title = scrapper.find_imax(div_number, li_number)
    #cgv_title을 못 받아왔단 의미는 IP차단 당했다는 의미
    if cgv_title == None:
      print("IP차단")
      print('count : ', count)
      break
    else:
      for data in movie_info:
        #이미 데이터가 존재하면 다음 데이터로 넘어감
        if postgre.check_data(data):
          continue
        else:
          send_text = f'{data[3]} 영화관에 {data[0]}, {data[1]} 영화가 오픈하였습니다.'
          #텔레그램 알림톡 전송
          bot.send_msg(send_text = send_text)
          #데이터 베이스 추가
          postgre.insert_data(data)
    time.sleep(1)
    count +=1
  #오픈되지 않은 날짜 확인시
  except NoSuchElementException as e:
    scrapper.click_next_btn()
    div_number = 1
    li_number = 0
  li_number += 1


