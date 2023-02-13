from Message import MessageBot
from Imax_Crawler import Crawler
from Data import DataBase
#추적해야하는 날짜 설정
check_days = [8,9,10,11,12,13,14]

#crawler객체, bot객체, postgre객체 생성
crawler = Crawler(check_days=check_days)
bot = MessageBot()
postgre = DataBase()
postgre.create_table()
#imax 영화 정보 받아오기
imax_data = crawler.find_imax()

#알림톡 보내기 및 데이터베이스 입력
for data in imax_data:
    flag = postgre.check_data(data)
    if flag:
      print(f'{data[0]}, {data[1]} 데이터가 이미 존재하여 입력할 수 없습니다.')
      continue
    else:
      send_text = f'{data[0]}, {data[1]} 영화가 오픈하였습니다.'
      bot.send_msg(send_text = send_text)
      postgre.insert_data(data)
