from flask import Blueprint, request, redirect, url_for, render_template, flash
from repository import UsuarioRepository, LogRepository
from hashlib import sha256
from datetime import datetime

usuarioController = Blueprint('bp_usuario', __name__)
usuariosRepository = UsuarioRepository()


@usuarioController.route('/add', methods=['POST','GET'])
def add_usuario():
    if request.method == "POST":
        try:
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            senha_correta = usuariosRepository.verificarSenha(senha)
            tipo = 'usuario'
            
            data_criacao = datetime.now().replace(second=0, microsecond=0)
            if not all([nome, email, senha, tipo, data_criacao]):
                flash("Todos os campos são obrigatórios.", "error")
                return redirect(url_for('bp_usuario.add_usuario'))
            
            if senha_correta != True:
                flash("Entrada inválida detectada. Verifique os campos e tente novamente.", "error")
                return redirect(url_for('bp_usuario.add_usuario'))
            
            senha = sha256(senha.encode('utf-8')).hexdigest()
            senha_correta = None

            if "@" not in email:
                flash("O email deve conter o símbolo @", "info")
                redirect(url_for('bp_usuario.add_usuario'))


            
            if usuariosRepository.antiXSS(nome) or usuariosRepository.antiXSS(email):
                flash("Entrada inválida detectada. Verifique os campos e tente novamente.", "error")
                return redirect(url_for('bp_usuario.add_usuario'))
            
            # Verifica se o e-mail ou nome já existem usando o repositório
            if usuariosRepository.usuario_existe_por_email(email):
                flash("E-mail já está em uso. Por favor, use outro.", "error")
                return redirect(url_for('bp_usuario.add_usuario'))

            if usuariosRepository.usuario_existe_por_nome(nome):
                flash("Nome de usuário já está em uso. Por favor, escolha outro.", "error")
                return redirect(url_for('bp_usuario.add_usuario'))

            response = usuariosRepository.novoUsuario(nome, email, senha, tipo, data_criacao)
            if isinstance(response, str):
                flash(response, "error")
            else:
                flash("Usuário criado com sucesso!", "success")
                return redirect(url_for('bp_inicio.login'))
            return redirect(url_for('bp_inicio.index'))
        except Exception as e:
            flash(f"Erro ao criar usuário: {e}", "error")
            print((f"Erro ao criar usuário: {e}", "error"))
            return redirect(url_for('bp_inicio.index'))
    return render_template('registrar.html')

@usuarioController.route('/', methods=['GET'])
def view_usuarios():
    try:
        # Busca todos os usuários para exibição
        usuarios = usuariosRepository.listarTodosJSON()
        return render_template("Usuario/usuarios.html", usuarios=usuarios)
    except Exception as e:
        flash(f"Erro ao carregar os usuários: {e}", "error")
        return render_template("Usuario/usuarios.html", usuarios=[])


@usuarioController.route('/editar/<int:usuario_id>', methods=['GET', 'POST'])
def edit_usuario(usuario_id):
    try:
        if request.method == 'POST':
            # Atualização de dados do usuário
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = sha256(request.form.get('senha').encode('utf-8')).hexdigest()
            senha = request.form.get('senha')
            senha_correta = usuariosRepository.verificarSenha(senha)

            
            tipo = request.form.get('tipo')
            data_criacao = datetime.now().replace(second=0, microsecond=0)


            if not all([nome, email, senha, tipo, data_criacao]):
                flash("Todos os campos são obrigatórios para atualizar.", "error")
                return redirect(url_for('bp_usuario.edit_usuario', usuario_id=usuario_id))
            
            if senha_correta != True:
                flash("Entrada inválida detectada. Verifique os campos e tente novamente.", "error")
                return redirect(url_for('bp_usuario.add_usuario'))
            
            senha = sha256(senha).encode('utf-8').hexdigest()
            senha_correta = None
            
            if usuariosRepository.antiXSS(nome) or usuariosRepository.antiXSS(email):
                flash("Entrada inválida detectada. Verifique os campos e tente novamente.", "error")
                print("Entrada inválida detectada. Verifique os campos e tente novamente.")
                return redirect(url_for('bp_usuario.add_usuario'))

            response = usuariosRepository.atualizar_usuario(usuario_id, nome, email, senha, tipo, data_criacao)
            if "Erro" in response:
                flash(response, "error")
            else:
                flash("Usuário atualizado com sucesso!", "success")

            return redirect(url_for('bp_usuario.view_usuarios'))

        # Recuperação do usuário para exibição no formulário
        usuario = usuariosRepository.buscarUsuarioPorId(usuario_id)
        if not usuario:
            flash("Usuário não encontrado.", "error")
            return redirect(url_for('bp_usuario.view_usuarios'))

        return render_template("Usuario/UsuarioEdit.html", usuario=usuario)
    except Exception as e:
        flash(f"Erro ao editar usuário: {e}", "error")
        return redirect(url_for('bp_usuario.view_usuarios'))


@usuarioController.route('/excluir/<int:usuario_id>', methods=['POST'])
def delete_usuario(usuario_id):
    try:
        response = usuariosRepository.deletar_usuario(usuario_id)
        if "Erro" in response:
            flash(response, "error")
        else:
            flash("Usuário excluído com sucesso!", "success")

        return redirect(url_for('bp_usuario.view_usuarios'))
    except Exception as e:
        flash(f"Erro ao excluir usuário: {e}", "error")
        return redirect(url_for('bp_usuario.view_usuarios'))


@usuarioController.route('/add_adm', methods=['POST','GET'])
def add_admin():
    try:
        nome = "adm"
        email = "adm@gmail.com"
        senha = sha256("adm".encode('utf-8')).hexdigest() 
        tipo = 'admin'
        data_criacao = datetime.now().replace(second=0, microsecond=0)


        response = usuariosRepository.novoUsuario(nome, email, senha, tipo, data_criacao)


        if isinstance(response, str):  
            flash(response, "error")
            return redirect(url_for('bp_inicio.index'))  
        else:
            flash("Usuário admin criado com sucesso!", "success")
            return redirect(url_for('bp_inicio.login'))  

    except Exception as e:
        flash(f"Erro ao criar usuário admin: {e}", "error")
        return redirect(url_for('bp_inicio.index'))  
