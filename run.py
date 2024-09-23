import os

from waitress import serve

from app.routes import app

if os.getenv("FLASK_CONFIG") == "prod":
    serve(app, host="127.0.0.1", port=8000)
else:
    app.run(host="127.0.0.1", port=8000)
