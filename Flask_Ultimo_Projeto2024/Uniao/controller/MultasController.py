from flask import Blueprint, request, redirect, url_for, render_template, flash
from repository import MultasRepository, EmprestimosRepository, LogRepository

multasController = Blueprint('bp_multas', __name__)
multasRepository=MultasRepository()

@multasController.route('/listar', methods=['GET'])
def listar_multas():
    try:
        usuario_id = request.args.get('usuario_id')
        if usuario_id:
            multas = multasRepository.obter_multas_por_usuario(usuario_id)
        else:
            multas = multasRepository.obter_todas_multas()

        return render_template("Multas/multas.html", multas=multas)
    except Exception as e:
        flash(f"Erro ao carregar as multas: {e}", "error")
        return render_template("Multas/multas.html", multas=[])

@multasController.route('/gerar_multa/<int:emprestimo_id>', methods=['GET', 'POST'])
def gerar_multa(emprestimo_id):
    try:

        emprestimo = EmprestimosRepository().buscarEmprestimoPorId(emprestimo_id)
        if not emprestimo:
            flash("Empréstimo não encontrado.", "error")
            return redirect(url_for('bp_loan.view_emprestimos'))

        if request.method == 'GET':
            valor_multa, atraso = multasRepository.calcular_multa(emprestimo.id)
            if atraso == 0:
                flash("Não é possível gerar a multa, o empréstimo não está atrasado.", "info")
                return redirect(url_for('bp_loan.view_emprestimos'))
            return render_template('Multas/ConfirmarMulta.html', emprestimo=emprestimo, valor_multa=valor_multa, atraso=atraso)

        if request.method == 'POST':
            if emprestimo.data_devolucao_real:
                valor_multa, _ = multasRepository.calcular_multa(emprestimo_id)
                if valor_multa > 0:
                    multasRepository.gerar_multa(emprestimo.usuario_id, valor_multa, emprestimo_id) 
                    flash(f"Multa de R${valor_multa} gerada para o usuário {emprestimo.usuario_id}.", "success")
                else:
                    flash("O empréstimo foi devolvido dentro do prazo, não há multa a ser gerada.", "info")
            else:
                flash("A devolução ainda não foi realizada, não é possível gerar multa.", "warning")

            return redirect(url_for('bp_loan.view_emprestimos'))

    except Exception as e:
        flash(f"Erro ao gerar a multa: {e}", "error")
        return redirect(url_for('bp_loan.view_emprestimos'))



@multasController.route('/pagar/<int:multa_id>', methods=['GET', 'POST'])
def pagar_multa(multa_id):
    try:
        multa = multasRepository.obter_multa_por_id(multa_id)
        if not multa:
            flash("Multa não encontrada.", "error")
            print("Multa não encontrada.", "error")
            return redirect(url_for('bp_multas.listar_multas'))

        if request.method == 'GET':
            return render_template('Multas/ConfirmarPagamento.html', multa=multa)

        if multasRepository.marcar_como_pago(multa_id):
            flash(f"Multa de ID {multa_id} paga com sucesso!", "success")
        else:
            flash("Erro ao pagar a multa.", "error")
            print(("Erro ao pagar a multa.", "error"))
        return redirect(url_for('bp_multas.listar_multas'))

    except Exception as e:
        flash(f"Erro ao pagar a multa: {e}", "error")
        print(f"Erro ao pagar a multa: {e}", "error")
        return redirect(url_for('bp_multas.listar_multas'))


@multasController.route('/excluir/<int:multa_id>', methods=['GET', 'POST'])
def excluir_multa(multa_id):
    try:
        if multasRepository.deletar_multa(multa_id):
            flash("Multa excluída com sucesso!", "success")
        else:
            flash("Erro ao excluir a multa.", "error")
        return redirect(url_for('bp_multas.listar_multas'))
    except Exception as e:
        flash(f"Erro ao excluir multa: {e}", "error")
        return redirect(url_for('bp_multas.listar_multas'))
