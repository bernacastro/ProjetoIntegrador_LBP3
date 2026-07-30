from flask import Blueprint, render_template, redirect, url_for, request, flash
from repository import CategoriaRepository, LogRepository

categoryController = Blueprint("bp_categories", __name__)

categoryRepository = CategoriaRepository()

@categoryController.route("/add", methods=['GET', 'POST'])
def add_category():
    if request.method == "POST":
        nome = request.form.get('categoria')
        if not nome:
            flash("O nome da categoria é obrigatório.", "error")
            return redirect(url_for('bp_categories.view_categories'))
        
        if categoryRepository.antiXSS(nome):
            flash("Houve um erro: tentativa de XSS", "error")
            print("Tentativa de XSS")
            return redirect(url_for('bp_inicio.index'))
        
        mensagem = categoryRepository.addCategory(nome)
        if "sucesso" in mensagem.lower():
            flash(mensagem, "success")
        else:
            flash(mensagem, "error")
        
        return redirect(url_for('bp_categories.view_categories'))
    
    return render_template('Categorias/CategoriaAdd.html')

@categoryController.route('/categorias', methods=['GET'])
def view_categories():
    nome = request.args.get('nome', '').strip()
    categorias = categoryRepository.searchCategories(nome)
    return render_template('Categorias/categorias.html', categorias=categorias, nome=nome)

@categoryController.route('/editar/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    categoria = categoryRepository.getCategoryById(id)

    if not categoria: #Se categoria não existe
        flash(f"Categoria com ID {id} não encontrada.", "error")
        return redirect(url_for('bp_categories.view_categories'))

    if request.method == 'POST':
        nome = request.form.get('categoria')
        if not nome:
            flash("O nome da categoria é obrigatório.", "error")
            return redirect(url_for('bp_categories.edit_category', id=id))
        
        mensagem = categoryRepository.updateCategory(id, nome)
        if "sucesso" in mensagem.lower():
            flash(mensagem, "success")
        else:
            flash(mensagem, "error")
        
        return redirect(url_for('bp_categories.view_categories'))
    
    return render_template('Categorias/CategoriaEdit.html', categoria=categoria)

# Rota para excluir uma categoria
@categoryController.route('/excluir/<int:id>', methods=['POST','GET'])
def delete_category(id):
    mensagem = categoryRepository.deleteCategory(id)
    if "sucesso" in mensagem.lower():
        flash(mensagem, "success")
    else:
        flash(mensagem, "error")
    return redirect(url_for('bp_categories.view_categories'))

@categoryController.route('/add_base', methods=['POST','GET'])
def criar_categorias_demo():
    categorias = [
        "Ficção Científica",
        "Romance",
        "Ficção Fantástica",
        "Clássicos",
        "Autoajuda",
        "Biografias",
        "Suspense",
        "História",
        "Literatura Infantil",
        "Distopia",
        "Aventura",
        "Poesia",
        "Negócios",
        "Espiritualidade",
        "Tecnologia",
        "Saúde e Bem-Estar",
        "Ciências",
        "Mistério",
        "Arte e Design",
        "Culinária"
    ]

    for categoria in categorias:
        mensagem = categoryRepository.addCategory(categoria)
        if "sucesso" in mensagem.lower():
            print(f"Categoria '{categoria}' adicionada com sucesso!")
        else:
            print(f"Erro ao adicionar categoria '{categoria}': {mensagem}")
    print("Processo de criação de categorias concluído.")
