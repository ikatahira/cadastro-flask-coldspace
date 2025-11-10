from flask import Flask, render_template, request, redirect, session, send_file
from models import db, Usuario, Endereco, Acesso, DispositivoIoT, LogSistema
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import io
import csv
import pandas as pd


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'dev_secret_key')


db.init_app(app)


with app.app_context():
db.create_all()


# ---------- Helpers ----------
def log(descricao, nivel='INFO'):
l = LogSistema(descricao=descricao, nivel=nivel)
db.session.add(l)
db.session.commit()


# ---------- Rotas públicas ----------
@app.route('/')
def home():
usuarios = Usuario.query.all()
return render_template('index.html', usuarios=usuarios)


@app.route('/adicionar', methods=['POST'])
def adicionar():
nome = request.form.get('nome','').strip()
idade = request.form.get('idade','').strip()
email = request.form.get('email','').strip() or None
try:
idade = int(idade)
except ValueError:
idade = None


if nome and isinstance(idade, int) and idade >= 0:
novo = Usuario(nome=nome, idade=idade, email=email)
db.session.add(novo)
db.session.commit()
log(f'Usuário criado: {novo.nome} (id={novo.id})')
return redirect('/')


@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
usuario = Usuario.query.get_or_404(id)
if request.method == 'POST':
nome = request.form.get('nome','').strip()
idade = request.form.get('idade','').strip()
try:
idade = int(idade)
except ValueError:
idade = None
app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)), debug=True)