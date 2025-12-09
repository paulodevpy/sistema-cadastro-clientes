# 🧾 Sistema de Cadastro de Clientes (Versão PRO)

Sistema web completo para gestão de clientes, desenvolvido em **Python (Flask)**, com foco em portfólio profissional.

Este projeto vai além de um CRUD comum, incluindo **dashboard, gráficos, exportação de dados, API REST e controle de níveis de usuários**.

---

## 🚀 Funcionalidades

### 🔐 Autenticação e Níveis de Acesso

- Login com dois perfis:
  - **Admin:** acesso total ao sistema (CRUD, exportações e API completa)
  - **Somente leitura:** apenas visualização e busca
- Usuários padrão:
  - `admin / admin123`
  - `user / user123`

---

### 👥 Gestão de Clientes (CRUD Completo)

- Cadastro de cliente
- Edição de cliente
- Exclusão de cliente
- Listagem com ordenação por data
- Busca por:
  - Nome
  - E-mail
  - Telefone
- Cadastro com:
  - Nome
  - E-mail
  - Telefone (com máscara automática)
  - Observações
  - Data de criação automática

---

### 📊 Dashboard Profissional

- Cards de métricas:
  - Total de clientes
  - Clientes com e-mail
  - Clientes com telefone
- Gráfico de clientes cadastrados por mês usando **Chart.js**

---

### 📤 Exportação de Dados

- Exportação para **Excel (.xlsx)**
- Exportação para **CSV**
- Downloads disponíveis apenas para usuário **admin**

---

### 🌐 API REST Completa

Endpoints disponíveis:

- `GET /api/clientes`
- `GET /api/clientes/<id>`
- `POST /api/clientes` (admin)
- `PUT /api/clientes/<id>` (admin)
- `DELETE /api/clientes/<id>` (admin)

API ideal para integração com:

- Aplicativos Mobile
- Frontend React
- Sistemas terceiros

---

### 📱 Máscara Automática de Telefone

- Formato automático ao digitar:
  - `(11) 98765-4321`
- Implementado em JavaScript puro

---

### 🔎 Busca Inteligente

- Pesquisa dinâmica por nome, e-mail ou telefone

---

## 🛠️ Tecnologias Utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5
- CSS3
- JavaScript (Vanilla)
- Chart.js
- openpyxl

---

## 📂 Estrutura do Projeto

```text
sistema-cadastro-clientes/
├─ app.py
├─ requirements.txt
├─ instance/
│  └─ app.db
├─ templates/
│  ├─ base.html
│  ├─ login.html
│  ├─ customers.html
│  └─ customer_form.html
└─ static/
   └─ styles.css
```

---

## 🚀 Como Executar o Projeto Localmente

1. Clone o repositório:

```bash
git clone https://github.com/paulodevpy/sistema-cadastro-clientes.git
cd sistema-cadastro-clientes
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
python app.py
```

5. Acesse no navegador:

```text
http://127.0.0.1:5000
```

### 🔑 Usuários de Teste

- **Admin:** `admin / admin123`  
- **Somente leitura:** `user / user123`

---

## 💼 Projeto Profissional para Portfólio

Este projeto demonstra:

- Backend completo com Flask  
- Autenticação e autorização por nível de acesso  
- API REST integrada  
- Dashboard com gráficos  
- Exportação de dados (Excel e CSV)  
- Interface moderna baseada em painel administrativo  

Pode ser facilmente adaptado para:

- Clínicas  
- Escritórios  
- Consultorias  
- Imobiliárias  
- Academias  
- Empresas em geral 