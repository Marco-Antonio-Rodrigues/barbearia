from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Barbeiro(db.Model):
    __tablename__ = "barbeiro"
    idbarbeiro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomecompletobarbeiro = db.Column(db.String(30), nullable=False)
    instagram = db.Column(db.String(30), nullable=True)
    telefone = db.Column(db.String(15), nullable=True)

    agendamentos = relationship("Agendamento", back_populates="barbeiro")
    realizacoes = relationship("Realiza", back_populates="barbeiro")

    def serialize(self):
        return {
            "idbarbeiro": self.idbarbeiro,
            "nomecompletobarbeiro": self.nomecompletobarbeiro,
            "instagram": self.instagram,
            "telefone": self.telefone,
        }
