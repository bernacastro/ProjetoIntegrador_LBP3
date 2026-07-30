from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from repository import EmprestimosRepository, LogRepository, LivroRepository, UsuarioRepository
from datetime import datetime

emprestimoController = Blueprint('bp_loan', __name__)
emprestimosRepository = EmprestimosRepository()
livro_repository = LivroRepository()
usuarioRepository = UsuarioRepository()

@emprestimoController.route('/add', methods=['POST','GET'])
def add_emprestimo():
    if request.method=="POST":
        try:
            # Coleta de dados do formulário
            usuario_id = request.form.get('usuario_id')
            livro_id = request.form.get('livro_id')
            data_emprestimo = datetime.now().replace(second=0, microsecond=0)
            data_devolucao_prevista_bruta = request.form.get('data_devolucao_prevista')
            data_devolucao_prevista = datetime.strptime(data_devolucao_prevista_bruta, '%Y-%m-%d')

            if not all([usuario_id, livro_id, data_emprestimo, data_devolucao_prevista]):
                flash("Todos os campos são obrigatórios.", "error")
                return redirect(url_for('bp_loan.view_emprestimos'))
            
            if (emprestimosRepository.antiXSS(usuario_id) or emprestimosRepository.antiXSS(livro_id) or
                emprestimosRepository.antiXSS(data_emprestimo) or emprestimosRepository.antiXSS(data_devolucao_prevista_bruta) or
                emprestimosRepository.antiXSS(data_devolucao_prevista)) == True:
                flash("Houve um erro: tentativa de XSS", "error")
                print("Tentativa de XSS")
                redirect(url_for('bp_inicio.index'))


            response = emprestimosRepository.criarEmprestimo(
                usuario_id, livro_id, data_emprestimo, data_devolucao_prevista
            )
            if isinstance(response, str):
                flash(response, "error")
            else:
                flash("Empréstimo criado com sucesso!", "success")

                livro_id=int(livro_id)
                livro_repository.atualizar_quantidade_disponivel(livro_id)

            return redirect(url_for('bp_loan.view_emprestimos'))
        except Exception as e:
            flash(f"Erro ao criar empréstimo: {e}", "error")
            return redirect(url_for('bp_loan.view_emprestimos'))
    return redirect(url_for('bp_inicio.sucess'))



@emprestimoController.route('/', methods=['GET'])
def view_emprestimos():
    try:
            # Busca todos os empréstimos para exibição
        emprestimos = emprestimosRepository.listarTodosJSON()
        usuarios = emprestimosRepository.getUsuarios()
        livros = emprestimosRepository.getLivros()
        return render_template("Emprestimo/emprestimos.html", emprestimos=emprestimos, livros=livros, usuarios=usuarios)
        

    except Exception as e:
        flash(f"Erro ao carregar os empréstimos: {e}", "error")
        print(f"Erro ao carregar os empréstimos: {e}", "error")
        return render_template("Emprestimo/emprestimos.html", emprestimos=[])


@emprestimoController.route('/editar/<int:emprestimo_id>', methods=['GET', 'POST'])
def edit_emprestimo(emprestimo_id):
    try:
        if request.method == 'POST':
            usuario_id = request.form.get('usuario_id')
            livro_id = request.form.get('livro_id')
            data_emprestimo_bruta = request.form.get('data_emprestimo')
            data_emprestimo = datetime.strptime(data_emprestimo_bruta, '%Y-%m-%d').date()
            data_devolucao_prevista_bruta = request.form.get('data_devolucao_prevista')
            data_devolucao_prevista = datetime.strptime(data_devolucao_prevista_bruta, '%Y-%m-%d').date()
            print(type(data_devolucao_prevista_bruta), type(data_devolucao_prevista))

            if not all([usuario_id, livro_id, data_emprestimo, data_devolucao_prevista]):
                flash("Todos os campos são obrigatórios.", "error")
                print("Todos os campos são obrigatórios.", "error")
                return redirect(url_for('bp_loan.edit_emprestimo', emprestimo_id=emprestimo_id))

            response = emprestimosRepository.atualizar_devolucao(emprestimo_id, usuario_id, livro_id, data_emprestimo, data_devolucao_prevista)
            if "Erro" in response:
                flash(response, "error")
                print(response, "error")
            else:
                flash("Devolução atualizada com sucesso!", "success")
                print("Devolução atualizada com sucesso!", "success")

                
                livro = livro_repository.getBookById(livro_id)
                print(livro.titulo)
                if livro:
                    livro_repository.atualizar_quantidade_disponivel(livro.id)

            return redirect(url_for('bp_loan.view_emprestimos'))

        # Recuperação do empréstimo para exibição no formulário
        emprestimo = emprestimosRepository.buscarEmprestimoPorId(emprestimo_id)
        usuarios = emprestimosRepository.getUsuarios()
        livros = emprestimosRepository.getLivros()
        if not emprestimo:
            flash("Empréstimo não encontrado.", "error")
            print("Empréstimo não encontrado.", "error")
            return redirect(url_for('bp_loan.view_emprestimos'))

        return render_template("Emprestimo/EmprestimosEdit.html", emprestimo=emprestimo, usuarios=usuarios, livros=livros)
    except Exception as e:
        flash(f"Erro ao editar empréstimo: {e}", "error")
        print(f"Erro ao editar empréstimo: {e}", "error")
        return redirect(url_for('bp_loan.view_emprestimos'))


