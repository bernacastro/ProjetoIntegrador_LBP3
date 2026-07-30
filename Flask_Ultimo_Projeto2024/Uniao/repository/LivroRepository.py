from DAO import LivroDAO
from datetime import datetime

class LivroRepository:
    def __init__(self):
        self.livroDAO = LivroDAO()

    def searchBooksJSON(self):
        try:
            livros = self.livroDAO.searchBooks()
            return [livro.JSonificar() for livro in livros]
        except Exception as e:
            return {"error": f"Erro ao buscar livros: {e}"}

    def addBook(self, titulo, isbn, data_publicacao, autor_id, categoria_id, quantidade_total):
        print("Adicionando livro...")
        try:
            data_publicacao_formatada = datetime.strptime(data_publicacao, "%Y-%m-%d").date()
            sucesso = self.livroDAO.addBook(
                titulo, isbn, data_publicacao_formatada,autor_id, categoria_id, quantidade_total
            )
            return {"success": sucesso}
        except ValueError as e:
            return {"error": f"Data de publicação inválida ({e})"}
        except Exception as e:
            return {"error": f"Erro ao adicionar livro: {e}"}

    def updateBook(self, id, titulo, isbn, data_publicacao, autor_id, categoria_id, quantidade_total):
        try:
            data_publicacao_formatada = datetime.strptime(data_publicacao, "%Y-%m-%d").date()
            sucesso = self.livroDAO.updateBook(
                id, titulo, isbn, data_publicacao_formatada, autor_id, categoria_id, quantidade_total
            )
            return {"success": sucesso}
        except ValueError as e:
            return {"error": f"Data de publicação inválida ({e})"}
        except Exception as e:
            return {"error": f"Erro ao atualizar livro: {e}"}

    def getBookById(self, id):
        try:
            return self.livroDAO.getBookById(id)
        except Exception as e:
            return {"error": f"Erro ao buscar livro por ID: {e}"}

    def getAutores(self):
        try:
            return self.livroDAO.getAutores()
        except Exception as e:
            return {"error": f"Erro ao buscar autores: {e}"}

    def getCategorias(self):
        try:
            return self.livroDAO.getCategorias()
        except Exception as e:
            return {"error": f"Erro ao buscar categorias: {e}"}
        
    def getEmprestimoByID(self, id):
        try:
            return self.livroDAO.getEmprestimoByID(id)
        except Exception as e:
            return {"error": f"Erro ao buscar Emprestimos: {e}"}

    def deleteBook(self, id):
        try:
            sucesso = self.livroDAO.deleteBook(id)
            return {"success": sucesso}
        except Exception as e:
            return {"error": f"Erro ao excluir livro: {e}"}

    def searchBooksCustom(self, titulo=None, autor_id=None, categoria_id=None, data_inicio=None, isbn=None):
        try:
            livros = self.livroDAO.searchBooksCustom(titulo, autor_id, categoria_id, data_inicio, isbn)
            return [livro.JSonificar() for livro in livros]
        except Exception as e:
            return {"error": f"Erro ao realizar consulta personalizada: {e}"}
        

    def atualizar_quantidade_disponivel(self, livro_id, aumentar=True):
        try:
            # Chama o método do DAO para atualizar a quantidade disponível
            livro = self.livroDAO.getBookById(livro_id)  # Busca o livro pelo ID
            if livro:
                if aumentar:
                    livro.quantidade_disponivel += 1  # Aumenta a quantidade disponível
                else:
                    livro.quantidade_disponivel -= 1  # Diminui a quantidade disponível
                self.livroDAO.atualizar_quantidade_disponivel(livro.id)  # Atualiza o livro no banco de dados
        except Exception as e:
            print(f"Erro ao atualizar a quantidade disponível do livro: {e}")

    def antiXSS(self, valor):
        try:
            caracteres_perigosos = ["<", ">", "&", "'", '"', "/", "script", "onerror", "onload","select","return","print","delete"]

            for char in caracteres_perigosos:
                if char in valor.lower():
                    return True
            return False
        except Exception as e:
            print(f"Erro ao verificar valor contra XSS: {e}")
            return None