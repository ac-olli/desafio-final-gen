from datetime import datetime
from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True, info={'constraint_name': 'user_email_email_check'})
    foto = db.Column(db.String(200))
    postagens = db.relationship('Postagem', backref='usuario')

class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    texto = db.Column(db.String(50), nullable=False)
    data = db.Column(db.DateTime())
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tema_id = db.Column(db.Integer, db.ForeignKey('tema.id'))

class Tema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    postagens = db.relationship('Postagem', backref='tema')