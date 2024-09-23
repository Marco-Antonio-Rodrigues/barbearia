from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Cliente(db.Model):
    __tablename__ = "cliente"
    idcliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomecompletocliente = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(40), nullable=True)
    telefone = db.Column(db.String(15), nullable=True)
    cpf = db.Column(db.String(15), nullable=True)

    agendamentos = relationship("Agendamento", back_populates="cliente")
    vendas = relationship("VendaCliente", back_populates="cliente")

    def serialize(self):
        return {
            "idcliente": self.idcliente,
            "nomecompletocliente": self.nomecompletocliente,
            "senha": self.senha,
            "email": self.email,
            "telefone": self.telefone,
            "cpf": self.cpf,
        }

class Venda(db.Model):
    __tablename__ = "venda"
    idvenda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    datavenda = db.Column(db.Date, nullable=True)
    formapag = db.Column(db.String(20), nullable=True)

    clientes = relationship("VendaCliente", back_populates="venda")
    mercadorias = relationship("VendaMercadoria", back_populates="venda")
    agendamentos = relationship("Agendamento", back_populates="venda")


class VendaCliente(db.Model):
    __tablename__ = "vendacliente"
    idvenda = db.Column(db.Integer, ForeignKey("venda.idvenda"), primary_key=True)
    idcliente = db.Column(db.Integer, ForeignKey("cliente.idcliente"), primary_key=True)

    venda = relationship("Venda", back_populates="clientes")
    cliente = relationship("Cliente", back_populates="vendas")


class VendaMercadoria(db.Model):
    __tablename__ = "vendamercadoria"
    idproduto = db.Column(db.Integer, ForeignKey("produto.idproduto"), primary_key=True)
    idvenda = db.Column(db.Integer, ForeignKey("venda.idvenda"), primary_key=True)

    produto = relationship("Produto", back_populates="vendamercadorias")
    venda = relationship("Venda", back_populates="mercadorias")


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


class AgendamentoServico(db.Model):
    __tablename__ = "agendamentoservico"
    idagendamento = db.Column(
        db.Integer, ForeignKey("agendamento.idagendamento"), primary_key=True
    )
    idproduto = db.Column(db.Integer, ForeignKey("produto.idproduto"), primary_key=True)

    agendamento = relationship("Agendamento", back_populates="servicos")
    produto = relationship("Produto", back_populates="agendamentoservicos")


class Categoria(db.Model):
    __tablename__ = "categoria"
    idproduto = db.Column(db.Integer, ForeignKey("produto.idproduto"), primary_key=True)
    nomecategoria = db.Column(db.String(30), nullable=False)

    produto = relationship("Produto", back_populates="categorias")


class Cupom(db.Model):
    __tablename__ = "cupom"
    idcupom = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.Text, nullable=True)
    desconto = db.Column(db.Numeric(5, 2), nullable=True)
    datainicio = db.Column(db.Date, nullable=True)
    datatermino = db.Column(db.Date, nullable=True)

    descontos = relationship("Desconto", back_populates="cupom")


class Desconto(db.Model):
    __tablename__ = "desconto"
    idcupom = db.Column(db.Integer, ForeignKey("cupom.idcupom"), primary_key=True)
    idproduto = db.Column(db.Integer, ForeignKey("produto.idproduto"), primary_key=True)

    cupom = relationship("Cupom", back_populates="descontos")
    produto = relationship("Produto", back_populates="descontos")


class Realiza(db.Model):
    __tablename__ = "realiza"
    idbarbeiro = db.Column(
        db.Integer, ForeignKey("barbeiro.idbarbeiro"), primary_key=True
    )
    idproduto = db.Column(db.Integer, ForeignKey("produto.idproduto"), primary_key=True)

    barbeiro = relationship("Barbeiro", back_populates="realizacoes")
    produto = relationship("Produto", back_populates="realizacoes")
