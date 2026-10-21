from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select

from database import engine, Base, session
from models import Usuario, Livro

app = Flask(__name__)

Base.metadata.create_all(engine)

@app.route("/", methods=["POST","GET"])
def index():
    return render_template('index.html')

@app.route("/usuario/novo", methods=["POST","GET"])
def new_user():
    if request.method == "POST":
        nome = request.form.get("nome", None)
        email = request.form.get("email", None)

        if nome and email:
            usuario = session.scalars(select(Usuario).where(Usuario.email == email)).first

            if usuario:
                usuario_novo = Usuario(nome=nome, email=email)
                session.add(usuario_novo)
                session.commit()
                return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route("/livros/novo", methods=["POST","GET"])
def new_book():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        Usuario_id = request.form.get("Usuario_id")

        if titulo and Usuario_id:
            livro = session.scalars(select(Livro).where(Livro.titulo == titulo)).first()

            if not livro:
                livro_novo = Livro(titulo=titulo, Usuario_id=int(Usuario_id))
                session.add(livro_novo)
                session.commit()
                return redirect(url_for("listar_livro"))

    return render_template("Livro_form.html")

@app.route("/livros/listar")
def listar_livro():
    livros = session.scalars(select(Livro).order_by(Livro.titulo)).all()
    return render_template("index.html", livros=livros)


@app.route("/usuarios/listar")
def listar_usuarios():
    usuarios = session.scalars(select(Usuario).order_by(Usuario.nome)).all()
    return render_template("index.html", usuarios=usuarios)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        if email and senha:
            usuario = session.scalars(select(Usuario).where(Usuario.email == email)).first()
            if usuario:
                if usuario.senha == senha:
                    return redirect(url_for("index"))
                else:
                    return redirect(url_for("new_user"))

    return render_template("login.html")