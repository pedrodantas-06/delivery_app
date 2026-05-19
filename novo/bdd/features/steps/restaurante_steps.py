from behave.api.pending_step import StepNotImplementedError
from behave import given, when, then
import requests
import mysql.connector

@given(u'que o endpoint de "{endpoint}" está "{status}"')
def step_endpoint_disponivel(context, endpoint, status):
    if endpoint == "cadastro de restaurante":
        context.endpoint = "http://localhost:8000/restaurantes"

    try:
        resposta = requests.get(context.endpoint)
        assert resposta.status_code == 200
    except requests.ConnectionError:
        raise AssertionError(f"A API falhou, o endpoint {endpoint} não está {status}!")

@given(u'que o "restaurante" cujo "nome" é "Gosto bom" não existe na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Given que o "restaurante" cujo "nome" é "Gosto bom" não existe na tabela "restaurantes" do banco de dados')


@when(u'eu envio uma requisição ao endpoint de "cadastro de restaurante" com os dados:')
def step_impl(context):
    raise StepNotImplementedError(u'When eu envio uma requisição ao endpoint de "cadastro de restaurante" com os dados:')


@then(u'o sistema deve registrar o restaurante "Gosto bom" na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve registrar o restaurante "Gosto bom" na tabela "restaurantes" do banco de dados')


@then(u'o restaurante "Gosto bom" deve estar disponível para criar propostas')
def step_impl(context):
    raise StepNotImplementedError(u'Then o restaurante "Gosto bom" deve estar disponível para criar propostas')


@then(u'o sistema responde com o código HTTP "201"')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema responde com o código HTTP "201"')


@then(u'o sistema responde com o código HTTP "400"')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema responde com o código HTTP "400"')


@given(u'que o "restaurante" cujo "nome" é "Gosto bom" existe na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Given que o "restaurante" cujo "nome" é "Gosto bom" existe na tabela "restaurantes" do banco de dados')


@given(u'que o "restaurante" cujo "cnpj" é "00.000.000/0001-00" existe na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Given que o "restaurante" cujo "cnpj" é "00.000.000/0001-00" existe na tabela "restaurantes" do banco de dados')


@given(u'que o endpoint de "edição de restaurante" está "disponível"')
def step_impl(context):
    raise StepNotImplementedError(u'Given que o endpoint de "edição de restaurante" está "disponível"')


@given(u'que eu sou o proprietário do "restaurante" de id "123"')
def step_impl(context):
    raise StepNotImplementedError(u'Given que eu sou o proprietário do "restaurante" de id "123"')


@given(u'o "restaurante" cujo "id" é "123" existe na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Given o "restaurante" cujo "id" é "123" existe na tabela "restaurantes" do banco de dados')


@when(u'eu envio uma requisição ao endpoint de "edição de restaurante" com os dados:')
def step_impl(context):
    raise StepNotImplementedError(u'When eu envio uma requisição ao endpoint de "edição de restaurante" com os dados:')


@then(u'o sistema deve atualizar o "restaurante" de id "123" com o novo "nome" para "Gosto Muito Bom" na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "restaurante" de id "123" com o novo "nome" para "Gosto Muito Bom" na tabela "restaurantes" do banco de dados')


@then(u'o sistema responde com o código HTTP "200"')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema responde com o código HTTP "200"')


@given(u'que o endpoint de "pedidos" está "disponível"')
def step_impl(context):
    raise StepNotImplementedError(u'Given que o endpoint de "pedidos" está "disponível"')


@given(u'eu sou o proprietário do restaurante de id "123"')
def step_impl(context):
    raise StepNotImplementedError(u'Given eu sou o proprietário do restaurante de id "123"')


@given(u'estou autenticado no sistema')
def step_impl(context):
    raise StepNotImplementedError(u'Given estou autenticado no sistema')


@given(u'o "pedido" cujo "id" é "987" existe na tabela "pedidos" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Given o "pedido" cujo "id" é "987" existe na tabela "pedidos" do banco de dados')


@given(u'o "restaurante" cujo "id" é "123" está "aberto"')
def step_impl(context):
    raise StepNotImplementedError(u'Given o "restaurante" cujo "id" é "123" está "aberto"')


@given(u'eu recebo uma requisição do sistema informando "novo pedido" com id "987"')
def step_impl(context):
    raise StepNotImplementedError(u'Given eu recebo uma requisição do sistema informando "novo pedido" com id "987"')


@when(u'eu envio um requisição de ao endpoint "pedidos" com os dados:')
def step_impl(context):
    raise StepNotImplementedError(u'When eu envio um requisição de ao endpoint "pedidos" com os dados:')


@then(u'o sistema deve atualizar o "pedido" de id "987" com o novo "status" para "Em preparo" na tabela "pedidos" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "pedido" de id "987" com o novo "status" para "Em preparo" na tabela "pedidos" do banco de dados')


@then(u'o sistema deve atualizar o "pedido" de id "987" com o novo "id_restaurante" para "123" na tabela "pedidos" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "pedido" de id "987" com o novo "id_restaurante" para "123" na tabela "pedidos" do banco de dados')


@then(u'o sistema deve atualizar o "pedido" de id "987" com o novo "status" para "Rejeitado" na tabela "pedidos" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "pedido" de id "987" com o novo "status" para "Rejeitado" na tabela "pedidos" do banco de dados')


@given(u'que o endpoint de "restaurantes" está "disponível"')
def step_impl(context):
    raise StepNotImplementedError(u'Given que o endpoint de "restaurantes" está "disponível"')


@when(u'o horário atual está "fora" do intervalo de "funcionamento do restaurante" "Gosto bom":')
def step_impl(context):
    raise StepNotImplementedError(u'When o horário atual está "fora" do intervalo de "funcionamento do restaurante" "Gosto bom":')


@then(u'o sistema deve atualizar o "restaurante" de id "123" com o novo "status" para "Fechado" na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "restaurante" de id "123" com o novo "status" para "Fechado" na tabela "restaurantes" do banco de dados')


@when(u'o horário atual está "dentro" do intervalo de "funcionamento do restaurante" "Gosto bom":')
def step_impl(context):
    raise StepNotImplementedError(u'When o horário atual está "dentro" do intervalo de "funcionamento do restaurante" "Gosto bom":')


@then(u'o sistema deve atualizar o "restaurante" de id "123" com o novo "status" para "Aberto" na tabela "restaurantes" do banco de dados')
def step_impl(context):
    raise StepNotImplementedError(u'Then o sistema deve atualizar o "restaurante" de id "123" com o novo "status" para "Aberto" na tabela "restaurantes" do banco de dados')
