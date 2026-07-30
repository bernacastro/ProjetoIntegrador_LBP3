from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from repository import LivroRepository, UsuarioRepository, LogRepository

livroController = Blueprint("bp_books", __name__)
livroRepository = LivroRepository()
usuarioRepository=UsuarioRepository()
logRepository = LogRepository()

# Rota para adicionar um novo livro
@livroController.route("/add", methods=['POST'])
def add_book():
    try:
        # Obtém os dados do formulário enviados pelo usuário
        titulo = request.form.get('titulo')  # Título do livro
        isbn = request.form.get('isbn')  # ISBN do livro
        data_publicacao = request.form.get('publicadoEm')  # Data de publicação do livro
        autor_id = request.form.get('autor_id')  # ID do autor do livro
        categoria_id = request.form.get('categoria_id')  # ID da categoria do livro
        quantidade_total = request.form.get('quantidade_total')  # Quantidade total de exemplares

        # Validação básica dos dados recebidos
        if not (titulo and isbn and data_publicacao and autor_id and categoria_id and quantidade_total):
            # Caso algum campo obrigatório esteja vazio, exibe uma mensagem de erro
            flash("Todos os campos são obrigatórios.", "error")
            return redirect(url_for('bp_inicio.index'))  # Redireciona de volta para a página inicial

        if (livroRepository.antiXSS(titulo) or
            livroRepository.antiXSS(data_publicacao) or
            livroRepository.antiXSS(autor_id) or
            livroRepository.antiXSS(categoria_id) or
            livroRepository.antiXSS(quantidade_total)):
            flash("Houve um erro: tentativa de XSS", "error")
            print("Tentativa de XSS")
            return redirect(url_for('bp_inicio.index'))
        
        # Exibe uma mensagem no console para verificar que os dados foram recebidos
        print("Livro recebido")

        # Chama o método addBook do repositório para adicionar o livro no banco de dados
        resultado = livroRepository.addBook(
            titulo=titulo,
            isbn=isbn,
            data_publicacao=data_publicacao,
            autor_id=autor_id,
            categoria_id=categoria_id,
            quantidade_total=quantidade_total
        )
        # Verifica se o resultado contém um erro e exibe a mensagem correspondente
        if "error" in resultado:
            flash(resultado["error"], "error")  # Mensagem de erro, caso haja
        else:
            logRepository.registrar_log("Livro adicionado com sucesso!", "success")
            flash("Livro adicionado com sucesso!", "success")  # Mensagem de sucesso, caso o livro seja adicionado com sucesso

        # Redireciona de volta para a página inicial
        return redirect(url_for('bp_inicio.index'))

    except Exception as e:
        # Caso ocorra alguma exceção durante o processo, captura o erro e exibe uma mensagem
        flash(f"Ocorreu um erro: {e}", "error")  # Exibe a mensagem de erro para o usuário
        return redirect(url_for('bp_inicio.index'))  # Redireciona de volta para a página inicial



@livroController.route('/livros', methods=['GET'])
def view_books():
    try:
        titulo = request.args.get('titulo', '').strip()
        autor_id = request.args.get('autor_id', '').strip()
        categoria_id = request.args.get('categoria_id', '').strip()
        data_inicio = request.args.get('data_inicio', '').strip()
        isbn = request.args.get('isbn', '').strip()

        livros = livroRepository.searchBooksCustom(
            titulo=titulo,
            autor_id=autor_id,
            categoria_id=categoria_id,
            data_inicio=data_inicio,
            isbn=isbn
        )

        autores = livroRepository.getAutores()
        categorias = livroRepository.getCategorias()

        if session.get("tipo") == "admin":
            return render_template(
                'Livro/livros-admin.html',
                livros=livros,
                autores=autores,
                categorias=categorias
            )
        else:
            return render_template(
                "Livro/livros-visitante.html",
                livros=livros,
                autores=autores,
                categorias=categorias
            )
    
    except Exception as e:
        logRepository.registrar_log("Erro ao carregar os livros", "error")
        flash(f"Erro ao carregar os livros: {e}", "error")
        return render_template('Livro/livros-admin.html', livros=[], autores=[], categorias=[])