@emprestimoController.route('/excluir/<int:emprestimo_id>', methods=['GET', 'POST'])
def deletar_emprestimo(emprestimo_id):
    try:
        emprestimo = emprestimosRepository.buscarEmprestimoPorId(emprestimo_id)
        
        response = emprestimosRepository.deletarEmprestimo(emprestimo_id)
        if "Erro" in response:
            flash(response, "error")
        else:
            flash("Empréstimo excluído com sucesso!", "success")

        if emprestimo.data_devolucao_real is not None:
            flash("Este empréstimo já foi devolvido.", "warning")
        else:
            livro_id = emprestimo.livro_id 
            livro_repository.atualizar_quantidade_disponivel(livro_id, aumentar=True)

        return redirect(url_for('bp_loan.view_emprestimos'))
    except Exception as e:
        flash(f"Erro ao excluir empréstimo: {e}", "error")
        return redirect(url_for('bp_loan.view_emprestimos'))


@emprestimoController.route('/usuario/<int:usuario_id>', methods=['GET'])
def listar_por_usuario(usuario_id):
    try:
        emprestimos = emprestimosRepository.listarPorUsuarioJSON(usuario_id)
        return render_template("Emprestimo/emprestimos_por_usuario.html", emprestimos=emprestimos)
    except Exception as e:
        flash(f"Erro ao listar empréstimos por usuário: {e}", "error")
        return render_template("Emprestimo/emprestimos_por_usuario.html", emprestimos=[])


@emprestimoController.route('/livro/<int:livro_id>', methods=['GET'])
def listar_por_livro(livro_id):
    try:
        emprestimos = emprestimosRepository.listarPorLivroJSON(livro_id)
        return render_template("Emprestimo/emprestimos_por_livro.html", emprestimos=emprestimos)
    except Exception as e:
        flash(f"Erro ao listar empréstimos por livro: {e}", "error")
        return render_template("Emprestimo/emprestimos_por_livro.html", emprestimos=[])


@emprestimoController.route('/marcar_devolvido/<int:emprestimo_id>', methods=['GET'])
def marcar_devolvido(emprestimo_id):
    try:
        emprestimo = emprestimosRepository.buscarEmprestimoPorId(emprestimo_id)
        if emprestimo.data_devolucao_real is not None:
            flash("Este empréstimo já foi devolvido.", "warning")
            return redirect(url_for('bp_loan.view_emprestimos'))
        
        # Atualiza a data de devolução real
        data_devolucao_real = datetime.now().replace(second=0, microsecond=0)
        
        
        response = emprestimosRepository.marcarDevolvido(emprestimo_id, data_devolucao_real)

        if "Erro" in response:
            flash(response, "error")
        else:
            flash("Empréstimo marcado como devolvido com sucesso!", "success")


            livro_id = emprestimo.livro_id
            livro_repository.atualizar_quantidade_disponivel(livro_id, aumentar=True)

        return redirect(url_for('bp_loan.view_emprestimos'))
    except Exception as e:
        flash(f"Erro ao marcar devolução: {e}", "error")
        return redirect(url_for('bp_loan.view_emprestimos'))
