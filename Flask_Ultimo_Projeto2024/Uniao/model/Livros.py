from database import database

class Livros(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(150), nullable=False)
    isbn = database.Column(database.String(13), unique=True, nullable=False)
    data_publicacao = database.Column(database.Date, nullable=True)
    autor_id = database.Column(database.Integer, database.ForeignKey("autores.id"), nullable=True)
    categoria_id = database.Column(database.Integer, database.ForeignKey("categorias.id"), nullable=True)
    quantidade_total = database.Column(database.Integer, nullable=False)
    quantidade_disponivel = database.Column(database.Integer, nullable=True)

    autor = database.relationship("Autores", back_populates="livros", lazy=True)
    categoria = database.relationship("Categorias", back_populates="livros", lazy=True)

    reservas = database.relationship("Reservas", back_populates="livro", lazy=True)
    emprestimos = database.relationship("Emprestimos", back_populates="livro", lazy=True)

    def JSonificar(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "isbn": self.isbn,
            "data_publicacao": self.data_publicacao.isoformat() if self.data_publicacao else None,
            "autor": self.autor.nome if self.autor else "Autor não definido",
            "categoria": self.categoria.nome if self.categoria else "Categoria não definida",
            "quantidade_total": self.quantidade_total,
            "quantidade_disponivel": self.quantidade_disponivel
        }
