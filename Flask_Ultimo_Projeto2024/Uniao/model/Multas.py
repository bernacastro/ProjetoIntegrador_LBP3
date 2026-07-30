from database import database


class Multas(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    usuario_id = database.Column(database.Integer, database.ForeignKey("usuarios.id"), nullable=False)
    valor = database.Column(database.Float, nullable=False)
    data_geracao = database.Column(database.DateTime, nullable=False)
    status = database.Column(database.String(20), nullable=False)
    emprestimo_id = database.Column(database.Integer, database.ForeignKey("emprestimos.id"), nullable=False)  

    usuario = database.relationship("Usuarios", back_populates="multas")
    emprestimo = database.relationship("Emprestimos", back_populates="multas", foreign_keys=[emprestimo_id])  

    def JSonificar(self):
        return {
            "id": self.id,
            "emprestimo": self.emprestimo,
            "usuario": self.usuario.nome,
            "valor": self.valor,
            "data_geracao": self.data_geracao.isoformat(),
            "status": self.status,
            "emprestimo_id": self.emprestimo_id
        }