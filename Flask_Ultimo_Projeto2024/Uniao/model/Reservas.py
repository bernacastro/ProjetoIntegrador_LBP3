from database import database

class Reservas(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    usuario_id = database.Column(database.Integer, database.ForeignKey("usuarios.id"), nullable=False)
    livro_id = database.Column(database.Integer, database.ForeignKey("livros.id"), nullable=False)
    data_reserva = database.Column(database.DateTime, nullable=False)
    status = database.Column(database.String(20), nullable=False)

    usuario = database.relationship("Usuarios", back_populates="reservas")
    livro = database.relationship("Livros", back_populates="reservas")

    def JSonificar(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "livro_id": self.livro_id,
            "data_reserva": self.data_reserva.isoformat(),
            "status": self.status
        }

