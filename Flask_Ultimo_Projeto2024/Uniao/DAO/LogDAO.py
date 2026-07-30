from database import database
from model import Log

class LogDAO:
  @staticmethod
  def registrar_log(mensagem, classe):
      try:
        log = Log(mensagem=mensagem, classe=classe)
        database.session.add(log)
        database.session.commit()
      except Exception as e:
        database.session.rollback()
        print(f"Erro ao gravar Log: {e}")
        return False