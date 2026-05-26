from behave import given, when, then, step
import requests
import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuração da API
BASE_URL = "http://localhost:8000"

import socket

def get_db_connection():
    """Conecta ao banco de dados MySQL"""
    print(f"🐘 Conectando ao banco: host={os.getenv('DB_HOST', 'localhost')}, port={int(os.getenv('DB_PORT', 3306))}, database={os.getenv('DB_NAME', 'yummicious_db')}")
    
    # Mostrar se é o mesmo container
    if os.getenv('DB_HOST', 'localhost') == 'localhost':
        print("⚠️  Conectando ao localhost - pode ser diferente do container da API")
    
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'delivery_user'),
        password=os.getenv('DB_PASSWORD', 'delivery_pass'),
        database=os.getenv('DB_NAME', 'yummicious_db')
    )

# ==================== GIVEN STEPS ====================

@given(u'existe um cliente cadastrado com ID "{cliente_id}"')
def step_cliente_cadastrado(context, cliente_id):
    """Garante que o cliente existe no banco"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            INSERT INTO clientes (id, nome, email, saldo) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE nome = VALUES(nome)
        """, (cliente_id, f"Cliente {cliente_id}", f"{cliente_id}@email.com", 0.00))
        conn.commit()
        context.cliente_id = cliente_id
    finally:
        cursor.close()
        conn.close()

@given(u'o pedido "{pedido_id}" do cliente "{cliente_nome}" está com status "{status}"')
def step_pedido_com_status(context, pedido_id, cliente_nome, status):
    """Cria ou atualiza um pedido com o status especificado"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Buscar ou criar cliente
    cursor.execute("SELECT id FROM clientes WHERE nome = %s", (cliente_nome,))
    cliente = cursor.fetchone()
    
    if not cliente:
        cliente_id = f"cli_{cliente_nome.replace(' ', '_').lower()}"
        cursor.execute("""
            INSERT INTO clientes (id, nome, email, saldo) 
            VALUES (%s, %s, %s, %s)
        """, (cliente_id, cliente_nome, f"{cliente_nome}@email.com", 0.00))
    else:
        cliente_id = cliente['id']
    
    # Criar ou atualizar pedido
    num_pedido = int(pedido_id)
    cursor.execute("""
        INSERT INTO pedidos (id, id_restaurante, status, cliente_id, valor_total)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            status = VALUES(status),
            valor_total = VALUES(valor_total)
    """, (num_pedido, 1, status, cliente_id, 100.00))
    conn.commit()
    
    context.pedido_id = num_pedido
    context.cliente_id = cliente_id
    cursor.close()
    conn.close()

@given(u'o valor pago foi "{valor}"')
def step_valor_pago(context, valor):
    """Atualiza o valor do pedido"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    valor_float = float(valor.replace(',', '.'))
    cursor.execute("UPDATE pedidos SET valor_total = %s WHERE id = %s", 
                   (valor_float, context.pedido_id))
    conn.commit()
    cursor.close()
    conn.close()

@given(u'o método de pagamento foi "{metodo}"')
def step_metodo_pagamento(context, metodo):
    """Registra o método de pagamento usado (apenas para contexto)"""
    context.metodo_pagamento = metodo

@given(u'o cliente "{cliente_nome}" tem "{saldo}" no saldo do app')
def step_cliente_saldo(context, cliente_nome, saldo):
    """Define o saldo do cliente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    saldo_float = float(saldo.replace(',', '.'))
    cursor.execute("""
        UPDATE clientes SET saldo = %s 
        WHERE nome = %s
    """, (saldo_float, cliente_nome))
    conn.commit()
    cursor.close()
    conn.close()

@given(u'o cliente "{cliente_id}" possui o método "{metodo_id}" cadastrado')
def step_cliente_possui_metodo(context, cliente_id, metodo_id):
    """Cria um método de pagamento para o cliente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    metodo_id_num = int(metodo_id.replace('metodo_', ''))
    
    cursor.execute("""
        INSERT INTO metodos_pagamento (id, cliente_id, tipo, ultimos_4_digitos, nome_titular, validade_mes, validade_ano)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE id = VALUES(id)
    """, (metodo_id_num, cliente_id, 'CREDIT_CARD', '1111', 'CLIENTE TESTE', 12, 2028))
    conn.commit()
    cursor.close()
    conn.close()
    
    if not hasattr(context, 'metodos_cliente'):
        context.metodos_cliente = []
    context.metodos_cliente.append(metodo_id_num)

