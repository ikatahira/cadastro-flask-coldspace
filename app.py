from flask import Flask, render_template, request, redirect, session, send_file
linhas = db.session.query(db.func.date(Acesso.data_hora).label('dia'), db.func.count(Acesso.id)).group_by('dia').all()
dias = [str(r[0]) for r in linhas]
contagens = [r[1] for r in linhas]
return render_template('dashboard.html', total=total, media_idade=round(float(media_idade),2), total_acessos=total_acessos, dias=dias, contagens=contagens)


# ---------- Exportar CSV ----------
@app.route('/exportar/usuarios')
def exportar_usuarios():
usuarios = Usuario.query.all()
si = io.StringIO()
cw = csv.writer(si)
cw.writerow(['id','nome','idade','email','data_criacao'])
for u in usuarios:
cw.writerow([u.id, u.nome, u.idade, u.email or '', u.data_criacao.isoformat()])
output = io.BytesIO()
output.write(si.getvalue().encode('utf-8'))
output.seek(0)
return send_file(output, mimetype='text/csv', download_name='usuarios.csv', as_attachment=True)


# ---------- Autenticação simples (registro rápido) ----------
@app.route('/login', methods=['GET','POST'])
def login():
if request.method == 'POST':
email = request.form.get('email','').strip()
senha = request.form.get('senha','')
u = Usuario.query.filter_by(email=email).first()
if u and u.senha_hash and check_password_hash(u.senha_hash, senha):
session['user_id'] = u.id
a = Acesso(usuario=u, acao='login')
db.session.add(a)
db.session.commit()
log(f'Login: usuario id={u.id}')
return redirect('/')
else:
return render_template('login.html', erro='Credenciais inválidas')
return render_template('login.html')


@app.route('/logout')
def logout():
uid = session.pop('user_id', None)
if uid:
log(f'Logout: usuario id={uid}')
return redirect('/')


# ---------- Peça inicial: criar senha para um usuário (apenas dev) ----------
@app.route('/criar_senha/<int:id>', methods=['GET','POST'])
def criar_senha(id):
u = Usuario.query.get_or_404(id)
if request.method == 'POST':
senha = request.form.get('senha','')
if senha:
u.senha_hash = generate_password_hash(senha)
db.session.commit()
log(f'Senha criada para usuario id={id}')
return redirect('/')
return '''<form method="post"><input name="senha" placeholder="Nova senha"><button type="submit">Criar</button></form>'''


# ---------- Exec ----------
if __name__ == '__main__':
app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)), debug=True)