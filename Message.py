import telegram
import key

class MessageBot:
  def __init__(self):
    self.__token = key.TOKEN
    self.__id = key.CHAT_ID
    self._bot = telegram.Bot(token = self.__token)

  @property
  def id(self):
    return self.__id
  @id.getter
  def id(self):
    return self.__id
  @property
  def token(self):
    return self.__token
  @token.getter
  def token(self):
    return self.__token

  def test_send_msg(self):
    self._bot.send_message(chat_id = self.__id, text = '테스트 메시지 입니다.')

  def send_msg(self, send_text):
    self._bot.send_message(chat_id = self.__id, text = send_text)

# bot = MessageBot()
# print('chat id is : ', bot.id)
# print("token is : ", bot.token)

# bot.test_send_msg()
