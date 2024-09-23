from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Agendamento(db.Model):
    __tablename__ = "agendamento"
    idagendamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idcliente = db.Column(db.Integer, ForeignKey("cliente.idcliente"))
    idbarbeiro = db.Column(db.Integer, ForeignKey("barbeiro.idbarbeiro"))
    idvenda = db.Column(db.Integer, ForeignKey("venda.idvenda"))
    hora = db.Column(db.Time, nullable=True)
    data = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(10), nullable=True)
    nota = db.Column(db.Integer, nullable=True)
    descricao = db.Column(db.Text, nullable=True)

    cliente = relationship("Cliente", back_populates="agendamentos")
    barbeiro = relationship("Barbeiro", back_populates="agendamentos")
    venda = relationship("Venda", back_populates="agendamentos")
    servicos = relationship("AgendamentoServico", back_populates="agendamento")

    def serialize(self):
        return {
            "idagendamento": self.idagendamento,
            "idcliente": self.idcliente,
            "idbarbeiro": self.idbarbeiro,
            "idvenda": self.idvenda,
            "hora": str(self.hora) if self.hora else None,
            "data": self.data.strftime("%Y-%m-%d") if self.data else None,
            "status": self.status,
            "nota": self.nota,
            "descricao": self.descricao,
            "cliente": self.cliente.nomecompletocliente if self.cliente else None,
            "barbeiro": self.barbeiro.nomecompletobarbeiro if self.barbeiro else None,
            "servicos": [servico.serialize() for servico in self.servicos],
        }


class AgendamentoServico(db.Model):
    __tablename__ = "agendamentoservico"
    idagendamento = db.Column(
        db.Integer, ForeignKey("agendamento.idagendamento"), primary_key=True
    )
    idproduto = db.Column(db.Integer, ForeignKey("produto.idproduto"), primary_key=True)

    agendamento = relationship("Agendamento", back_populates="servicos")
    produto = relationship("Produto", back_populates="agendamentoservicos")

    def serialize(self):
        return {
            "idproduto": self.idproduto,
            "idagendamento": self.idagendamento,
            "produto": self.produto.nomeproduto if self.produto else None,
        }
