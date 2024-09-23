from flask import request

from app import db
from app.clientes.models import Cliente
from app.utils import generate_response


def routes(app):
    @app.route("/clientes", methods=["POST"])
    def criar_cliente():
        data = request.get_json()
        if not data or not "nomecompletocliente" in data or not "senha" in data:
            return generate_response({}, 400, "Nome completo e senha são obrigatórios.")

        novo_cliente = Cliente(
            nomecompletocliente=data["nomecompletocliente"],
            senha=data["senha"],
            email=data.get("email"),
            telefone=data.get("telefone"),
            cpf=data.get("cpf"),
        )
        db.session.add(novo_cliente)
        db.session.commit()
        return generate_response(novo_cliente.serialize(), 201)

    @app.route("/clientes", methods=["GET"])
    def listar_clientes():
        clientes = Cliente.query.all()
        clientes_json = [cliente.serialize() for cliente in clientes]
        return generate_response(clientes_json)

    @app.route("/clientes/<int:id>", methods=["GET"])
    def obter_cliente(id):
        cliente = Cliente.query.get_or_404(id)
        return generate_response(cliente.serialize())

    @app.route("/clientes/<int:id>", methods=["PATCH"])
    def atualizar_cliente(id):
        cliente = Cliente.query.get_or_404(id)
        data = request.get_json()

        cliente.nomecompletocliente = data.get(
            "nomecompletocliente", cliente.nomecompletocliente
        )
        cliente.senha = data.get("senha", cliente.senha)
        cliente.email = data.get("email", cliente.email)
        cliente.telefone = data.get("telefone", cliente.telefone)
        cliente.cpf = data.get("cpf", cliente.cpf)

        db.session.commit()

        return generate_response(cliente.serialize())

    @app.route("/clientes/<int:id>", methods=["DELETE"])
    def excluir_cliente(id):
        cliente = Cliente.query.get_or_404(id)
        db.session.delete(cliente)
        db.session.commit()

        return generate_response({"message": "Cliente excluído com sucesso"})
