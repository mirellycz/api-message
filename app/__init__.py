from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config



db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__) # inicializa instancia do flask
    app.config.from_object(Config)  # aplica as configurações
    app.json.sort_keys = False # Desativa ordenação alfabética das chaves JSON

    db.init_app(app)  # associa o SQLAlchemy à aplicação Flask

    migrate.init_app(app, db)

    from app.models.message import Message
    from app.routes.messages import messages_bp

    app.register_blueprint(messages_bp, url_prefix="/messages")

    @app.route("/test")
    def test():
        return {"status": "ok"}
        
    return app