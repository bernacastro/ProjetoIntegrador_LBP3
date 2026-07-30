from DAO import LogDAO

class LogRepository:
    def __init__(self):
      self.dao = LogDAO()
    def registrar_log(self, mensagem, classe):
      self.dao.registrar_log(mensagem, classe)
