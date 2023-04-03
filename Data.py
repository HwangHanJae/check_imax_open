import psycopg2
import key
class DataBase:
  def __init__(self):
    self.__conn = psycopg2.connect(host = key.HOST,
                          dbname = key.DB,
                          user= key.USER,
                          password = key.PW)
    self.__cursor = self.__conn.cursor()
  @property
  def conn(self):
    return self.__conn
  @conn.getter
  def conn(self):
    return self.__conn
  @property
  def cursor(self):
    return self.__cursor
  @cursor.getter
  def cursor(self):
    return self.__cursor

  def create_table(self):
    """
    MOVIE_INFO 테이블 CREATE 함수
    """
    sql = """CREATE TABLE IF NOT EXISTS MOVIE_INFO (
      id serial PRIMARY KEY,
      movie_open_date text NOT NULL,
      title text NOT NULL,
      tracking_time text NOT NULL,
      theater text NOT NULL);"""
    self.__cursor.execute(sql)
    self.__conn.commit()
      
  def insert_data(self, data):
    insert_sql  = """INSERT INTO MOVIE_INFO (movie_open_date, title, tracking_time, theater) VALUES(%s, %s, %s, %s);"""
    # select_sql = """SELECT *
    #                 FROM MOVIE_INFO
    #                 WHERE movie_open_date = %s and title = %s;"""
    try:
      movie_open_date = data[0]
      title = data[1]
      tracking_time = data[2]
      theater = data[3]
      # self.__cursor.execute(select_sql, (str(movie_open_date), title))
      # rows = self.__cursor.fetchall()
      # if rows == []:
      self.__cursor.execute(insert_sql, (str(movie_open_date), title, tracking_time, theater))  
      self.__conn.commit()
    except Exception as error:
      print("Error in Insert Data Transaction", error)
      self.__conn.rollback()
  def clear_table(self):
    truncate_sql = """TRUNCATE TABLE MOVIE_INFO restart identity """
    check_sql = """SELECT * FROM MOVIE_INFO"""
    self.__cursor.execute(truncate_sql)
    self.__cursor.execute(check_sql)
    rows = self.__cursor.fetchall()
    if rows == []:
      print('clear 완료')
      self.__conn.commit()
    else:
      print('오류 발생')
      self.__conn.rollback()

  def check_data(self, data):
    """
    입력받은 데이터가 데이터베이스에 존재하는지 확인
    """
    movie_open_date = data[0]
    title = data[1]
    theater = data[3]
    select_sql = """SELECT movie_open_date, title FROM MOVIE_INFO
                    WHERE movie_open_date = %s and title = %s and theater = %s"""
    self.__cursor.execute(select_sql, (str(movie_open_date), title, theater))
    rows = self.__cursor.fetchall()
    for row in rows:
      if row:
        return True
    return False
  def drop_table(self):
    sql = """DROP TABLE IF EXISTS MOVIE_INFO"""
    self.__cursor.execute(sql)
    self.__conn.commit()
    print('DROP TABLE 완료')
  def delete_table(self):
    sql =  """DELETE FROM MOVIE_INFO"""
    self.__cursor.execute(sql)
    self.__conn.commit()
    print('DELETE TABLE 완료')

# def input_test(postgre, datas):
#   for data in datas:
#     flag = postgre.check_data(data)
#     if flag:
#       print(f'{data[0]}, {data[1]}, {data[3]} 데이터가 이미 존재하여 입력할 수 없습니다.')
#       continue
#     else:
#       postgre.insert_data(data)

