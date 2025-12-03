# library-python
# Colaboradores do Projeto

```json
[
  {
    "nome": "Guilherme dos Santos Miranda",
    "matricula": "01699784"
  },
  {
    "nome": "Helton Robson dos Santos",
    "matricula": "01698749"
  },
  {
    "nome": "Jamylle da Silva Santana",
    "matricula": "01698776"
  },
  {
    "nome": "Larissa Vitória M de Souza",
    "matricula": "01703622"
  },
  {
    "nome": "Roberta Camila Ferreira dos Santos",
    "matricula": "01679746"
  }
]
```




# 📚 Sistema de Biblioteca – Documentação do Projeto

Este projeto implementa um sistema completo de gerenciamento de livros utilizando **SQLite**, **Flask** (interface web) e **FastAPI** (API REST).  
A documentação abaixo explica cada módulo, suas funções e os outputs esperados.

---

## 🗂️ 1. create_db.py – Criação do Banco de Dados

Script responsável por criar o arquivo `biblioteca.db` e sua estrutura inicial.

### ✔ Objetivo
Criar a estrutura inicial do banco de dados.

### ✔ Tecnologias
- Python `sqlite3` (nativo)

### ✔ Funcionamento
- Abre ou cria o arquivo `biblioteca.db`
- Executa o comando `CREATE TABLE IF NOT EXISTS`
- Salva (`commit`) e fecha conexão

### ✔ Estrutura da Tabela `livros`

| Campo            | Tipo                                | Descrição                  |
|------------------|--------------------------------------|----------------------------|
| id               | INTEGER PRIMARY KEY AUTOINCREMENT    | Identificador único        |
| titulo           | TEXT NOT NULL                        | Título do livro            |
| autor            | TEXT NOT NULL                        | Autor do livro             |
| ano_publicacao   | INTEGER NOT NULL                     | Ano do livro               |
| disponivel       | BOOLEAN NOT NULL                     | Se está disponível         |

### ✔ Output esperado
Ao executar:
python create_db.py

Gera:
biblioteca.db criado com a tabela 'livros'.
---

## 🌐 2. app_flask.py – Aplicação Web (Flask)

# 📌 Rotas da API (FastAPI)

A API expõe endpoints REST para operações CRUD sobre a tabela "livros".  
Abaixo estão todas as rotas, suas descrições, exemplos de requisição e respostas esperadas.

---

## GET /livros
Retorna todos os livros cadastrados.

### Exemplo de Requisição

### Resposta (200)
```json
[
  {
    "id": 1,
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "ano_publicacao": 1899,
    "disponivel": true
  }
]
```
POST /livros

Cria um novo livro no banco.

```
{
  "titulo": "Novo Livro",
  "autor": "Autor X",
  "ano_publicacao": 2020,
  "disponivel": true
}
```
```
{
  "message": "Livro criado com sucesso",
  "id": 5
}
```
GET /livros/{id}

Retorna um livro específico usando o ID.

```
GET /livros/3
{
  "id": 3,
  "titulo": "O Hobbit",
  "autor": "J. R. R. Tolkien",
  "ano_publicacao": 1937,
  "disponivel": true
}
```
```
{
  "error": "Livro não encontrado"
}
```
PUT /livros/{id}

Atualiza todos os campos de um livro existente.

```
{
  "titulo": "Livro Atualizado",
  "autor": "Autor Atualizado",
  "ano_publicacao": 2024,
  "disponivel": false
}
```
```
{
  "message": "Livro atualizado"
}
```
```
{
  "error": "Livro não encontrado"
}
```

DELETE /livros/{id}

Remove um livro do banco.
```
{
  "message": "Livro removido"
}
```
```
{
  "error": "Livro não encontrado"
}

```



## 🖥️ 3. index.html – Interface do Usuário

Template HTML (com Jinja2 + JS) usado pela aplicação Flask.

### ✔ Conteúdo do template
- Formulário para adicionar livros
- Tabela listando todos os livros
- Inputs editáveis acionados via JavaScript
- Botão de excluir usando POST com `_method=DELETE`

