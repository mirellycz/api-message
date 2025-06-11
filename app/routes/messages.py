from flask import Blueprint, request, jsonify, abort
from app.models.message import Message
from .. import db
from app.models.message import Message
from app.schemas.schema import MessageSchema


messages_bp = Blueprint('messages', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

# Rota para listar todas as mensagens

@messages_bp.route('/', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([msg.to_dict() for msg in messages]), 200

# Rota para obter uma mensagem por id
@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get_or_404(message_id)
    return jsonify(message.to_dict()), 200

# Rota para criar uma nova mensagem
@messages_bp.route("/", methods=["POST"])
def create_message():
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Campo 'content' é obrigatório"}), 400

    nova_msg = Message(content=content)  
    db.session.add(nova_msg)
    db.session.commit()

    return jsonify(nova_msg.to_dict()), 201
# Rota para atualizar uma mensagem existente
@messages_bp.route('/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    data = request.get_json()
    if not data or 'content' not in data:
        abort(400, description="Campo 'content' é obrigatório.")
    
    message.content = data['content']
    db.session.commit()
    
    return jsonify(message.to_dict()), 200

# Rota para deletar uma mensagem
@messages_bp.route("/<int:id>", methods=["DELETE"])
def delete_message(id):
    mensagem = Message.query.get_or_404(id)
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify({"message": "Mensagem deletada com sucesso"}), 200
    
    
