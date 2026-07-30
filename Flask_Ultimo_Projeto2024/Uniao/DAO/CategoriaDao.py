from model import Categorias
from database import database

class CategoriaDAO:
    @staticmethod
    def searchCategories():
        try:
            return Categorias.query.all()
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            return []

    @staticmethod
    def searchCategoriesByName(nome):
        try:
            return Categorias.query.filter(Categorias.nome.ilike(f'%{nome}%')).all()
        except Exception as e:
            print(f"Erro ao buscar categorias por nome: {e}")
            return []

    @staticmethod
    def addCategory(nome):
        try:
            nova_categoria = Categorias(nome=nome)
            database.session.add(nova_categoria)
            database.session.commit()
            return True
        except Exception as e:
            database.session.rollback()
            print(f"Erro ao adicionar categoria: {e}")
            return False

    @staticmethod
    def updateCategory(id, nome):
        try:
            categoria = database.session.get(Categorias, id)
            if categoria:
                categoria.nome = nome
                database.session.commit()
                return True
            else:
                print("Erro: Categoria não encontrada")
                return False
        except Exception as e:
            database.session.rollback()
            print(f"Erro ao atualizar categoria: {e}")
            return False

    @staticmethod
    def deleteCategory(id):
        try:
            categoria = database.session.get(Categorias, id)
            if categoria:
                database.session.delete(categoria)
                database.session.commit()
                return True
            else:
                print("Erro: Categoria não encontrada")
                return False
        except Exception as e:
            database.session.rollback()
            print(f"Erro ao excluir categoria: {e}")
            return False

    @staticmethod
    def getCategoryById(id):
        try:
            return database.session.get(Categorias, id)
        except Exception as e:
            print(f"Erro ao buscar categoria por ID: {e}")
            return None