### ✔ Output visual esperado
- Lista atualizada automaticamente
- Edição inline
- Exclusão funcional

---

## ⚡ 4. api_fast.py – API REST (FastAPI)

API REST completa para integração ou consumo externo.  
Roda por padrão na **porta 8000**.

### ✔ Tecnologias
- FastAPI
- Pydantic
- SQLite3

### ✔ Modelo de Dados (Pydantic)
```python
class Livro(BaseModel):
    titulo: str
    autor: str
    ano_publicacao: int
    disponivel: bool
```
✔ Endpoints Implementados (CRUD)

```
Método	Rota	Descrição	Status Codes

GET	/livros	Lista todos os livros	200
GET	/livros/{id}	Retorna um livro específico	200, 404
POST	/livros	Adiciona um novo livro	201
PUT	/livros/{id}	Atualiza um livro existente	200, 404
DELETE	/livros/{id}	Remove um livro	200, 404
```
```
[
  {
    "id": 1,
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "ano_publicacao": 1899,
    "disponivel": true
  }
]
```
```
{
  "message": "Livro criado com sucesso",
  "id": 5
}
```
```
{
  "message": "Livro atualizado"
}
```
http://127.0.0.1:8000/docs


# 5.Processo de Retorno de HTML Dinâmico (Flask + Jinja2)

Este README explica como a aplicação Flask (`app_flask.py`) lida com a requisição de um usuário e retorna o conteúdo HTML dinâmico, utilizando o motor de templates Jinja2 e os dados do banco de dados SQLite.

---

## . Fluxo de Requisição e Resposta

O coração do retorno de HTML está na função de view do Flask, onde os dados são buscados e injetados em um template.

### A Rota Principal (app_flask.py)

A rota principal (`/`) é responsável por buscar a lista de livros no banco de dados (`biblioteca.db`) e usar o Flask para gerar o HTML final.

```python
# app_flask.py

from flask import Flask, render_template, request, redirect
import sqlite3
# ... (função connect)

# -----------------------
# Rota principal (GET)
# Lista livros
# -----------------------
@app.route("/", methods=["GET"])
def index():
    # 1. Busca os dados no banco de dados SQLite
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall() # 'livros' é uma lista de tuplas
    conn.close()

    # 2. Renderiza o template 'index.html', passando a lista de livros
    return render_template("index.html", livros=livros)
```
Explicação dos Passos

Busca de Dados: A função index() se conecta ao SQLite e executa uma query para buscar todos os livros, armazenando o resultado na variável livros.

Retorno de HTML: A função render_template("index.html", livros=livros) é chamada.

Ela localiza o template index.html (geralmente na pasta templates).

Passa a variável Python livros para o template, onde ela será acessível.

O Jinja2 processa o template, substituindo as variáveis e executando os loops.

O Flask retorna a string HTML final como resposta HTTP 200 (OK) para o navegador.

________________________________________________________________________________________________________________________________________________________________________________________________________________________________

O Template Dinâmico (index.html)

O arquivo index.html é um template Jinja2. Ele contém a estrutura HTML padrão, mas usa a sintaxe especial de templates para inserir o conteúdo dinâmico.

Uso do Jinja2 para Renderização de Dados

No template, a lista livros enviada pela rota do Flask é percorrida para construir a tabela de livros:
```
<tbody>
    {% for livro in livros %}
    <tr>
        <form method="POST" action="/atualizar/{{ livro[0] }}">
            <td>{{ livro[0] }}</td>
            <td><input type="text" name="titulo" value="{{ livro[1] }}" disabled required></td>
        </form>
    </tr>
    {% endfor %}
</tbody>
```
{% ... %}: Usado para blocos de controle (como for loops, if statements).

{{ ... }}: Usado para exibir o valor de uma variável.

O motor Jinja2 transforma esse código de template em HTML puro, injetando os dados de cada livro, antes que o Flask o envie ao navegador.



