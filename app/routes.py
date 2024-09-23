import os

from app import create_app
from app.agendamentos.routes import routes as agendamentos_routes
from app.barbeiros.routes import routes as barbeiros_routes
from app.clientes.routes import routes as clientes_routes
from app.produtos.routes import routes as produtos_routes

app = create_app(os.getenv("FLASK_CONFIG"))

clientes_routes(app)
barbeiros_routes(app)
produtos_routes(app)
agendamentos_routes(app)
