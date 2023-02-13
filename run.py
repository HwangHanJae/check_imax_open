from Message import MessageBot
from Imax_Crawler import Crawler
from Data import DataBase
from datetime import datetime
#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
#추적 날짜 설정
check_days = [8,9,10,11,12,13,14]

#crawler객체, bot객체, postgre객체 생성

bot = MessageBot()
postgre = DataBase()
postgre.create_table()

#알림톡 보내기 및 데이터베이스 입력
def daily_job(postgre, bot,check_days):
  #10시부터 22시까지만 추적하도록 설정
  crawler = Crawler(check_days=check_days)
  now_hour = datetime.now().hour
  if now_hour in range(10, 22):
    print(str(datetime.now()) + "추적 시작")
    #imax 영화 정보 받아오기
    imax_data = crawler.find_imax()
    for data in imax_data:
        flag = postgre.check_data(data)
        if flag:
          #print(f'{data[0]}, {data[1]} 데이터가 이미 존재하여 입력할 수 없습니다.')
          continue
        else:
          send_text = f'{data[0]}, {data[1]} 영화가 오픈하였습니다.'
          bot.send_msg(send_text = send_text)
          postgre.insert_data(data)
  else:
    print('스케쥴러 종료')
    scheduler.remove_job('my_job_id')
    return
scheduler = BlockingScheduler(timezone='Asia/Seoul')
scheduler.add_job(func=daily_job, trigger='interval', args=[postgre, bot,check_days],seconds=60, id='my_job_id')
scheduler.start()