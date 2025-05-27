from datetime import datetime
from app import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self): #trasnforma em dicionario p facilitar conversão p JSON
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }