from datetime import datetime
from database import database
from model import Multas

class MultasDAO:
    def obter_todas_multas(self):
        return database.session.query(Multas).all()
    @staticmethod
    def gerar_multa(usuario_id, valor_multa, emprestimo_id):
        multa = Multas(usuario_id=usuario_id, valor=valor_multa, data_geracao=datetime.now(), status="pendente", emprestimo_id=emprestimo_id)
        database.session.add(multa)
        database.session.commit()
    @staticmethod
    def marcar_como_pago(multa_id):
        multa = database.session.query(Multas).filter(Multas.id == multa_id).first()
        if multa:
            multa.status = "paga"
            database.session.commit()
            return True
        return False
    @staticmethod
    def deletar_multa(multa_id):
        multa = database.session.query(Multas).filter(Multas.id == multa_id).first()
        if multa:
            database.session.delete(multa)
            database.session.commit()
            return True
        return False
    @staticmethod
    def obter_multa_por_id(multa_id):
        try:
            multa = Multas.query.get(multa_id)
            if multa:
                return multa
            else:
                print(f"Multa com ID {multa_id} não encontrado.")
                return None
        except Exception as e:
            print(f"Erro ao buscar a multa com ID {multa_id}: {e}")
            return None