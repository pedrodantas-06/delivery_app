from behave import given, when, then
import requests
import mysql.connector
from backend.core.config import settings
from datetime import datetime
from backend.core.conexao_banco import ConexaoBanco

BASE_URL = f"http://localhost:8000{settings.API_V1_STR}"

def get_db_connection():
    host_atual = "localhost" if settings.DB_HOST == "db" else settings.DB_HOST
    return mysql.connector.connect(
        host=host_atual,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )

@given(u'que o endpoint de "{endpoint}" está "{status}"')
def step_endpoint_disponivel(context, endpoint, status):
    rotas = {
        "cadastro de restaurante": f"{BASE_URL}/restaurantes/cadastrar",
        "edição de restaurante": f"{BASE_URL}/restaurantes/atualizar/123",
        "remoção de restaurante": f"{BASE_URL}/restaurantes/remover/123",
        "pedidos": f"{BASE_URL}/restaurantes/pedidos/987/decisao",
        "restaurantes": f"{BASE_URL}/restaurantes/status"
    }
    
    url_alvo = rotas.get(endpoint)
    if not url_alvo:
        raise ValueError(f"O endpoint '{endpoint}' não foi mapeado no arquivo de steps.")
    context.endpoint = url_alvo

    try:
        context.response = requests.get(f"{BASE_URL}/restaurantes")
        
        if status == "disponível":
            assert context.response.status_code < 500, f"API fora do ar! Código: {context.response.status_code}"
    except requests.ConnectionError:
        raise AssertionError("O servidor FastAPI está completamente desligado. Inicie o servidor backend antes dos testes.")

@given(u'que o "{entidade}" cujo "{campo}" é "{valor}" "{existencia}" na tabela "{tabela}" do banco de dados')
def step_verificar_existencia_db(context, entidade, campo, valor, existencia, tabela):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = f"SELECT * FROM {tabela} WHERE {campo} = %s"
        if campo == "id":
            cursor.execute(query, (int(valor),))
        else:
            cursor.execute(query, (valor,))
            
        result = cursor.fetchone()
        print(existencia, result)
        if "não existe" == existencia:
            assert result is None, f"{entidade} {valor} existe na tabela {tabela}... {result}"
        else:
            assert result is not None, f"{entidade} {valor} não existe na tabela {tabela}... {result}"
            if entidade == "restaurante":
                context.restaurante_id = result['id']
            elif entidade == "pedido":
                context.pedido_id = result['id']
    finally:
        cursor.close()
        conn.close()

@given(u'eu sou o proprietário do "{entidade}" de id "{id_val}"')
def step_proprietario(context, entidade, id_val):
    context.proprietario_de = (entidade, int(id_val))

@given(u'estou autenticado no sistema')
def step_autenticado(context):
    context.autenticado = True

@given(u'o "{entidade}" cujo "id" é "{id_val}" está "{status}"')
def step_verificar_status_entidade(context, entidade, id_val, status):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT status FROM {entidade}s WHERE id = %s"
    cursor.execute(query, (int(id_val),))
    result = cursor.fetchone()
    assert result is not None
    assert result['status'].lower() == status.lower()
    cursor.close()
    conn.close()

@given(u'eu recebo uma requisição do sistema informando "{mensagem}" com id "{id_val}"')
def step_receber_notificacao(context, mensagem, id_val):
    context.notificacao = {"mensagem": mensagem, "id": int(id_val)}

# @when(u'eu envio uma requisição ao endpoint de "{endpoint}" com os dados')
@when(u'eu envio uma requisição ao endpoint de "{endpoint}" com os dados:')
def step_enviar_requisicao(context, endpoint):
    data = {}
    if context.table:
        row = context.table[0]
        for heading in context.table.headings:
            val = row[heading]
            if heading in ["id", "id_pedido", "id_restaurante"]:
                try:
                    data[heading] = int(val)
                except ValueError:
                    data[heading] = val
            else:
                data[heading] = val

    if endpoint == "cadastro de restaurante":
        url = f"{BASE_URL}/restaurantes/cadastrar"
        context.response = requests.post(url, json=data)
    elif endpoint == "edição de restaurante":
        rest_id = data.get('id') or getattr(context, 'restaurante_id', 123)
        url = f"{BASE_URL}/restaurantes/atualizar/{rest_id}"
        context.response = requests.put(url, json=data)
    elif endpoint == "remoção de restaurante":
        rest_id = data.get('id')
        url = f"{BASE_URL}/restaurantes/remover/{rest_id}"
        context.response = requests.delete(url)

@when(u'eu envio um requisição de ao endpoint "{endpoint}" com os dados:')
def step_enviar_requisicao_pedido(context, endpoint):
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

