from database import database
from model import Usuarios

class UsuarioDAO:
    @staticmethod
    def novo_usuario(nome,email,senha,tipo,data_criacao):
        usuario = Usuarios( 
            nome=nome,
            email=email,
            senha=senha,
            tipo=tipo,
            data_criacao=data_criacao
            )
        
        database.session.add(usuario)
        database.session.commit()
        return usuario

    @staticmethod
    def listar_todos():
        return Usuarios.query.all()

    @staticmethod
    def buscar_por_id(usuario_id):
        return Usuarios.query.get(usuario_id)

    @staticmethod
    def atualizar_usuario(usuario_id, nome,email,senha,tipo,data_criacao):
        usuario = Usuarios.query.get(usuario_id)
        if usuario:
            usuario.nome = nome
            usuario.email = email
            usuario.senha = senha
            usuario.tipo = tipo
            usuario.data_criacao = data_criacao
            database.session.commit()
            return usuario
        return None

    @staticmethod
    def deletar_usuario(usuario_id):
        usuario = Usuarios.query.get(usuario_id)
        if usuario:
            database.session.delete(usuario)
            database.session.commit()
            return True
        return False

    @staticmethod
    def listar_por_usuario(usuario_id):
        return Usuarios.query.filter_by(usuario_id=usuario_id).all()

    @staticmethod
    def listar_por_livro(livro_id):
        return Usuarios.query.filter_by(livro_id=livro_id).all()

    def buscar_por_email(self, email):
        return Usuarios.query.filter_by(email=email).first()

    def buscar_por_nome(self, nome):
        return Usuarios.query.filter_by(nome=nome).first()