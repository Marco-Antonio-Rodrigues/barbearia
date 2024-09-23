import logging
from datetime import datetime

from flask import request

from app import db
from app.agendamentos.models import Agendamento, AgendamentoServico
from app.utils import generate_response


def routes(app):
    @app.route("/agendamentos", methods=["POST"])
    def criar_agendamento():
        data = request.get_json()
        if not data or not "idcliente" in data or not "idbarbeiro" in data:
            logging.error("Dados inválidos ao tentar criar agendamento")
            return generate_response(
                {"error": "Cliente e barbeiro são obrigatórios."}, status=400
            )

        try:
            novo_agendamento = Agendamento(
                idcliente=data["idcliente"],
                idbarbeiro=data["idbarbeiro"],
                idvenda=data.get("idvenda"),
                hora=data.get("hora"),
                data=datetime.strptime(data["data"], "%Y-%m-%d")
                if data.get("data")
                else None,
                status=data.get("status"),
                nota=data.get("nota"),
                descricao=data.get("descricao"),
            )
            db.session.add(novo_agendamento)
            db.session.commit()

            if "servicos" in data:
                for idproduto in data["servicos"]:
                    novo_servico = AgendamentoServico(
                        idagendamento=novo_agendamento.idagendamento,
                        idproduto=idproduto,
                    )
                    db.session.add(novo_servico)

            db.session.commit()
            logging.info(
                f"Agendamento criado com sucesso: {novo_agendamento.idagendamento}"
            )
            return generate_response(
                novo_agendamento.serialize(),
                status=201,
                message="Agendamento criado com sucesso",
            )
        except Exception as e:
            logging.error(f"Erro ao criar agendamento: {e}")
            return generate_response(
                {"error": "Erro ao criar agendamento."}, status=500
            )

    @app.route("/agendamentos", methods=["GET"])
    def listar_agendamentos():
        agendamentos = Agendamento.query.all()
        return generate_response(
            [agendamento.serialize() for agendamento in agendamentos]
        )

    @app.route("/agendamentos/<int:id>", methods=["GET"])
    def obter_agendamento(id):
        agendamento = Agendamento.query.get_or_404(id)
        return generate_response(agendamento.serialize())

    @app.route("/agendamentos/<int:id>", methods=["PATCH"])
    def atualizar_agendamento(id):
        agendamento = Agendamento.query.get_or_404(id)
        data = request.get_json()

        try:
            agendamento.idcliente = data.get("idcliente", agendamento.idcliente)
            agendamento.idbarbeiro = data.get("idbarbeiro", agendamento.idbarbeiro)
            agendamento.idvenda = data.get("idvenda", agendamento.idvenda)
            agendamento.hora = data.get("hora", agendamento.hora)
            agendamento.data = (
                datetime.strptime(data.get("data"), "%Y-%m-%d")
                if data.get("data")
                else agendamento.data
            )
            agendamento.status = data.get("status", agendamento.status)
            agendamento.nota = data.get("nota", agendamento.nota)
            agendamento.descricao = data.get("descricao", agendamento.descricao)

            if "servicos" in data:
                AgendamentoServico.query.filter_by(idagendamento=id).delete()
                for idproduto in data["servicos"]:
                    novo_servico = AgendamentoServico(
                        idagendamento=agendamento.idagendamento, idproduto=idproduto
                    )
                    db.session.add(novo_servico)

            db.session.commit()
            logging.info(
                f"Agendamento atualizado com sucesso: {agendamento.idagendamento}"
            )
            return generate_response(
                agendamento.serialize(),
                status=200,
                message="Agendamento atualizado com sucesso",
            )
        except Exception as e:
            logging.error(f"Erro ao atualizar agendamento: {e}")
            return generate_response(
                {"error": "Erro ao atualizar agendamento."}, status=500
            )

    @app.route("/agendamentos/<int:id>", methods=["DELETE"])
    def excluir_agendamento(id):
        agendamento = Agendamento.query.get_or_404(id)

        try:
            db.session.delete(agendamento)
            db.session.commit()
            logging.info(
                f"Agendamento excluído com sucesso: {agendamento.idagendamento}"
            )
            return generate_response(
                {}, status=200, message="Agendamento excluído com sucesso"
            )
        except Exception as e:
            logging.error(f"Erro ao excluir agendamento: {e}")
            return generate_response(
                {"error": "Erro ao excluir agendamento."}, status=500
            )
