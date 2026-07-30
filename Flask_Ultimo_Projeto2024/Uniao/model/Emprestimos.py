from database import database
from datetime import datetime

class Emprestimos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    usuario_id = database.Column(database.Integer, database.ForeignKey("usuarios.id"), nullable=False)
    livro_id = database.Column(database.Integer, database.ForeignKey("livros.id"), nullable=False)
    data_emprestimo = database.Column(database.DateTime, nullable=False, default=datetime.now)
    data_devolucao_prevista = database.Column(database.DateTime, nullable=False)
    data_devolucao_real = database.Column(database.DateTime, nullable=True)

    usuario = database.relationship("Usuarios", back_populates="emprestimos")
    livro = database.relationship("Livros", back_populates="emprestimos")
    multas = database.relationship("Multas", back_populates="emprestimo")

    def JSonificar(self):
        return {
            "id": self.id,
            "usuario": self.usuario.nome,
            "multas": self.multas,
            "livro": self.livro.titulo,
            "data_emprestimo": self.data_emprestimo.isoformat(),
            "data_devolucao_prevista": self.data_devolucao_prevista.isoformat(),
            "data_devolucao_real": self.data_devolucao_real.isoformat() if self.data_devolucao_real else None
        }
