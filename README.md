# 🧾 Sistema de Cadastro de Clientes

Sistema web simples para cadastro e gestão de clientes, desenvolvido em **Python (Flask)** com banco de dados **SQLite**.

## ✨ Funcionalidades

- Login simples (usuário e senha fixos para demonstração)
- Listagem de clientes com busca por nome, e-mail ou telefone
- Cadastro de novos clientes
- Edição de clientes
- Exclusão de clientes
- Interface limpa e responsiva

## 🛠️ Tecnologias

- Python
- Flask
- Flask SQLAlchemy
- SQLite
- HTML, CSS

## 🚀 Como executar

```bash
git clone https://github.com/SEU_USUARIO/sistema-cadastro-clientes.git
cd sistema-cadastro-clientes

# cria ambiente virtual (opcional, mas recomendado)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# instala dependências
pip install -r requirements.txt

# roda o servidor
python app.py
