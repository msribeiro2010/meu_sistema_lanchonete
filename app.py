from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Configurações de conexão ao PostgreSQL
DB_HOST = "localhost"       # ou outro host
DB_NAME = "db_mar_lanches"      # nome do banco
DB_USER = "postgres"        # usuário
DB_PASS = "mar"     # senha

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

# -----------------------------
#  CLIENTES
# -----------------------------
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        # Coletar dados do form
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        data_cadastro = request.form.get('data_cadastro')
        
        # Inserir no banco
        cur.execute("""
            INSERT INTO clientes (nome, telefone, endereco, data_cadastro)
            VALUES (%s, %s, %s, %s)
        """, (nome, telefone, endereco, data_cadastro))
        
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('clientes'))
    
    # Se for GET, listamos os clientes
    cur.execute("SELECT id, nome, telefone, endereco, data_cadastro FROM clientes ORDER BY id;")
    lista_clientes = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('clientes.html', clientes=lista_clientes)


# -----------------------------
#  FORNECEDORES
# -----------------------------
@app.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        data_contratacao = request.form.get('data_contratacao')
        observacoes = request.form.get('observacoes')

        cur.execute("""
            INSERT INTO fornecedores (nome, telefone, email, data_contratacao, observacoes)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, telefone, email, data_contratacao, observacoes))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('fornecedores'))
    
    cur.execute("SELECT id, nome, telefone, email, data_contratacao, observacoes FROM fornecedores ORDER BY id;")
    lista_fornecedores = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('fornecedores.html', fornecedores=lista_fornecedores)


# -----------------------------
#  PEDIDOS
# -----------------------------
@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        mesa = request.form.get('mesa')
        data_hora_pedido = request.form.get('data_hora_pedido')
        situacao = request.form.get('situacao')
        
        cur.execute("""
            INSERT INTO pedidos (mesa, data_hora_pedido, situacao)
            VALUES (%s, %s, %s)
        """, (mesa, data_hora_pedido, situacao))
        
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('pedidos'))
    
    cur.execute("SELECT id, mesa, data_hora_pedido, situacao FROM pedidos ORDER BY id;")
    lista_pedidos = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('pedidos.html', pedidos=lista_pedidos)


# -----------------------------
#  INGREDIENTES ESTOQUE
# -----------------------------
@app.route('/ingredientes', methods=['GET', 'POST'])
def ingredientes():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')

        cur.execute("""
            INSERT INTO ingredientes_estoque (nome, categoria)
            VALUES (%s, %s)
        """, (nome, categoria))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('ingredientes'))
    
    cur.execute("SELECT id, nome, categoria FROM ingredientes_estoque ORDER BY id;")
    lista_ingredientes = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('ingredientes.html', ingredientes=lista_ingredientes)


# -----------------------------
#  EXECUÇÃO
# -----------------------------
if __name__ == '__main__':
    # Em dev, debug=True
    app.run(debug=True, host='0.0.0.0', port=5001)