@when(u'o horário atual está "{posicao}" do intervalo de "funcionamento do restaurante" "{nome}":')
def step_horario_atual(context, posicao, nome):
    conn = get_db_connection()
    cursor = conn.cursor()
    agora = datetime.now()
    if posicao == "dentro":
        novo_horario = "00:00-23:59"
    else:
        uma_hora_atras = (agora.replace(hour=(agora.hour - 1) % 24)).strftime("%H:%M")
        uma_hora_atras_mais_um = (agora.replace(hour=(agora.hour - 1) % 24, minute=(agora.minute + 1) % 60)).strftime("%H:%M")
        novo_horario = f"{uma_hora_atras}-{uma_hora_atras_mais_um}"

    cursor.execute("UPDATE restaurantes SET horario = %s WHERE nome = %s", (novo_horario, nome))
    conn.commit()
    cursor.close()
    conn.close()
    
    url = f"{BASE_URL}/restaurantes/status"
    requests.post(url)

@then(u'o sistema deve registrar o {entidade} "{valor}" na tabela "{tabela}" do banco de dados')
def step_verificar_registro(context, entidade, valor, tabela):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM {tabela} WHERE nome = %s"
    cursor.execute(query, (valor,))
    result = cursor.fetchone()
    assert result is not None, f"{entidade} {valor} não registrado"
    cursor.close()
    conn.close()

@then(u'o sistema responde com o código HTTP "{status_code}"')
def step_verificar_status_http(context, status_code):
    assert context.response.status_code == int(status_code), \
        f"Esperado {status_code}, mas obteve {context.response.status_code}. Resposta: {context.response.text}"

@then(u'o sistema deve atualizar o "{entidade}" de id "{id_val}" com o novo "{campo}" para "{valor}" na tabela "{tabela}" do banco de dados')
def step_verificar_atualizacao(context, entidade, id_val, campo, valor, tabela):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM {tabela} WHERE id = %s"
    cursor.execute(query, (int(id_val),))
    result = cursor.fetchone()
    assert result is not None, f"{entidade} com id {id_val} não encontrado"
    
    actual_value = result.get(campo)
    if campo == "id_restaurante":
        assert int(actual_value) == int(valor)
    else:
        assert str(actual_value) == str(valor)
        
    cursor.close()
    conn.close()

@then(u'o restaurante "{valor}" deve estar "{status_proposta}" para criar propostas')
def step_disponibilidade_propostas(context, valor, status_proposta):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        id_val = int(valor)
        query = "SELECT * FROM restaurantes WHERE id = %s"
        cursor.execute(query, (id_val,))
    except ValueError:
        query = "SELECT * FROM restaurantes WHERE nome = %s"
        cursor.execute(query, (valor,))
        
    result = cursor.fetchone()
    if status_proposta == "disponível":
        assert result is not None
    else:
        assert result is None
    cursor.close()
    conn.close()

@then(u'o sistema deve remover o restaurante "{id_val}" na tabela "{tabela}" do banco de dados')
def step_verificar_remocao(context, id_val, tabela):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT * FROM {tabela} WHERE id = %s"
    cursor.execute(query, (int(id_val),))
    result = cursor.fetchone()
    assert result is None, f"Restaurante {id_val} ainda existe na tabela {tabela}"
    cursor.close()
    conn.close()

@then(u'o sistema deve atualizar o "restaurante" cujo "id" é "123" com o novo "nome" para "Gosto Muito Bom" na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "restaurante" cujo "id" é "123" com o novo "nome" para "Gosto Muito Bom" na tabela "restaurantes" do banco de dados')


@given(u'que o "restaurante" cujo "id" é "123" está "aberto"')
def step_impl(context):
    raise StepNotImplementedError(u'Given que o "restaurante" cujo "id" é "123" está "aberto"')


@then(u'o sistema deve atualizar o "pedido" cujo "id" é "987" com o novo "status" para "Em preparo" na tabela "pedidos" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "pedido" cujo "id" é "987" com o novo "status" para "Em preparo" na tabela "pedidos" do banco de dados')


@then(u'o sistema deve atualizar o "pedido" cujo "id" é "987" com o novo "id_restaurante" para "123" na tabela "pedidos" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "pedido" cujo "id" é "987" com o novo "id_restaurante" para "123" na tabela "pedidos" do banco de dados')


@then(u'o sistema deve atualizar o "pedido" cujo "id" é "987" com o novo "status" para "Rejeitado" na tabela "pedidos" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "pedido" cujo "id" é "987" com o novo "status" para "Rejeitado" na tabela "pedidos" do banco de dados')


@then(u'o sistema deve atualizar o "restaurante" cujo "id" é "123" com o novo "status" para "Fechado" na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "restaurante" cujo "id" é "123" com o novo "status" para "Fechado" na tabela "restaurantes" do banco de dados')


@then(u'o sistema deve atualizar o "restaurante" cujo "id" é "123" com o novo "status" para "Aberto" na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "restaurante" cujo "id" é "123" com o novo "status" para "Aberto" na tabela "restaurantes" do banco de dados')
