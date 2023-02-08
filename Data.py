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
  def _table_exist(self):
    flag = False
    try:
      self.__cursor.execute("""SELECT * FROM MOVIE_INFO
      """)
      flag =True
      return flag
    except:
      flag = False
      return flag

  def create_table(self):
    sql = """CREATE TABLE MOVIE_INFO (
      id serial PRIMARY KEY,
      movie_date VARCHAR(8) NOT NULL,
      title text NOT NULL,
      flag boolean NOT NULL);"""
    if self._table_exist():
      pass
    else:
      self.__cursor.execute(sql)
      #self.__cursor.close()
      self.__conn.commit()
      
  def insert_data(self, data):
    insert_sql  = """INSERT INTO MOVIE_INFO (movie_date, title, flag) VALUES(%s, %s, %s);"""
    select_sql = """SELECT movie_date, title, flag
                    FROM MOVIE_INFO
                    WHERE movie_date = %s and title = %s;"""
    try:
      for i in range(len(data)):
        date = data[i][0]
        title = data[i][1]
        flag = data[i][2]
        self.__cursor.execute(select_sql, (str(date), title))
        rows = self.__cursor.fetchall()
        if rows == []:
          self.__cursor.execute(insert_sql, (str(date), title, flag))
        else:
          continue
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
      #self.__cursor.close()
      self.__conn.commit()
    else:
      print('오류 발생')
      self.__conn.rollback()
  def select_table(self):
    select_sql = """SELECT * FROM MOVIE_INFO"""
    self.__cursor.execute(select_sql)
    rows = self.__cursor.fetchall()
    for row in rows:
      print(row)
      
postgre = DataBase()
data1 = [(20220209, 'title1', False),(20220210, 'title2', False)]
data2 = [(20220211, 'title3', False)]
postgre.create_table()
postgre.insert_data(data1)
postgre.insert_data(data2)
postgre.select_table()
postgre.clear_table()
postgre.select_table()
