from Message import MessageBot
from Imax_Crawler import Crawler

check_days = [1,7,8,9,10,14,15,16,17,18,30]
crawler = Crawler(check_days=check_days)
imax_data = crawler.find_imax()
print(imax_data)