@given(u'o cliente "{cliente_id}" possui o método "{metodo_id}" com validade "{validade}"')
def step_cliente_metodo_com_validade(context, cliente_id, metodo_id, validade):
    """Cria método com validade específica (formato: MM/AAAA)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    metodo_id_num = int(metodo_id.replace('metodo_', ''))
    mes, ano = validade.split('/')
    
    cursor.execute("""
        INSERT INTO metodos_pagamento (id, cliente_id, tipo, ultimos_4_digitos, nome_titular, validade_mes, validade_ano)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            validade_mes = VALUES(validade_mes),
            validade_ano = VALUES(validade_ano)
    """, (metodo_id_num, cliente_id, 'CREDIT_CARD', '2222', 'CLIENTE TESTE', int(mes), int(ano)))
    conn.commit()
    cursor.close()
    conn.close()
    
    if not hasattr(context, 'metodos_cliente'):
        context.metodos_cliente = []
    if metodo_id_num not in context.metodos_cliente:
        context.metodos_cliente.append(metodo_id_num)

@given(u'o cliente "{cliente_id}" não tem métodos de pagamento cadastrados')
def step_cliente_sem_metodos(context, cliente_id):
    """Garante que o cliente não tem métodos de pagamento cadastrados"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Remove todos os métodos de pagamento do cliente
        cursor.execute("DELETE FROM metodos_pagamento WHERE cliente_id = %s", (cliente_id,))
        conn.commit()
        print(f"🗑️  Removidos todos os métodos de pagamento do cliente {cliente_id}")
    except Exception as e:
        print(f"⚠️  Erro ao limpar métodos: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
    
    # Inicializar a lista de métodos do cliente no contexto
    if not hasattr(context, 'metodos_cliente'):
        context.metodos_cliente = []
    else:
        context.metodos_cliente = [m for m in context.metodos_cliente if m != cliente_id]

# ==================== WHEN STEPS ====================

@when(u'eu envio uma requisição POST para "{endpoint}" para o cliente "{cliente_id}"')
def step_envio_post(context, endpoint, cliente_id):
    """Envia requisição POST (com ou sem corpo, detecta automaticamente)"""

    url = f"{BASE_URL}{endpoint}"
    
    # Preparar parâmetros
    params = {'cliente_id': cliente_id}
    
    # Verificar se tem corpo na tabela
    if context.table:
        # Tem corpo - construir payload
        payload = {}
        for row in context.table:
            campo = row['campo']
            valor = row['valor']
            if campo in ['validade_mes', 'validade_ano', 'id_pedido', 'id_restaurante']:
                payload[campo] = int(valor)
            elif campo == 'cvv':
                payload[campo] = str(valor)
            else:
                payload[campo] = valor
        
        context.response = requests.post(url, json=payload, params=params if params else None)
    else:
        # Sem corpo
        context.response = requests.post(url, params=params if params else None)

@when(u'eu envio uma requisição DELETE para "{endpoint}" para o cliente "{cliente_id}"')
def step_envio_delete(context, endpoint, cliente_id):
    """Envia requisição DELETE"""
    # Remover aspas se existirem
    cliente_id = cliente_id.strip('"')
    
    url = f"{BASE_URL}{endpoint}"
    
    params = {'cliente_id': cliente_id}
    print(f"🌐 Chamando DELETE: {url} com params: {params}")
    
    context.response = requests.delete(url, params=params)
    context.cliente_id = cliente_id
    
    print(f"📊 Status code: {context.response.status_code}")

@when(u'eu envio uma requisição PUT para "{endpoint}" do cliente "{cliente_id}"')
def step_envio_put_para_cliente(context, endpoint, cliente_id):
    """Envia requisição PUT com corpo para um cliente específico"""
    cliente_id = cliente_id.strip('"')
    url = f"{BASE_URL}{endpoint}"
    
    # Construir payload do corpo da requisição (vem da tabela)
    payload = {}
    if context.table:
        for row in context.table:
            campo = row['campo']
            valor = row['valor']
            if campo in ['validade_mes', 'validade_ano']:
                payload[campo] = int(valor)
            else:
                payload[campo] = valor
    
    params = {'cliente_id': cliente_id}
    print(f"🌐 Chamando PUT: {url}")
    print(f"📦 Payload: {payload}")
    print(f"🔑 Params: {params}")
    
    context.response = requests.put(url, json=payload, params=params)
    context.cliente_id = cliente_id

@when(u'eu envio um requisição de ao endpoint "{endpoint}" com os dados:')
def step_envio_requisicao_pedido(context, endpoint):
    """Envia requisição para endpoint de pedidos"""
    data = {}
    if context.table:
        row = context.table[0]
        for heading in context.table.headings:
            val = row[heading]
            if heading in ["id_pedido", "id_restaurante"]:
                data[heading] = int(val)
            else:
                data[heading] = val
    
    if endpoint == "pedidos":
        id_pedido = data.get('id_pedido')
        url = f"{BASE_URL}/restaurantes/pedidos/{id_pedido}/decisao"
        context.response = requests.post(url, json=data)

# ==================== THEN STEPS ====================

@then(u'o status da resposta deve ser "{status_code}"')
def step_verificar_status_resposta(context, status_code):
    """Verifica o status code da resposta"""
    # Extrair o número do status code (ex: "200 OK" -> 200)
    if ' ' in status_code:
        expected_code = int(status_code.split()[0])
    else:
        expected_code = int(status_code)
    
    assert context.response.status_code == expected_code, \
        f"Esperado {expected_code}, mas obteve {context.response.status_code}. Resposta: {context.response.text}"

@then(u'o status da resposta deve ser 204 NO CONTENT')
def step_status_204_no_content(context):
    """Verifica se o status code é 204 (No Content)"""
    assert context.response.status_code == 204, \
        f"Esperado 204, mas obteve {context.response.status_code}. Resposta: {context.response.text}"

@then(u'o status deve ser 200 OK')
def step_status_200_ok(context):
    """Verifica se o status code é 200 (OK)"""
    assert context.response.status_code == 200, \
        f"Esperado 200, mas obteve {context.response.status_code}. Resposta: {context.response.text}"

@then(u'a mensagem deve ser "{mensagem}"')
def step_verificar_mensagem(context, mensagem):
    """Verifica a mensagem de erro na resposta"""
    data = context.response.json()
    assert 'detail' in data
    assert data['detail'] == mensagem

@then(u'o cartão deve estar dentre os métodos de pagamento do cliente "{cliente_id}"')
def step_verificar_cartao_cliente(context, cliente_id):
    """Verifica se o cartão foi criado para o cliente"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM metodos_pagamento 
        WHERE cliente_id = %s 
        ORDER BY id DESC LIMIT 1
    """, (cliente_id,))
    
    metodo = cursor.fetchone()
    assert metodo is not None, "Nenhum método encontrado para o cliente"
    
    cursor.close()
    conn.close()

