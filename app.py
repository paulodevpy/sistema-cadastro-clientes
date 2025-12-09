from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# diretório base onde está este arquivo app.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "troque-essa-chave"

# caminho ABSOLUTO para o banco dentro da pasta instance
DB_PATH = os.path.join(BASE_DIR, "instance", "app.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(50))
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Customer {self.nome}>"

# usuario fixo apenas para demonstracao
USERNAME = "admin"
PASSWORD = "admin123"


def login_required(view):
    from functools import wraps

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("list_customers"))
        else:
            flash("Usuário ou senha inválidos.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    return redirect(url_for("list_customers"))


@app.route("/clientes")
@login_required
def list_customers():
    search = request.args.get("q", "").strip()
    query = Customer.query

    if search:
        like_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Customer.nome.ilike(like_term),
                Customer.email.ilike(like_term),
                Customer.telefone.ilike(like_term),
            )
        )

    customers = query.order_by(Customer.criado_em.desc()).all()
    return render_template("customers.html", customers=customers, search=search)


@app.route("/clientes/novo", methods=["GET", "POST"])
@login_required
def create_customer():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        if not nome:
            flash("O campo nome é obrigatório.", "danger")
            return redirect(url_for("create_customer"))

        customer = Customer(
            nome=nome,
            email=email or None,
            telefone=telefone or None,
            observacoes=observacoes or None,
        )
        db.session.add(customer)
        db.session.commit()
        flash("Cliente cadastrado com sucesso!", "success")
        return redirect(url_for("list_customers"))

    return render_template("customer_form.html", customer=None)


@app.route("/clientes/<int:customer_id>/editar", methods=["GET", "POST"])
@login_required
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == "POST":
        customer.nome = request.form.get("nome", "").strip()
        customer.email = request.form.get("email", "").strip() or None
        customer.telefone = request.form.get("telefone", "").strip() or None
        customer.observacoes = request.form.get("observacoes", "").strip() or None

        if not customer.nome:
            flash("O campo nome é obrigatório.", "danger")
            return redirect(url_for("edit_customer", customer_id=customer.id))

        db.session.commit()
        flash("Cliente atualizado com sucesso!", "success")
        return redirect(url_for("list_customers"))

    return render_template("customer_form.html", customer=customer)


@app.route("/clientes/<int:customer_id>/excluir", methods=["POST"])
@login_required
def delete_customer(customer_id):
    ...
    return redirect(url_for("list_customers"))


# garante que as tabelas existam antes de iniciar o servidor
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
