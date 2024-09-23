from sqlalchemy.orm import relationship

from app import db


class Produto(db.Model):
    __tablename__ = "produto"
    idproduto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeproduto = db.Column(db.String(50), nullable=False)
    preco = db.Column(
        db.Numeric(10, 2), nullable=False
    )  # precisão de 10 números com 2 após a virgula
    quantidade = db.Column(db.Integer, nullable=True)
    tipo = db.Column(db.String(50), nullable=True)
    validade = db.Column(db.Date, nullable=True)
    descricao = db.Column(db.Text, nullable=True)

    categorias = relationship("Categoria", back_populates="produto")
    descontos = relationship("Desconto", back_populates="produto")
    realizacoes = relationship("Realiza", back_populates="produto")
    agendamentoservicos = relationship("AgendamentoServico", back_populates="produto")
    vendamercadorias = relationship("VendaMercadoria", back_populates="produto")

    def serialize(self):
        return {
            "idproduto": self.idproduto,
            "nomeproduto": self.nomeproduto,
            "preco": str(self.preco),
            "quantidade": self.quantidade,
            "tipo": self.tipo,
            "validade": self.validade.strftime("%Y-%m-%d") if self.validade else None,
            "descricao": self.descricao,
        }
