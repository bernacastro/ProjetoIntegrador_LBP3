from flask import Blueprint, render_template,request,session,redirect,url_for,flash
from hashlib import sha256
from DAO import AutorDAO, LivroDAO, CategoriaDAO,UsuarioDAO, EmprestimosDAO
from repository import UsuarioRepository, LogRepository
# Criação de um Blueprint chamado "bp_authors" para gerenciar rotas relacionadas a autores
padraoController = Blueprint("bp_inicio", __name__)
usuarioRepository= UsuarioRepository()

# Rota inicial para renderizar uma página específica para autores
@padraoController.route("/sucess")
def sucess():
        livros=LivroDAO.searchBooksCustom()
        categorias=CategoriaDAO.searchCategories()
        autores=AutorDAO.searchAutores()
        usuarios=UsuarioDAO.listar_todos()
        emprestimos=EmprestimosDAO.listar_todos()
        nome = session['nome']
        if session.get("tipo") != "admin":
            return render_template("homeLOGADA.html", livros=livros, nome=nome, autores=autores, categorias=categorias,usuarios=usuarios, emprestimos=emprestimos)
        return render_template("admin.html", livros=livros, nome=nome, autores=autores, categorias=categorias,usuarios=usuarios, emprestimos=emprestimos)

@padraoController.route("/")
def index():
    if 'usuario' in session:
        return redirect(url_for('bp_inicio.sucess'))

    return render_template("home.html", nome="Visitante")

@padraoController.route("/login", methods=["GET", "POST"])
def login():
    if 'usuario' in session:
        flash(f"Você já está logado como {session['nome']}!", "info")
        return redirect(url_for('bp_inicio.sucess'))
    

    if request.method == "POST":
        usuario = request.form["usuario"].strip()  # Remove espaços extras
        senha = sha256(request.form.get('senha').encode('utf-8')).hexdigest()
        try:
            if "@" in usuario:
                user = usuarioRepository.usuario_existe_por_email(usuario)
            else:
                user = usuarioRepository.usuario_existe_por_nome(usuario)

            if usuarioRepository.antiXSS(usuario) or usuarioRepository.antiXSS(senha):

                flash("Houve um erro: tentativa de XSS", "error")
                print("Tentativa de XSS")
                redirect(url_for('bp_inicio.index'))
            if user and user.senha == senha:
                session['usuario'] = user.email
                session['nome'] = user.nome
                session['tipo'] = user.tipo

                flash(f"Bem-vindo, {user.nome}!", "success")
                return redirect(url_for('bp_inicio.sucess')) 
            else:
                flash("Usuário ou senha inválidos. Tente novamente.", "error")
        except Exception as e:
            flash(f"Ocorreu um erro ao tentar fazer login: {e}", "error")

        return redirect(url_for('bp_inicio.index'))

    return render_template("login.html")


@padraoController.route("/logout")
def logout():
    session.clear()  # Limpa a sessão
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for('bp_inicio.login'))