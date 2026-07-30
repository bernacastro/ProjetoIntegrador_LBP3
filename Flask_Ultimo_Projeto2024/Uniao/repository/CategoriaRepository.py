from DAO import CategoriaDAO

class CategoriaRepository:
    def __init__(self):
        self.categoriaDAO = CategoriaDAO()

    def searchCategories(self, nome=''):
        try:
            if nome:
                return self.categoriaDAO.searchCategoriesByName(nome)
            return self.categoriaDAO.searchCategories()
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            return []

    def searchCategoriesJSON(self, nome=''):
        try:
            categorias = self.searchCategories(nome)
            return [categoria.JSonificar() for categoria in categorias]
        except Exception as e:
            print(f"Erro ao converter categorias para JSON: {e}")
            return []

    def addCategory(self, nome):
        try:
            sucesso = self.categoriaDAO.addCategory(nome)
            return "Categoria adicionada com sucesso!" if sucesso else "Erro ao adicionar a categoria..."
        except Exception as e:
            print(f"Erro ao processar adição de categoria: {e}")
            return "Erro interno ao adicionar a categoria..."

    def updateCategory(self, id, nome):
        try:
            sucesso = self.categoriaDAO.updateCategory(id, nome)
            return "Categoria atualizada com sucesso!" if sucesso else "Erro ao atualizar a categoria..."
        except Exception as e:
            print(f"Erro ao processar atualização de categoria: {e}")
            return "Erro interno ao atualizar a categoria..."

    def deleteCategory(self, id):
        try:
            sucesso = self.categoriaDAO.deleteCategory(id)
            return "Categoria excluída com sucesso!" if sucesso else "Erro ao excluir a categoria..."
        except Exception as e:
            print(f"Erro ao processar exclusão de categoria: {e}")
            return "Erro interno ao excluir a categoria..."

    def getCategoryById(self, id):
        try:
            return self.categoriaDAO.getCategoryById(id)
        except Exception as e:
            print(f"Erro ao buscar categoria por ID: {e}")
            return None

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