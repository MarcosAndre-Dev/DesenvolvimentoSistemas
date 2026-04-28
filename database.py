import hashlib
from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///./tarefas.db"
engine = create_engine(DATABASE_URL)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                status TEXT DEFAULT 'pendente',
                usuario_id INTEGER,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        senha_md5 = hashlib.md5("123456".encode()).hexdigest()
        conn.execute(text("""
            INSERT OR IGNORE INTO usuarios (usuario, senha)
            VALUES ('admin', :senha)
        """), {"senha": senha_md5})
        conn.commit()