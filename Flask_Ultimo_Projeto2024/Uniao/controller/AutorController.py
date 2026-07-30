from flask import Blueprint, render_template, request, redirect, url_for, flash
from repository import AutorRepository, UsuarioRepository, LogRepository
from datetime import datetime

# Cria o blueprint para a rota de autores
authorController = Blueprint('bp_autores', __name__)

# Instancia o repositório de autores
autorRepository = AutorRepository()
usuarioRepository = UsuarioRepository()

# Exibe todos os autores
@authorController.route("/autores", methods=["GET"])
def view_autores():
    try:
        autores_json = autorRepository.searchAutoresJSON()
        return render_template("Autor/autores.html", autores=autores_json)
    except Exception as e:
        flash(f"Erro ao carregar autores: {e}", "error")
        return render_template("Autor/autores.html", autores=[])

# Adiciona um novo autor
@authorController.route("/autores/adicionar", methods=["POST"])
def add_autor():
    try:
        nome = request.form.get("nome")
        data_nascimentobruta = request.form.get("data_nascimento")
        nacionalidade = request.form.get("nacionalidade")

        if autorRepository.antiXSS(nome):
            flash("Houve um erro: tentativa de XSS", "error")
            print("Tentativa de XSS")
            return redirect(url_for('bp_inicio.index'))

        if autorRepository.antiXSS(nacionalidade):
            flash("Houve um erro: tentativa de XSS", "error")
            print("Tentativa de XSS")
            return redirect(url_for('bp_inicio.index'))

        if not nome or not data_nascimentobruta or not nacionalidade:
            flash("Todos os campos são obrigatórios.", "error")
            return redirect(url_for('bp_inicio.index'))
        
        data_nascimento = datetime.strptime(data_nascimentobruta, '%Y-%m-%d').date()
        mensagem = autorRepository.addAutor(nome, data_nascimento, nacionalidade)

        return redirect(url_for('bp_inicio.index'))
    except Exception as e:
        flash(f"Erro ao adicionar autor: {e}", "error")
        return redirect(url_for('bp_inicio.index'))

# Edita um autor existente
@authorController.route("/autores/editar/<int:id>", methods=["GET", "POST"])
def edit_autor(id):
    try:
        if request.method == "POST":
            nome = request.form.get("nome")
            data_nascimentoBruta = request.form.get("data_nascimento")
            nacionalidade = request.form.get("nacionalidade")

            if autorRepository.antiXSS(nome):
                flash("Houve um erro: tentativa de XSS", "error")
                print("Tentativa de XSS")
                return redirect(url_for('bp_inicio.index'))

            if autorRepository.antiXSS(nacionalidade):
                flash("Houve um erro: tentativa de XSS", "error")
                print("Tentativa de XSS")
                return redirect(url_for('bp_inicio.index'))
            if not nome or not data_nascimentoBruta or not nacionalidade:
                flash("Todos os campos são obrigatórios.", "error")
                return redirect(url_for('bp_autores.edit_autor', id=id))

            data_nascimento = datetime.strptime(data_nascimentoBruta, '%Y-%m-%d').date()
            mensagem = autorRepository.updateAutor(id, nome, data_nascimento, nacionalidade)
            flash(mensagem, "success" if "sucesso" in mensagem.lower() else "error")
            return redirect(url_for('bp_autores.view_autores'))
        
        autor = autorRepository.getAutorById(id)
        if not autor:
            flash(f"Autor com ID {id} não encontrado.", "error")
            return redirect(url_for('bp_autores.view_autores'))
        
        return render_template("Autor/AutorEdit.html", autor=autor)
    except Exception as e:
        flash(f"Erro ao editar autor: {e}", "error")
        return redirect(url_for('bp_autores.view_autores'))

# Exclui um autor
@authorController.route("/autores/excluir/<int:id>", methods=["POST","GET"])
def delete_autor(id):
    try:
        mensagem = autorRepository.deleteAutor(id)
        flash(mensagem, "success" if "sucesso" in mensagem.lower() else "error")
    except Exception as e:
        flash(f"Erro ao excluir autor: {e}", "error")
    return redirect(url_for('bp_autores.view_autores'))

# Página inicial redireciona para a lista de autores
@authorController.route("/")
def index():
    return redirect(url_for('bp_autores.view_autores'))


@authorController.route('/add_base', methods=['POST','GET'])
def add_varios_autores():
    try:
        # Lista de autores a serem adicionados
        autores = [
            {"nome": "J.R.R. Tolkien", "data_nascimento": "1892-01-03", "nacionalidade": "Britânico"},
            {"nome": "George Orwell", "data_nascimento": "1903-06-25", "nacionalidade": "Britânico"},
            {"nome": "Jane Austen", "data_nascimento": "1775-12-16", "nacionalidade": "Britânica"},
            {"nome": "Antoine de Saint-Exupéry", "data_nascimento": "1900-06-29", "nacionalidade": "Francês"},
            {"nome": "Paulo Coelho", "data_nascimento": "1947-08-24", "nacionalidade": "Brasileiro"},
            {"nome": "Dan Brown", "data_nascimento": "1964-06-22", "nacionalidade": "Americano"},
            {"nome": "Miguel de Cervantes", "data_nascimento": "1547-09-29", "nacionalidade": "Espanhol"},
            {"nome": "J.K. Rowling", "data_nascimento": "1965-07-31", "nacionalidade": "Britânica"},
            {"nome": "Douglas Adams", "data_nascimento": "1952-03-11", "nacionalidade": "Britânico"},
            {"nome": "Gabriel García Márquez", "data_nascimento": "1927-03-06", "nacionalidade": "Colombiano"},
            {"nome": "William P. Young", "data_nascimento": "1955-05-11", "nacionalidade": "Americano"},
            {"nome": "Markus Zusak", "data_nascimento": "1975-03-23", "nacionalidade": "Alemão-Australiano"},
            {"nome": "Suzanne Collins", "data_nascimento": "1962-08-10", "nacionalidade": "Americana"},
            {"nome": "Frank Herbert", "data_nascimento": "1920-10-08", "nacionalidade": "Americano"},
            {"nome": "Michael Ende", "data_nascimento": "1929-11-12", "nacionalidade": "Alemão"},
            {"nome": "J.D. Salinger", "data_nascimento": "1919-01-01", "nacionalidade": "Americano"},
            {"nome": "Stephenie Meyer", "data_nascimento": "1973-12-24", "nacionalidade": "Americana"}
        ]

        # Adiciona os autores ao banco de dados
        for autor in autores:
            # Validações
            if not autor["nome"] or not autor["data_nascimento"] or not autor["nacionalidade"]:
                flash("Todos os campos são obrigatórios.", "error")
                return redirect(url_for('bp_inicio.index'))
            
            # Converte a data de nascimento para o formato correto
            data_nascimento = datetime.strptime(autor["data_nascimento"], '%Y-%m-%d').date()
            # Adiciona o autor ao banco de dados
            mensagem = autorRepository.addAutor(autor["nome"], data_nascimento, autor["nacionalidade"])

        flash("Autores adicionados com sucesso!", "success")
        return redirect(url_for('bp_inicio.index'))

    except Exception as e:
        flash(f"Erro ao adicionar autores: {e}", "error")
        return redirect(url_for('bp_inicio.index'))
    