from datetime import datetime

tracking_time = datetime.now()
tracking_time = tracking_time.strftime("%Y-%m-%d %H:%M:%S")
if datetime.now().hour in range(10, 22):
  print(datetime.now().hour)
  
else:print('aa')