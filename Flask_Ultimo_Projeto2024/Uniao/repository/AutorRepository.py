from flask import redirect, url_for
from DAO import AutorDAO

class AutorRepository:
    def __init__(self):
        self.autorDAO = AutorDAO()

    def searchAutoresJSON(self):
        try:
            autores = self.autorDAO.searchAutores()
            return [autor.JSonificar() for autor in autores]
        except Exception as e:
            print(f"Erro ao buscar autores: {e}")
            return []

    def addAutor(self, nome: str, data_nascimento: str, nacionalidade: str):
        try:
            sucesso = self.autorDAO.addAutor(nome, data_nascimento, nacionalidade)
            if sucesso:
                return redirect(url_for("bp_autores.view_autores"))
            return "Erro ao adicionar o autor..."
        except Exception as e:
            print(f"Erro no processo de adição de autor: {e}")
            return "Erro interno ao adicionar o autor..."

    def updateAutor(self, id: int, nome: str, data_nascimento: str, nacionalidade: str):
        try:
            sucesso = self.autorDAO.updateAutor(id, nome, data_nascimento, nacionalidade)
            return "Autor atualizado com sucesso!" if sucesso else "Erro ao atualizar o autor no banco de dados..."
        except Exception as e:
            return f"Erro no processo de atualização: {e}"

    def getAutorById(self, id: int):
        try:
            return self.autorDAO.getAutorById(id)
        except Exception as e:
            print(f"Erro ao buscar autor por ID: {e}")
            return None

    def deleteAutor(self, id: int):
        try:
            sucesso = self.autorDAO.deleteAutor(id)
            return "Autor excluído com sucesso!" if sucesso else "Erro ao excluir o autor..."
        except Exception as e:
            print(f"Erro no processo de exclusão: {e}")
            return "Erro interno ao excluir o autor..."
        
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