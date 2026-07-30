from model import Autores
from database import database
from sqlalchemy.exc import SQLAlchemyError

class AutorDAO:
    @staticmethod
    def searchAutores():
        try:
            # Retorna todos os autores do banco de dados
            return Autores.query.all()
        except SQLAlchemyError as e:
            print(f"Erro ao buscar autores: {e}")
            return []

    @staticmethod
    def addAutor(nome: str, data_nascimento: str, nacionalidade: str):
        try:
            # Cria um novo objeto Autor
            novo_autor = Autores(
                nome=nome,
                data_nascimento=data_nascimento,
                nacionalidade=nacionalidade
            )
            # Adiciona o autor ao banco de dados
            database.session.add(novo_autor)
            # Confirma a transação
            database.session.commit()
            return True
        except SQLAlchemyError as e:
            # Em caso de erro, desfaz a transação
            database.session.rollback()
            print(f"Erro ao adicionar autor: {e}")
            return False

    @staticmethod
    def updateAutor(id: int, nome: str, data_nascimento: str, nacionalidade: str):
        try:
            # Busca o autor pelo ID
            autor = database.session.get(Autores, id)
            if autor:
                # Atualiza os campos do autor
                autor.nome = nome
                autor.data_nascimento = data_nascimento
                autor.nacionalidade = nacionalidade
                # Confirma a transação
                database.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            # Em caso de erro, desfaz a transação
            database.session.rollback()
            print(f"Erro ao atualizar autor: {e}")
            return False

    @staticmethod
    def getAutorById(id: int):
        try:
            # Retorna o autor pelo ID
            return database.session.get(Autores, id)
        except SQLAlchemyError as e:
            print(f"Erro ao buscar autor pelo ID {id}: {e}")
            return None

    @staticmethod
    def deleteAutor(id: int):
        try:
            # Busca o autor pelo ID
            autor = database.session.get(Autores, id)
            if autor:
                # Exclui o autor
                database.session.delete(autor)
                # Confirma a transação
                database.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            # Em caso de erro, desfaz a transação
            database.session.rollback()
            print(f"Erro ao excluir autor: {e}")
            return False
