from database import database
from datetime import datetime

class Log(database.Model):
  id = database.Column(database.Integer, primary_key=True)
  timestamp = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)
  classe = database.Column(database.String(10), nullable=False)
  mensagem = database.Column(database.Text, nullable=False)

  def __repr__(self):
    return f"Tempo:{self.timestamp} Classe: {self.classe} Mensagem: {self.mensagem}"