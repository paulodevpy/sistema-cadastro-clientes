from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
    send_file,
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
from sqlalchemy import or_
from collections import defaultdict
from openpyxl import Workbook
import io
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "troque-essa-chave"

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

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "observacoes": self.observacoes,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }


# usuarios fixos apenas para demonstracao de niveis
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "viewer"},
}


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


def role_required(role):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if not session.get("logged_in"):
                return redirect(url_for("login"))
            if session.get("role") != role:
                flash("Voce nao tem permissao para esta acao", "danger")
                return redirect(url_for("list_customers"))
            return view(*args, **kwargs)

        return wrapped_view

    return decorator


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = USERS.get(username)
        if user and user["password"] == password:
            session["logged_in"] = True
            session["username"] = username
            session["role"] = user["role"]
            flash("Login realizado com sucesso", "success")
            return redirect(url_for("list_customers"))

        flash("Usuario ou senha invalidos", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Voce saiu do sistema", "info")
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
            or_(
                Customer.nome.ilike(like_term),
                Customer.email.ilike(like_term),
                Customer.telefone.ilike(like_term),
            )
        )

    customers = query.order_by(Customer.criado_em.desc()).all()

    all_customers = Customer.query.all()
    total_clientes = len(all_customers)
    clientes_com_email = len([c for c in all_customers if c.email])
    clientes_com_telefone = len([c for c in all_customers if c.telefone])

    # dados para grafico (clientes por mes)
    meses = defaultdict(int)
    for c in all_customers:
        if c.criado_em:
            key = (c.criado_em.year, c.criado_em.month)
            meses[key] += 1

    meses_ordenados = sorted(meses.keys())
    chart_labels = [f"{mes:02d}/{ano}" for (ano, mes) in meses_ordenados]
    chart_values = [meses[key] for key in meses_ordenados]

    return render_template(
        "customers.html",
        customers=customers,
        search=search,
        total_clientes=total_clientes,
        clientes_com_email=clientes_com_email,
        clientes_com_telefone=clientes_com_telefone,
        chart_labels=chart_labels,
        chart_values=chart_values,
    )


@app.route("/clientes/novo", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_customer():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        if not nome:
            flash("O campo nome e obrigatorio", "danger")
            return render_template("customer_form.html", customer=None)

        customer = Customer(
            nome=nome,
            email=email,
            telefone=telefone,
            observacoes=observacoes,
        )

        db.session.add(customer)
        db.session.commit()

        flash("Cliente cadastrado com sucesso", "success")
        return redirect(url_for("list_customers"))

    return render_template("customer_form.html", customer=None)


@app.route("/clientes/<int:customer_id>/editar", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == "POST":
        customer.nome = request.form.get("nome", "").strip()
        customer.email = request.form.get("email", "").strip()
        customer.telefone = request.form.get("telefone", "").strip()
        customer.observacoes = request.form.get("observacoes", "").strip()

        if not customer.nome:
            flash("O campo nome e obrigatorio", "danger")
            return render_template("customer_form.html", customer=customer)

        db.session.commit()
        flash("Cliente atualizado com sucesso", "success")
        return redirect(url_for("list_customers"))

    return render_template("customer_form.html", customer=customer)


@app.route("/clientes/<int:customer_id>/excluir", methods=["POST"])
@login_required
@role_required("admin")
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash("Cliente excluido com sucesso", "info")
    return redirect(url_for("list_customers"))


@app.route("/clientes/exportar")
@login_required
@role_required("admin")
def export_customers():
    customers = Customer.query.order_by(Customer.criado_em.asc()).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Clientes"

    ws.append(["ID", "Nome", "Email", "Telefone", "Observacoes", "Criado em"])

    for c in customers:
        ws.append(
            [
                c.id,
                c.nome,
                c.email,
                c.telefone,
                c.observacoes,
                c.criado_em.strftime("%d/%m/%Y %H:%M") if c.criado_em else "",
            ]
        )

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="clientes.xlsx",
        mimetype=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
    )


# ----------------------- API REST -----------------------


@app.route("/api/clientes", methods=["GET"])
@login_required
def api_list_customers():
    customers = Customer.query.order_by(Customer.criado_em.desc()).all()
    return jsonify([c.to_dict() for c in customers])


@app.route("/api/clientes/<int:customer_id>", methods=["GET"])
@login_required
def api_get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_dict())


@app.route("/api/clientes", methods=["POST"])
@login_required
@role_required("admin")
def api_create_customer():
    data = request.get_json() or {}
    nome = data.get("nome", "").strip()

    if not nome:
        return jsonify({"error": "campo nome obrigatorio"}), 400

    customer = Customer(
        nome=nome,
        email=data.get("email"),
        telefone=data.get("telefone"),
        observacoes=data.get("observacoes"),
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201


@app.route("/api/clientes/<int:customer_id>", methods=["PUT", "PATCH"])
@login_required
@role_required("admin")
def api_update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}

    if "nome" in data:
        customer.nome = data["nome"]
    if "email" in data:
        customer.email = data["email"]
    if "telefone" in data:
        customer.telefone = data["telefone"]
    if "observacoes" in data:
        customer.observacoes = data["observacoes"]

    db.session.commit()
    return jsonify(customer.to_dict())


@app.route("/api/clientes/<int:customer_id>", methods=["DELETE"])
@login_required
@role_required("admin")
def api_delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"status": "ok"}), 204


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