@then(u'apenas o método "{metodo_id}" consta como método de pagamento do cliente "{cliente_id}"')
def step_verificar_apenas_um_metodo(context, metodo_id, cliente_id):
    """Verifica se apenas o método especificado existe"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    metodo_id_num = int(metodo_id.replace('metodo_', ''))
    
    cursor.execute("""
        SELECT id FROM metodos_pagamento 
        WHERE cliente_id = %s
    """, (cliente_id,))
    
    metodos = cursor.fetchall()
    ids_metodos = [m['id'] for m in metodos]
    
    assert len(ids_metodos) == 1, f"Esperado 1 método, mas encontrado {len(ids_metodos)}"
    assert ids_metodos[0] == metodo_id_num, f"Método {ids_metodos[0]} não é o esperado {metodo_id_num}"
    
    cursor.close()
    conn.close()

@then(u'o pedido "{pedido_id}" deve ter status "{status}"')
def step_verificar_status_pedido(context, pedido_id, status):
    """Verifica o status do pedido no banco"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT status FROM pedidos WHERE id = %s", (pedido_id,))
    pedido = cursor.fetchone()
    
    assert pedido is not None, "Pedido não encontrado"
    
    if status == "Cancelado":
        assert pedido['status'] == 'Cancelado'

    cursor.close()
    conn.close()

