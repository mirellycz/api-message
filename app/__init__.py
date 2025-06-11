from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException



db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__) # inicializa instancia do flask
    app.config.from_object(Config)  # aplica as configurações
    app.json.sort_keys = False # Desativa ordenação alfabética das chaves JSON

    db.init_app(app)  # associa o SQLAlchemy à aplicação Flask

    migrate.init_app(app, db)

    from app.models.message import Message
    from app.routes.messages import messages_bp

    app.register_blueprint(messages_bp, url_prefix="/messages")


    # Tratadores globais de erro (explicados na seção 5.6)
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    @app.route("/test")
    def test():
        return {"status": "ok"}
        
    return app

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "Validation Error",
            "messages": error.messages
        }), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            "error": error.name,
            "message": error.description
        }), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": str(error)
        }), 500

__all__ = ['db', 'ma']