@livroController.route('/editar/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    if request.method == 'POST':
        try:
            titulo = request.form.get('titulo')
            isbn = request.form.get('isbn')
            data_publicacao = request.form.get('data_publicacao')
            autor_id = request.form.get('autor_id')
            categoria_id = request.form.get('categoria_id')
            quantidade_total=request.form.get('quantidade_total')

            if not (titulo and isbn and data_publicacao  and autor_id and categoria_id and quantidade_total):
                flash("Todos os campos são obrigatórios.", "error")
                return redirect(url_for('bp_books.edit_book', id=id))

            resultado = livroRepository.updateBook(
                id, titulo, isbn, data_publicacao, autor_id, categoria_id, quantidade_total
            )

            if "error" in resultado:
                flash(resultado["error"], "error")
            else:
                flash("Livro atualizado com sucesso!", "success")

            return redirect(url_for('bp_books.view_books'))
        except Exception as e:
            flash(f"Erro ao atualizar o livro: {e}", "error")
            return redirect(url_for('bp_books.edit_book', id=id))

    livro = livroRepository.getBookById(id)
    autores = livroRepository.getAutores()
    categorias = livroRepository.getCategorias()

    return render_template('Livro/LivroEdit.html', livro=livro, autores=autores, categorias=categorias)


@livroController.route('/excluir/<int:id>', methods=['POST','GET'])
def delete_book(id):
    try:
        resultado = livroRepository.deleteBook(id)
        if "error" in resultado:
            flash(resultado["error"], "error")
        else:
            flash("Livro excluído com sucesso!", "success")

        return redirect(url_for('bp_books.view_books'))
    except Exception as e:
        flash(f"Erro ao excluir o livro: {e}", "error")
        return redirect(url_for('bp_books.view_books'))


@livroController.route("/")
def books_home():
    return redirect(url_for('bp_books.view_books'))


@livroController.route("/addLivrosBase", methods=['POST',"GET"])
def addBase():
    livros = [
        {"titulo": "O Senhor dos Anéis", "isbn": "9780345339706", "data_publicacao": "1954-07-29", "autor_id": 1, "categoria_id": 1, "quantidade_total": 5},
        {"titulo": "1984", "isbn": "9780451524935", "data_publicacao": "1949-06-08", "autor_id": 2, "categoria_id": 2, "quantidade_total": 10},
        {"titulo": "Orgulho e Preconceito", "isbn": "9780141439518", "data_publicacao": "1813-01-28", "autor_id": 3, "categoria_id": 3, "quantidade_total": 7},
        {"titulo": "A Arte da Guerra", "isbn": "9781599869773", "data_publicacao": "500-01-01", "autor_id": 4, "categoria_id": 4, "quantidade_total": 8},
        {"titulo": "O Pequeno Príncipe", "isbn": "9780156012195", "data_publicacao": "1943-04-06", "autor_id": 5, "categoria_id": 5, "quantidade_total": 12},
        {"titulo": "O Alquimista", "isbn": "9780061122415", "data_publicacao": "1988-05-01", "autor_id": 6, "categoria_id": 6, "quantidade_total": 10},
        {"titulo": "O Código Da Vinci", "isbn": "9780307474278", "data_publicacao": "2003-03-18", "autor_id": 7, "categoria_id": 7, "quantidade_total": 15},
        {"titulo": "Dom Quixote", "isbn": "9780060934347", "data_publicacao": "1605-01-01", "autor_id": 8, "categoria_id": 8, "quantidade_total": 6},
        {"titulo": "Harry Potter e a Pedra Filosofal", "isbn": "9780439554930", "data_publicacao": "1997-06-26", "autor_id": 9, "categoria_id": 9, "quantidade_total": 20},
        {"titulo": "O Hobbit", "isbn": "9780547928227", "data_publicacao": "1937-09-21", "autor_id": 10, "categoria_id": 1, "quantidade_total": 10},
        {"titulo": "O Guia do Mochileiro das Galáxias", "isbn": "9780345391803", "data_publicacao": "1979-10-12", "autor_id": 11, "categoria_id": 2, "quantidade_total": 9},
        {"titulo": "Cem Anos de Solidão", "isbn": "9780060883287", "data_publicacao": "1967-06-05", "autor_id": 12, "categoria_id": 3, "quantidade_total": 8},
        {"titulo": "A Revolução dos Bichos", "isbn": "9780451526342", "data_publicacao": "1945-08-17", "autor_id": 2, "categoria_id": 4, "quantidade_total": 14},
        {"titulo": "A Cabana", "isbn": "9780964729230", "data_publicacao": "2007-05-01", "autor_id": 13, "categoria_id": 5, "quantidade_total": 11},
        {"titulo": "A Menina que Roubava Livros", "isbn": "9780375842207", "data_publicacao": "2005-03-14", "autor_id": 14, "categoria_id": 6, "quantidade_total": 8},
        {"titulo": "Jogos Vorazes", "isbn": "9780439023481", "data_publicacao": "2008-09-14", "autor_id": 15, "categoria_id": 7, "quantidade_total": 9},
        {"titulo": "Duna", "isbn": "9780441172719", "data_publicacao": "1965-08-01", "autor_id": 16, "categoria_id": 8, "quantidade_total": 7},
        {"titulo": "A História Sem Fim", "isbn": "9780140386335", "data_publicacao": "1979-09-01", "autor_id": 17, "categoria_id": 9, "quantidade_total": 10},
        {"titulo": "O Apanhador no Campo de Centeio", "isbn": "9780316769488", "data_publicacao": "1951-07-16", "autor_id": 18, "categoria_id": 10, "quantidade_total": 5},
        {"titulo": "Crepúsculo", "isbn": "9780316015844", "data_publicacao": "2005-10-05", "autor_id": 19, "categoria_id": 11, "quantidade_total": 10},
    ]

    for livro in livros:
        livroRepository.addBook(
            titulo=livro["titulo"],
            isbn=livro["isbn"],
            data_publicacao=livro["data_publicacao"],
            autor_id=livro["autor_id"],
            categoria_id=livro["categoria_id"],
            quantidade_total=livro["quantidade_total"],
        )
    print("Catálogo de livros criado com sucesso!")
    return redirect(url_for('bp_inicio.index'))
