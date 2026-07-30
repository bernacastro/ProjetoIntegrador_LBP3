from database import database

class Categorias(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(50), nullable=False)

    livros = database.relationship("Livros", back_populates="categoria", lazy=True)

    def JSonificar(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "livros": [livro.JSonificar() for livro in self.livros]
        }