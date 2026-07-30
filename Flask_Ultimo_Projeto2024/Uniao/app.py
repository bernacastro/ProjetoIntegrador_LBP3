from flask import Flask,render_template,flash
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
    flash('A url da pagina parece estar incorreta, tente voltar para a pagina de login','warning')
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

if __name__ == "__main__":
    app.run(debug=True)

