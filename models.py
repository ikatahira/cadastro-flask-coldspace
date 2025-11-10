from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    senha_hash = db.Column(db.String(200), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)


class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    cep = db.Column(db.String(20))
    usuario = db.relationship('Usuario', backref='enderecos')


class Acesso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    acao = db.Column(db.String(100))
    usuario = db.relationship('Usuario', backref='acessos')


class DispositivoIoT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    status = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    usuario = db.relationship('Usuario', backref='dispositivos')


class LogSistema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text)
    nivel = db.Column(db.String(20))
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)


