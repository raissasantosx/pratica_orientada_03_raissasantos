from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select

from database import session, engine, Base
from models import Usuario, Livro

app = Flask(__name__)

Base.metadata.create_all(engine)

@app.route("/")
def index():
    usuarios = session.scalars(select(Usuario)).all()
    livros = session.scalars(select(Livro)).all()
    return 

@app.route("/usuario/novo", methods=["POST","GET"])
def new_user():
    if request.method == "POST":
        nome = request.form.get("nome", None)
        email = request.form.get("email", None)

        if nome and email:
            session = SessionLocal()
            usuario = session.scalars(select(Usuario).where(Usuario.email==email))

            if not usuario:
                usuario_novo = Usuario(nome=nome, email=email)
                session.add(usuario_novo)
                session.commit()

            else:
                return redirect(url_for('login'))

@app.route("/livros/novo", methods=["POST","GET"])
def new_livro():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        Usuario_id = request.form.get("Usuario_id")

        if titulo and Usuario_id:
            session = SessionLocal()
            livro = session.scalars(select(Livro).where(Livro.titulo == titulo)).first()

            if not livro:
                livro_novo = Livro(titulo=titulo, Usuario_id=int(Usuario_id))
                session.add(livro_novo)
                session.commit()
                return redirect(url_for("listar_livro"))

    return render_template("Livro_form.html")

@app.route("/livros/listar")
def listar_livro():
    session = SessionLocal()
    livros = session.scalars(select(Livro).order_by(Livro.titulo)).all()
    return render_template("index.html", livros=livros)


@app.route("/usuarios/listar")
def listar_usuarios():
    session = SessionLocal()
    usuarios = session.scalars(select(Usuario).order_by(Usuario.nome)).all()
    return render_template("index.html", usuarios=usuarios)


