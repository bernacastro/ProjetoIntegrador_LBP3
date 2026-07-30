from model import Livros, Autores, Categorias,Emprestimos, Multas
from database import database


class LivroDAO:
    @staticmethod
    def searchBooks():
        try:
            return Livros.query.all()
        except Exception as e:
            print(f"Erro ao buscar livros: {e}")
            return []

    @staticmethod
    def addBook(titulo, isbn, data_publicacao, autor_id, categoria_id, quantidade_total):
        try:
            novo_livro = Livros(
                titulo=titulo,
                isbn=isbn,
                data_publicacao=data_publicacao,
                quantidade_total=quantidade_total,
                autor_id=autor_id,
                categoria_id=categoria_id,
            )
            database.session.add(novo_livro)
            print("Livro adicionado!")
            database.session.commit()
            print("Livro commitado!")
            return True
        except Exception as e:
            database.session.rollback()
            print(f"Erro ao adicionar livro: {e}")
            return False

    @staticmethod
    def updateBook(id, titulo, isbn, data_publicacao, autor_id, categoria_id, quantidade_total):
        try:
            livro = Livros.query.get(id)
            if not livro:
                print(f"Livro com ID {id} não encontrado.")
                return False

            livro.titulo = titulo
            livro.isbn = isbn
            livro.data_publicacao = data_publicacao
            livro.autor_id = autor_id
            livro.categoria_id = categoria_id
            livro.quantidade_total = quantidade_total

            # Atualiza a quantidade disponível após modificar o livro
            LivroDAO.atualizar_quantidade_disponivel(livro.id)

            database.session.commit()
            return True
        except Exception as e:
            database.session.rollback()
            print(f"Erro ao atualizar livro: {e}")
            return False

    @staticmethod
    def getBookById(id):
        try:
            return Livros.query.get(id)
        except Exception as e:
            print(f"Erro ao buscar livro por ID: {e}")
            return None

    @staticmethod
    def getAutores():
        try:
            return Autores.query.all()
        except Exception as e:
            print(f"Erro ao buscar autores: {e}")
            return []

    @staticmethod
    def getCategorias():
        try:
            return Categorias.query.all()
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            return []

    @staticmethod
    def deleteBook(id):
        try:
            livro = Livros.query.get(id)
            if not livro:
                print(f"Livro com ID {id} não encontrado.")
                return False

            # Exclui os empréstimos associados ao livro
            emprestimos = Emprestimos.query.filter_by(livro_id=id).all()
            for emprestimo in emprestimos:
                multas = Multas.query.filter_by(emprestimo_id=emprestimo.id).all()
                for multa in multas:
                    database.session.delete(multa)
                    print(f"Multa com ID {multa.id} excluída.")
                database.session.delete(emprestimo)
                print(f"Empréstimo com ID {emprestimo.id} excluído.")

            database.session.delete(livro)
            database.session.commit()
            print(f"Livro com ID {id} excluído com sucesso!")
            return True
        except Exception as e:
            database.session.rollback()
            print(f"Erro ao excluir livro: {e}")
            return False

    @staticmethod
    def searchBooksCustom(titulo=None, autor_id=None, categoria_id=None, data_inicio=None, isbn=None):
        try:
            query = Livros.query
            if titulo:
                query = query.filter(Livros.titulo.like(f"%{titulo}%"))
            if autor_id:
                query = query.filter(Livros.autor_id == autor_id)
            if categoria_id:
                query = query.filter(Livros.categoria_id == categoria_id)
            if data_inicio:
                query = query.filter(Livros.data_publicacao >= data_inicio)
            if isbn:
                query = query.filter(Livros.isbn.like(f"%{isbn}%"))
            return query.all()
        except Exception as e:
            print(f"Erro ao realizar consulta personalizada: {e}")
            return []

    @staticmethod
    def atualizar_quantidade_disponivel(livro_id):
        try:
            livro = Livros.query.get(livro_id)
            if livro:
                livro.quantidade_total = int(livro.quantidade_total)
                
                quantidade_emprestados = len(Emprestimos.query.filter_by(livro_id=livro.id, data_devolucao_real=None).all())
                
                quantidade_emprestados = int(quantidade_emprestados)
                
                livro.quantidade_disponivel = livro.quantidade_total - quantidade_emprestados
                database.session.commit()
                print(f"Quantidade disponível do livro {livro_id} atualizada.")
        except Exception as e:
            print(f"Erro ao atualizar quantidade disponível do livro: {e}")

    @staticmethod
    def getEmprestimoById(id):
        try:
            emprestimo = Emprestimos.query.get(id)
            if not emprestimo:
                print(f"Empréstimo com ID {id} não encontrado.")
                return None
            return emprestimo
        except Exception as e:
            print(f"Erro ao buscar empréstimo por ID: {e}")
            return None
