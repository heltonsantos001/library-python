from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -----------------------
# Função de conexão
# -----------------------
def connect():
    return sqlite3.connect("biblioteca.db")

# -----------------------
# Rota principal (GET)
# Lista livros
# -----------------------
@app.route("/", methods=["GET"])
def index():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    conn.close()
    return render_template("index.html", livros=livros)

# -----------------------
# Rota para criar livro (POST)
# -----------------------
@app.route("/adicionar", methods=["POST"])
def adicionar():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    ano = request.form["ano_publicacao"]
    disponivel = request.form.get("disponivel") == "on"

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO livros (titulo, autor, ano_publicacao, disponivel)
        VALUES (?, ?, ?, ?)
    """, (titulo, autor, int(ano), disponivel))
    conn.commit()
    conn.close()

    return redirect("/")

# -----------------------
# Rota para atualizar (PUT/PATCH)
# -----------------------
@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    metodo = request.form.get("_method")

    # Se for DELETE → chama a rota de deletar
    if metodo == "DELETE":
        return deletar(id)

    # Se for PATCH/PUT → atualizar parcialmente ou totalmente
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    ano = request.form["ano_publicacao"]
    disponivel = request.form.get("disponivel") == "on"

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE livros
        SET titulo=?, autor=?, ano_publicacao=?, disponivel=?
        WHERE id=?
    """, (titulo, autor, int(ano), disponivel, id))
    conn.commit()
    conn.close()

    return redirect("/")

# -----------------------
# DELETE
# -----------------------
def deletar(id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livros WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
