from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import text                 
from database import engine, init_db
import hashlib

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="sua_chave_secreta_aqui")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse(request, "login.html")
@app.post("/login")
def login_post(request: Request, usuario: str = Form(...), senha: str = Form(...)):
    senha_md5 = hashlib.md5(senha.encode()).hexdigest()
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT id, usuario FROM usuarios WHERE usuario=:u AND senha=:s"),
            {"u": usuario, "s": senha_md5}
        ).fetchone()
    if row:
        request.session["usuario_id"] = row.id
        request.session["usuario"] = row.usuario
        return RedirectResponse("/", status_code=302)
    else:
        return templates.TemplateResponse(request, "login.html", {"erro": "Usuário ou senha inválidos"})
    
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)

@app.get("/")
def index(request: Request):
    if not request.session.get("usuario_id"):
        return RedirectResponse("/login", status_code=302)
    
    usuario_id = request.session["usuario_id"]
    with engine.connect() as conn:
        tarefas = conn.execute(
            text("SELECT * FROM tarefas WHERE usuario_id=:uid ORDER BY criado_em DESC"),
            {"uid": usuario_id}
        ).fetchall()
    
    return templates.TemplateResponse(request, "index.html", {"tarefas": tarefas})

@app.get("/nova")
def nova_get(request: Request):
    if not request.session.get("usuario_id"):
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse(request, "nova.html")

@app.post("/nova")
def nova_post(request: Request, titulo: str = Form(...), descricao: str = Form("")):
    if not request.session.get("usuario_id"):
        return RedirectResponse("/login", status_code=302)
    
    usuario_id = request.session["usuario_id"]
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO tarefas (titulo, descricao, usuario_id) VALUES (:t, :d, :u)"),
            {"t": titulo, "d": descricao, "u": usuario_id}
        )
        conn.commit()
    return RedirectResponse("/", status_code=302)

@app.get("/editar/{id}")
def editar_get(id: int, request: Request):
    if not request.session.get("usuario_id"):
        return RedirectResponse("/login", status_code=302)
    
    with engine.connect() as conn:
        tarefa = conn.execute(
            text("SELECT * FROM tarefas WHERE id=:id AND usuario_id=:uid"),
            {"id": id, "uid": request.session["usuario_id"]}
        ).fetchone()
    
    return templates.TemplateResponse(request, "editar.html", {"tarefa": tarefa})

@app.post("/editar/{id}")
def editar_post(id: int, request: Request, titulo: str = Form(...),
                descricao: str = Form(""), status: str = Form(...)):
    if not request.session.get("usuario_id"):
        return RedirectResponse("/login", status_code=302)
    
    with engine.connect() as conn:
        conn.execute(
            text("UPDATE tarefas SET titulo=:t, descricao=:d, status=:s WHERE id=:id AND usuario_id=:uid"),
            {"t": titulo, "d": descricao, "s": status, "id": id, "uid": request.session["usuario_id"]}
        )
        conn.commit()
    return RedirectResponse("/", status_code=302)

@app.get("/concluir/{id}")
def concluir(id: int, request: Request):
    if not request.session.get("usuario_id"):
        return RedirectResponse("/login", status_code=302)
    
    with engine.connect() as conn:
        conn.execute(
            text("UPDATE tarefas SET status='concluida' WHERE id=:id AND usuario_id=:uid"),
            {"id": id, "uid": request.session["usuario_id"]}
        )
        conn.commit()
    return RedirectResponse("/", status_code=302)

@app.get("/excluir/{id}")
def excluir(id: int, request: Request):
    if not request.session.get("usuario_id"):
        return RedirectResponse("/login", status_code=302)
    
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM tarefas WHERE id=:id AND usuario_id=:uid"),
            {"id": id, "uid": request.session["usuario_id"]}
        )
        conn.commit()
    return RedirectResponse("/", status_code=302)