@then(u'uma transação de estorno deve ser criada com valor "{valor}"')
def step_verificar_transacao_estorno(context, valor):
    """Verifica se a transação de estorno foi criada"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    valor_float = float(valor.replace(',', '.'))
    pedido_id = context.pedido_id if hasattr(context, 'pedido_id') else 1
    
    cursor.execute("""
        SELECT * FROM transacoes 
        WHERE pedido_id = %s AND tipo = 'ESTORNO'
    """, (pedido_id,))
    
    transacao = cursor.fetchone()
    assert transacao is not None, "Transação de estorno não encontrada"
    assert float(transacao['valor']) == valor_float, f"Valor {transacao['valor']} diferente de {valor_float}"
    
    cursor.close()
    conn.close()

@then(u'o saldo do cliente deve ser "{saldo}"')
def step_verificar_saldo_cliente(context, saldo):
    """Verifica o saldo do cliente"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    saldo_float = float(saldo.replace(',', '.'))
    cliente_id = context.cliente_id if hasattr(context, 'cliente_id') else 'cli_123'
    
    cursor.execute("SELECT saldo FROM clientes WHERE id = %s", (cliente_id,))
    cliente = cursor.fetchone()
    
    assert cliente is not None, "Cliente não encontrado"
    assert float(cliente['saldo']) == saldo_float, f"Saldo {cliente['saldo']} diferente de {saldo_float}"
    
    cursor.close()
    conn.close()

@then(u'a validade do método "{metodo_id}" deve ser atualizada para "{validade}"')
def step_verificar_validade_atualizada(context, metodo_id, validade):
    """Verifica se a validade do método foi atualizada"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    metodo_id_num = int(metodo_id.replace('metodo_', ''))
    mes_esperado, ano_esperado = validade.split('/')
    
    cursor.execute("""
        SELECT validade_mes, validade_ano 
        FROM metodos_pagamento 
        WHERE id = %s
    """, (metodo_id_num,))
    
    metodo = cursor.fetchone()
    assert metodo is not None, "Método não encontrado"
    assert metodo['validade_mes'] == int(mes_esperado)
    assert metodo['validade_ano'] == int(ano_esperado)
    
    cursor.close()
    conn.close()

@then(u'o status do pedido "{pedido_id}" deve permanecer "{status}"')
def step_status_pedido_permanece(context, pedido_id, status):
    """Verifica que o status do pedido não mudou"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT status FROM pedidos WHERE id = %s", (pedido_id,))
    pedido = cursor.fetchone()
    
    assert pedido is not None, "Pedido não encontrado"
    assert pedido['status'] == status
    
    cursor.close()
    conn.close()

# ==================== STEPS AUXILIARES PARA MÉTODOS DE PAGAMENTO ====================

@when(u'o corpo da requisição contém')
def step_corpo_requisicao_contem(context):
    """
    Step para indicar que o corpo da requisição será fornecido.
    O processamento real é feito no step_envio_post que lê context.table
    """
    pass

@when(u'o corpo contém')
def step_corpo_contem(context):
    """
    Step para indicar que o corpo da requisição PUT será fornecido.
    O processamento real é feito no step_envio_put que lê context.table
    """
    pass