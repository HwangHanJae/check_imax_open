from Message import MessageBot
from Imax_Scraping import Scrapper
from Data import DataBase
from datetime import datetime
import sys
import time
from pprint import pprint
#추적 날짜 설정
check_days = [6,7,8,9,10,11,12,13,14]
#check_days = [0,1,2,3,4,5,6,7]

bot = MessageBot()
postgre = DataBase()
postgre.create_table()

#알림톡 보내기 및 데이터베이스 입력
def daily_job(postgre, bot,check_days, debug):
  start = datetime.now()
  scrapper = Scrapper(check_days=check_days)
  print("추적 시작 : ", str(datetime.now()))
  #imax 영화 정보 받아오기
  imax_data, titles = scrapper.find_imax()
  for data, title in zip(imax_data, titles):
      #title이 None이라면 IP가 차단당함
      if title == None:
        return False
      flag = postgre.check_data(data)
      if flag:
        #print(f'{data[0]}, {data[1]} 데이터가 이미 존재하여 입력할 수 없습니다.')
        continue
      else:
        if debug:
          #bot.test_send_msg()
          print('메시지전송')
          end = datetime.now()
          print('시간 : ', end-start)
        else:
          send_text = f'{data[0]}, {data[1]} 영화가 오픈하였습니다.'
          bot.send_msg(send_text = send_text)
          postgre.insert_data(data)
          end = datetime.now()
          print('시간 : ', end-start)
  return True, imax_data
  

sleep_time = 90
print("최초 실행 시간 : ", str(datetime.now()))
#torexe = os.popen('C:/Users/User/Desktop/Tor Browser/Browser/firefox.exe')
count = 0
while True:
  now_hour = datetime.now().hour
  #10시부터 22시까지만 추적하도록 설정
  if now_hour in range(10, 22):
    flag, imax_data = daily_job(postgre, bot,check_days, False)
    pprint(imax_data)
    count += len(imax_data)
    if flag== False:
      print(f"check_days의 크기 : {len(check_days)}")
      print(f'sleep time : {sleep_time}')
      print(f'total browser count : {count}')
      print("IP 차단")
  else:
    sys.exit()
  time.sleep(sleep_time)
