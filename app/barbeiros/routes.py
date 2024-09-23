import logging

from flask import request

from app import db
from app.barbeiros.models import Barbeiro
from app.utils import generate_response


def routes(app):
    @app.route("/", methods=["GET"])
    def get_subscribers():
        return generate_response({"message": "Hello, world!"})

    @app.route("/barbeiros", methods=["POST"])
    def create_barbeiro():
        data = request.get_json()

        try:
            nome = data.get("nomecompletobarbeiro")
            instagram = data.get("instagram")
            telefone = data.get("telefone")

            novo_barbeiro = Barbeiro(
                nomecompletobarbeiro=nome, instagram=instagram, telefone=telefone
            )

            db.session.add(novo_barbeiro)
            db.session.commit()

            return generate_response(
                novo_barbeiro.serialize(), 201, "Criado com sucesso"
            )

        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao criar barbeiro: {e}")
            return generate_response({}, 400, f"Erro: {e}")

    @app.route("/barbeiros", methods=["GET"])
    def get_barbeiros():
        try:
            barbeiros = Barbeiro.query.all()
            barbeiros_json = [barbeiro.serialize() for barbeiro in barbeiros]

            return generate_response(barbeiros_json, 200, "ok")

        except Exception as e:
            logging.error(f"Erro ao buscar barbeiros: {e}")
            return generate_response({}, 400, f"Erro: {e}")

    @app.route("/barbeiros/<int:id>", methods=["GET"])
    def get_barbeiro(id):
        try:
            barbeiro = Barbeiro.query.get(id)
            if not barbeiro:
                return generate_response({}, 404, "Barbeiro não encontrado")

            return generate_response(barbeiro.serialize(), 200, "ok")

        except Exception as e:
            logging.error(f"Erro ao buscar barbeiro: {e}")
            return generate_response({}, 400, f"Erro: {e}")

    @app.route("/barbeiros/<int:id>", methods=["PATCH"])
    def update_barbeiro(id):
        data = request.get_json()

        try:
            barbeiro = Barbeiro.query.get(id)
            if not barbeiro:
                return generate_response({}, 404, "Barbeiro não encontrado")

            barbeiro.nomecompletobarbeiro = data.get(
                "nomecompletobarbeiro", barbeiro.nomecompletobarbeiro
            )
            barbeiro.instagram = data.get("instagram", barbeiro.instagram)
            barbeiro.telefone = data.get("telefone", barbeiro.telefone)

            db.session.commit()

            return generate_response(
                barbeiro.serialize(), 200, "Atualizado com sucesso"
            )

        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao atualizar barbeiro: {e}")
            return generate_response({}, 400, f"Erro: {e}")

    @app.route("/barbeiros/<int:id>", methods=["DELETE"])
    def delete_barbeiro(id):
        try:
            barbeiro = Barbeiro.query.get(id)
            if not barbeiro:
                return generate_response({}, 404, "Barbeiro não encontrado")

            db.session.delete(barbeiro)
            db.session.commit()

            return generate_response({}, 200, "Deletado com sucesso")

        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao deletar barbeiro: {e}")
            return generate_response({}, 400, f"Erro: {e}")
