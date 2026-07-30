from flask import Flask, render_template, flash, request, abort, session
from database import init_database
from controller.AutorController import authorController
from controller.LivroController import livroController
from controller.CategoriasController import categoryController
from controller.Iniciocontroller import padraoController
from controller.EmpresimoController import emprestimoController
from controller.UsuarioController import usuarioController
from controller.MultasController import multasController

app = Flask(__name__)
app.secret_key = '4a466f32ff8af1aad05ac24b5eced2531da40d014c105d9f67caf44c73fd73fc'

rotas_privadas_administrativas = ['static',
    'bp_autores.add_autor',
    'bp_autores.add_varios_autores',
    'bp_autores.edit_autor',
    'bp_autores.delete_autor',
    'bp_categories.add_category',
    'bp_categories.criar_categorias_demo',
    'bp_categories.edit_category',
    'bp_categories.delete_category',
    'bp_loan.add_emprestimo',
    'bp_loan.edit_emprestimo',
    'bp_loan.marcar_devolvido',
    'bp_loan.deletar_emprestimo',
    'bp_loan.listar_por_usuario',
    'bp_multas.gerar_multa',
    'bp_multas.excluir_multa',
    'bp_usuario.view_usuarios',
    'bp_usuario.edit_usuario',
    'bp_usuario.delete_usuario'
    'bp_books.addBase',
    'bp_books.add_book',
    'bp_books.edit_book',
    'bp_books.delete_book',
    'bp_multas.gerar_multa',
    'bp_multas.pagar_multa',
    'bp_multas.excluir_multa',

]

rotas_publicas = ['static',
    'bp_inicio.index',
    'bp_inicio.login',
    'bp_books.view_books',
    'bp_usuario.add_usuario',
    'bp_usuario.add_admin'
]

rotas_privadas = ['static',
    'bp_autores.view_autores',
    'bp_autores.index',
    'bp_categories.view_categories',
    'bp_loan.listar_por_livro',
    'bp_loan.view_emprestimos',
    'bp_inicio.sucess',
    'bp_inicio.logout',
    'bp_multas.listar_multas'
]

@app.before_request
def verificaSessao():

    if request.endpoint not in rotas_publicas:
        if "usuario" not in session:
            print("Bloqueado - Usuário não autenticado. Crie sua conta para (talvez) obter acesso")
            flash("Bloqueado - Usuário não autenticado. Crie sua conta para (talvez) obter acesso")
            abort(403)

        if request.endpoint in rotas_privadas_administrativas:
            if session.get("tipo") != "admin":
                print("Acesso negado - Usuário tentando acessar rota com nível hierárquico superior ao seu")
                flash("Acesso negado - Usuário tentando acessar rota com nível hierárquico superior ao seu")
                abort(403) 

    return


init_database(app)

app.register_blueprint(emprestimoController, url_prefix="/loan")
app.register_blueprint(multasController, url_prefix="/fine")
app.register_blueprint(authorController, url_prefix="/authors")
app.register_blueprint(livroController, url_prefix="/books")
app.register_blueprint(categoryController, url_prefix="/categories")
app.register_blueprint(usuarioController,url_prefix="/users")
app.register_blueprint(padraoController, url_prefix="/")

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    flash('A url da pagina parece estar incorreta :(', 'warning')
    return render_template('Erros/404.html'), 404

@app.errorhandler(403)
def acesso_negado(e):
    print(e)
    return render_template('Erros/403.html'), 403

@app.errorhandler(401)
def nao_autorizado(e):
    print(e)
    return render_template('Erros/401.html'), 401


@app.errorhandler(Exception)
def handle_generic_error(e):
    print(e)
    return render_template('Erros/erro.html', message=str(e)), 500

def antiXSS(valor):
        for char in valor:
            if char == "<" or char ==">" or char == "'" or char == "=" or char == '"':
                print("Erro: tentativa de XSS")
                return True
            
if __name__ == "__main__":
    app.run(debug=True)
