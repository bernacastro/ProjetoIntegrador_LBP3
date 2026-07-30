from database import database
from model import Emprestimos, Usuarios,Livros,Multas
from DAO import LivroDAO
livroDAO=LivroDAO()

class EmprestimosDAO:
    @staticmethod
    def criar_emprestimo(usuario_id, livro_id, data_emprestimo, data_devolucao_prevista):
        emprestimo = Emprestimos(
            usuario_id=usuario_id,
            livro_id=livro_id,
            data_emprestimo=data_emprestimo,
            data_devolucao_prevista=data_devolucao_prevista
        )
        database.session.add(emprestimo)
        database.session.commit()

        return emprestimo

    @staticmethod
    def listar_todos():
        return Emprestimos.query.all()

    @staticmethod
    def buscar_por_id(emprestimo_id):
        try:
            emprestimo = Emprestimos.query.get(emprestimo_id)
            if emprestimo:
                return emprestimo
            else:
                print(f"Empréstimo com ID {emprestimo_id} não encontrado.")
                return None
        except Exception as e:
            print(f"Erro ao buscar empréstimo com ID {emprestimo_id}: {e}")
            return None


    @staticmethod
    def atualizar_devolucao(emprestimo_id, usuario_id, livro_id, data_emprestimo, data_devolucao_prevista):
        emprestimo = Emprestimos.query.get(emprestimo_id)
        if emprestimo:
            emprestimo.usuario_id = usuario_id
            emprestimo.livro_id = livro_id
            emprestimo.data_emprestimo = data_emprestimo
            emprestimo.data_devolucao_prevista = data_devolucao_prevista
            emprestimo.data_devolucao_real=None
            database.session.commit()
            return emprestimo
        return None

    @staticmethod
    def deletar_emprestimo(emprestimo_id):
        try:
            emprestimo = Emprestimos.query.get(emprestimo_id)
            
            if emprestimo:
                multa = Multas.query.filter(Multas.emprestimo_id == emprestimo_id).first() 
                if multa:
                    database.session.delete(multa)
                
                # Exclui o empréstimo
                database.session.delete(emprestimo)
                database.session.commit()
                return True
            return False
        except Exception as e:
            # Em caso de erro, faz o rollback e retorna False
            database.session.rollback()
            return f"Erro ao excluir o empréstimo e a multa: {str(e)}"

    @staticmethod
    def listar_por_usuario(usuario_id):
        return Emprestimos.query.filter_by(usuario_id=usuario_id).all()

    @staticmethod
    def listar_por_livro(livro_id):
        return Emprestimos.query.filter_by(livro_id=livro_id).all()
    
    @staticmethod
    def getUsuarios():
        try:
            return Usuarios.query.all()
        except Exception as e:
            print(f"Erro ao buscar autores: {e}")
            return []

    @staticmethod
    def getLivros():
        try:
            return Livros.query.all()
        except Exception as e:
            print(f"Erro ao buscar livros: {e}")
            return []

    @staticmethod
    def atualizar_data_devolucao_real(emprestimo_id, data_devolucao_real):
        emprestimo = Emprestimos.query.get(emprestimo_id)
        if emprestimo:
            emprestimo.data_devolucao_real = data_devolucao_real
            database.session.commit()


            return True
        return False