from DAO import MultasDAO
from repository import EmprestimosRepository  # Agora estamos importando o EmprestimosRepository
from datetime import datetime

class MultasRepository:
    def __init__(self):
        self.dao = MultasDAO()
        self.emprestimosRepository = EmprestimosRepository()  # Instanciando EmprestimosRepository

    def obter_todas_multas(self):
        return self.dao.obter_todas_multas()

    def gerar_multa(self, usuario_id, valor_multa, emprestimo_id):
        self.dao.gerar_multa(usuario_id, valor_multa, emprestimo_id)

    def marcar_como_pago(self, multa_id):
        return self.dao.marcar_como_pago(multa_id)

    def deletar_multa(self, multa_id):
        return self.dao.deletar_multa(multa_id)

    def calcular_multa(self, emprestimo_id):
        emprestimo = self.emprestimosRepository.buscarEmprestimoPorId(emprestimo_id)  # Busca o empréstimo
        if emprestimo:  # Verifica se o empréstimo foi encontrado
            print("Empréstimo encontrado")
            print(emprestimo.data_devolucao_real)
            print(emprestimo.id)
            
            # Se não houver data de devolução real, usa a data atual
            data_devolucao_real = emprestimo.data_devolucao_real if emprestimo.data_devolucao_real else datetime.now()
            
            # Verifica se a data de devolução real é maior que a prevista
            if data_devolucao_real > emprestimo.data_devolucao_prevista:
                dias_atraso = (data_devolucao_real - emprestimo.data_devolucao_prevista).days
                valor_multa = (dias_atraso // 5) * 10  # Multa de 10 por cada 5 dias de atraso
                print(f"Valor da multa: {valor_multa}, Dias de atraso: {dias_atraso}")
                return valor_multa, dias_atraso
            else:
                # Caso não haja atraso
                mensagem = "O empréstimo não está atrasado."
                print(mensagem)
                return 0, 0, mensagem  # Retorna também a mensagem
        return 0, 0, "Erro: Empréstimo não encontrado"  # Mensagem de erro caso o empréstimo não seja encontrado
    
    def obter_multa_por_id(self, multa_id):
        try:
            multa = self.dao.obter_multa_por_id(multa_id)
            if multa:
                
                return multa
            return None
        except Exception as e:
            print(f"Erro ao obter multa por ID: {e}")
            return None

    def antiXSS(self, valor):
        try:
            caracteres_perigosos = ["<", ">", "&", "'", '"', "/", "script", "onerror", "onload","select","return","print","delete"]

            for char in caracteres_perigosos:
                if char in valor.lower():
                    return True
            return False
        except Exception as e:
            print(f"Erro ao verificar valor contra XSS: {e}")
            return None