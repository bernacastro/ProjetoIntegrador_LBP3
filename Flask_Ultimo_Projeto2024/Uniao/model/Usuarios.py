from database import database

class Usuarios(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha = database.Column(database.String(255), nullable=False)
    tipo = database.Column(database.String(20), nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False)

    emprestimos = database.relationship("Emprestimos", back_populates="usuario", lazy=True)
    reservas = database.relationship("Reservas", back_populates="usuario", lazy=True)
    multas = database.relationship("Multas", back_populates="usuario", lazy=True)

    def JSonificar(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo,
            "data_criacao": self.data_criacao.isoformat(),
            "emprestimos": [emprestimo.JSonificar() for emprestimo in self.emprestimos],
            "reservas": [reserva.JSonificar() for reserva in self.reservas],
            "multas": [multa.JSonificar() for multa in self.multas]
        }

