# 📋 Sistema de Tarefas — FastAPI

Sistema web de gerenciamento de tarefas desenvolvido com **Python + FastAPI**, utilizando **SQLite** como banco de dados e **Bootstrap 5** como framework de layout.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| Python 3 | Linguagem principal |
| FastAPI | Framework web (rotas, requisições) |
| SQLAlchemy | Conexão e queries no banco de dados |
| SQLite | Banco de dados local |
| Jinja2 | Renderização dos templates HTML |
| Bootstrap 5 | Framework de layout (via CDN) |
| Uvicorn | Servidor ASGI para rodar a aplicação |
| itsdangerous | Gerenciamento seguro de sessões |

---

## 📁 Estrutura do Projeto

```
AVA01/
├── venv/                  # Ambiente virtual Python
├── main.py                # Rotas da aplicação (login, logout, CRUD de tarefas)
├── database.py            # Conexão com o banco e criação das tabelas
├── requirements.txt       # Dependências do projeto
├── tarefas.db             # Banco de dados SQLite (gerado automaticamente)
└── templates/
    ├── layout.html        # Template base com navbar (herdado por todas as páginas)
    ├── login.html         # Tela de login
    ├── index.html         # Listagem de tarefas
    ├── nova.html          # Formulário para nova tarefa
    └── editar.html        # Formulário de edição de tarefa
```

---

## ▶️ Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/MarcosAndre-Dev/DesenvolvimentoSistemas.git
cd DesenvolvimentoSistemas
```

### 2. Crie e ative o ambiente virtual (venv)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/Scripts/Activate
```

> Após ativar, o terminal deve exibir `(venv)` no início da linha.

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode o servidor

```bash
uvicorn main:app --reload
```

### 5. Acesse no navegador

```
http://localhost:8000
```

---

## 🔐 Credenciais de Acesso

O usuário de teste é criado **automaticamente** na primeira execução:

| Campo | Valor |
|---|---|
| Usuário | `admin` |
| Senha | `123456` |

> A senha é armazenada em **MD5** no banco de dados, conforme especificado no enunciado.

---

## 🗄️ Banco de Dados

O banco **`tarefas.db`** (SQLite) é criado automaticamente ao iniciar a aplicação. Ele contém duas tabelas:

**`usuarios`**
| Coluna | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| usuario | TEXT | Nome de usuário (único) |
| senha | TEXT | Senha em MD5 |

**`tarefas`**
| Coluna | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| titulo | TEXT | Título da tarefa |
| descricao | TEXT | Descrição (opcional) |
| status | TEXT | `"pendente"` ou `"concluida"` |
| usuario_id | INTEGER | FK para `usuarios` |
| criado_em | TIMESTAMP | Data de criação |

---

## 🔗 Rotas da Aplicação

| Método | Rota | Descrição |
|---|---|---|
| GET | `/login` | Exibe o formulário de login |
| POST | `/login` | Processa o login (valida MD5) |
| GET | `/logout` | Encerra a sessão e redireciona |
| GET | `/` | Lista as tarefas do usuário logado |
| GET | `/nova` | Exibe formulário de nova tarefa |
| POST | `/nova` | Salva nova tarefa no banco |
| GET | `/editar/{id}` | Exibe formulário preenchido para editar |
| POST | `/editar/{id}` | Atualiza tarefa no banco |
| GET | `/concluir/{id}` | Muda status para `"concluida"` |
| GET | `/excluir/{id}` | Remove a tarefa do banco |

---

## ✅ Funcionalidades

- [x] Autenticação com usuário e senha (MD5)
- [x] Sessão protegida — páginas inacessíveis sem login
- [x] Listagem de tarefas com badge de status colorido
- [x] Criar nova tarefa
- [x] Editar tarefa (título, descrição e status)
- [x] Concluir tarefa com um clique
- [x] Excluir tarefa com confirmação
- [x] Layout responsivo com Bootstrap 5
- [x] Navbar com nome do usuário logado e botão de logout
- [x] Prepared statements em todas as queries (segurança contra SQL Injection)

---

## 📦 Dependências (`requirements.txt`)

```
fastapi
uvicorn
sqlalchemy
jinja2
python-multipart
itsdangerous
```

---

## 👨‍💻 Observações Técnicas

- O projeto utiliza **`SessionMiddleware`** do Starlette para gerenciar sessões, equivalente ao `$_SESSION` do PHP.
- Todas as queries ao banco usam **prepared statements** com parâmetros nomeados via `SQLAlchemy text()`, prevenindo SQL Injection.
- O banco **SQLite** é gerado automaticamente na pasta do projeto — não é necessário configurar nenhum servidor de banco de dados.
- O framework de layout escolhido foi o **Bootstrap 5**, importado via CDN em `layout.html`.