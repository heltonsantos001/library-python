"""
api_fast.py
API REST completa para consumir a tabela 'livros' do banco SQLite (biblioteca.db)

Tecnologias usadas:
- FastAPI (para criação da API REST)
- Pydantic (validação dos dados)
- SQLite3 (banco de dados)
- Uvicorn (servidor ASGI para rodar a API)

Endpoints implementados:
    GET /livros              -> Lista todos os livros
    GET /livros/{id}         -> Retorna um livro específico
    POST /livros             -> Adiciona um novo livro
    PUT /livros/{id}         -> Atualiza um livro existente
    DELETE /livros/{id}      -> Deleta um livro do banco

Para rodar:
    uvicorn api_fast:app --reload --port 8000

Swagger automático:
    http://127.0.0.1:8000/docs
"""

import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# -----------------------------------------------------------
#   MODELO DE DADOS (VALIDAÇÃO COM Pydantic)
# -----------------------------------------------------------

class Livro(BaseModel):
    titulo: str
    autor: str
    ano_publicacao: int
    disponivel: bool


# -----------------------------------------------------------
#   FUNÇÃO DE CONEXÃO COM O BANCO
# -----------------------------------------------------------

def connect():
    """Abre conexão com o banco SQLite (biblioteca.db)."""
    return sqlite3.connect("biblioteca.db")


# -----------------------------------------------------------
#       INICIALIZAÇÃO DA APLICAÇÃO FASTAPI
# -----------------------------------------------------------

app = FastAPI(
    title="API Biblioteca Universitária",
    description="API para gerenciamento de livros usando SQLite + FastAPI",
    version="1.0.0"
)


# -----------------------------------------------------------
#       GET /livros - Lista todos os livros
# -----------------------------------------------------------
@app.get("/livros")
def listar_livros():
    """
    Retorna todos os livros cadastrados no banco de dados.

    Exemplo de resposta:
    [
        {
            "id": 1,
            "titulo": "Dom Casmurro",
            "autor": "Machado de Assis",
            "ano_publicacao": 1899,
            "disponivel": true
        }
    ]
    """

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM livros")
    rows = cursor.fetchall()

    conn.close()

    livros = []
    for r in rows:
        livros.append({
            "id": r[0],
            "titulo": r[1],
            "autor": r[2],
            "ano_publicacao": r[3],
            "disponivel": bool(r[4])
        })

    return livros


# -----------------------------------------------------------
#       GET /livros/{id} - Busca livro por ID
# -----------------------------------------------------------
@app.get("/livros/{id}")
def obter_livro(id: int):
    """
    Retorna um único livro pelo seu ID.

    Se o ID não existir, retorna 404.
    """

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM livros WHERE id=?", (id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    return {
        "id": row[0],
        "titulo": row[1],
        "autor": row[2],
        "ano_publicacao": row[3],
        "disponivel": bool(row[4])
    }


# -----------------------------------------------------------
#       POST /livros - Adicionar novo livro
# -----------------------------------------------------------
@app.post("/livros", status_code=201)
def adicionar_livro(livro: Livro):
    """
    Adiciona um novo livro ao banco.

    Exemplo de JSON enviado:
    {
        "titulo": "Harry Potter",
        "autor": "J.K. Rowling",
        "ano_publicacao": 1997,
        "disponivel": true
    }
    """

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO livros (titulo, autor, ano_publicacao, disponivel)
        VALUES (?, ?, ?, ?)
    """, (livro.titulo, livro.autor, livro.ano_publicacao, livro.disponivel))

    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return {"mensagem": "Livro cadastrado com sucesso!", "id": novo_id}


# -----------------------------------------------------------
#       PUT /livros/{id} - Atualizar livro
# -----------------------------------------------------------
@app.put("/livros/{id}")
def atualizar_livro(id: int, livro: Livro):
    """
    Atualiza os dados de um livro existente.

    Se o ID não existir, retorna 404.
    """

    conn = connect()
    cursor = conn.cursor()

   
    cursor.execute("SELECT * FROM livros WHERE id=?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    
    cursor.execute("""
        UPDATE livros
        SET titulo=?, autor=?, ano_publicacao=?, disponivel=?
        WHERE id=?
    """, (livro.titulo, livro.autor, livro.ano_publicacao, livro.disponivel, id))

    conn.commit()
    conn.close()

    return {"mensagem": "Livro atualizado com sucesso."}


# -----------------------------------------------------------
#       DELETE /livros/{id} - Remover livro
# -----------------------------------------------------------
@app.delete("/livros/{id}")
def deletar_livro(id: int):
    """
    Remove um livro pelo ID.

    Se o ID não existir, retorna 404.
    """

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM livros WHERE id=?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    cursor.execute("DELETE FROM livros WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return {"mensagem": "Livro deletado com sucesso."}
