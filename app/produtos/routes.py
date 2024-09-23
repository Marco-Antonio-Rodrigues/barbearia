import logging
from datetime import datetime

from flask import request

from app import db
from app.produtos.models import Produto
from app.utils import generate_response


def routes(app):
    @app.route("/produtos", methods=["POST"])
    def criar_produto():
        data = request.get_json()
        if not data or not "nomeproduto" in data or not "preco" in data:
            logging.error("Dados inválidos ao tentar criar produto")
            return generate_response(
                {"error": "Nome do produto e preço são obrigatórios."}, status=400
            )

        try:
            novo_produto = Produto(
                nomeproduto=data["nomeproduto"],
                preco=data["preco"],
                quantidade=data.get("quantidade"),
                tipo=data.get("tipo"),
                validade=datetime.strptime(data.get("validade"), "%Y-%m-%d")
                if data.get("validade")
                else None,
                descricao=data.get("descricao"),
            )
            db.session.add(novo_produto)
            db.session.commit()
            logging.info(f"Produto criado com sucesso: {novo_produto.nomeproduto}")
            return generate_response(
                novo_produto.serialize(),
                status=201,
                message="Produto criado com sucesso",
            )
        except Exception as e:
            logging.error(f"Erro ao criar produto: {e}")
            return generate_response({"error": "Erro ao criar produto."}, status=500)

    @app.route("/produtos", methods=["GET"])
    def listar_produtos():
        produtos = Produto.query.all()
        return generate_response([produto.serialize() for produto in produtos])

    @app.route("/produtos/<int:id>", methods=["GET"])
    def obter_produto(id):
        produto = Produto.query.get_or_404(id)
        return generate_response(produto.serialize())

    # UPDATE - Atualizar um produto existente
    @app.route("/produtos/<int:id>", methods=["PUT"])
    def atualizar_produto(id):
        produto = Produto.query.get_or_404(id)
        data = request.get_json()

        try:
            produto.nomeproduto = data.get("nomeproduto", produto.nomeproduto)
            produto.preco = data.get("preco", produto.preco)
            produto.quantidade = data.get("quantidade", produto.quantidade)
            produto.tipo = data.get("tipo", produto.tipo)
            produto.validade = (
                datetime.strptime(data.get("validade"), "%Y-%m-%d")
                if data.get("validade")
                else produto.validade
            )
            produto.descricao = data.get("descricao", produto.descricao)

            db.session.commit()
            logging.info(f"Produto atualizado com sucesso: {produto.nomeproduto}")
            return generate_response(
                produto.serialize(),
                status=200,
                message="Produto atualizado com sucesso",
            )
        except Exception as e:
            logging.error(f"Erro ao atualizar produto: {e}")
            return generate_response(
                {"error": "Erro ao atualizar produto."}, status=500
            )

    @app.route("/produtos/<int:id>", methods=["DELETE"])
    def excluir_produto(id):
        produto = Produto.query.get_or_404(id)

        try:
            db.session.delete(produto)
            db.session.commit()
            logging.info(f"Produto excluído com sucesso: {produto.nomeproduto}")
            return generate_response(
                {}, status=200, message="Produto excluído com sucesso"
            )
        except Exception as e:
            logging.error(f"Erro ao excluir produto: {e}")
            return generate_response({"error": "Erro ao excluir produto."}, status=500)
