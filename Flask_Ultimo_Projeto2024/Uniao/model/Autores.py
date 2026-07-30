from database import database

class Autores(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    data_nascimento = database.Column(database.Date, nullable=True)
    nacionalidade = database.Column(database.String(50), nullable=False)

    livros = database.relationship("Livros", back_populates="autor", lazy=True)

    def JSonificar(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "nacionalidade": self.nacionalidade,
            "livros": [livro.JSonificar() for livro in self.livros]
        }