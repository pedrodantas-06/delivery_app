from django.db import models

class MetodoPagamento(models.Model):
    cliente_id = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20)
    token_cartao = models.CharField(max_length=200)
    ultimos_4_digitos = models.CharField(max_length=4)
    nome_titular = models.CharField(max_length=100)
    validade_mes = models.IntegerField()
    validade_ano = models.IntegerField()
    padrao = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

class Cupom(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=20)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    ativo = models.BooleanField(default=True)

class TransacaoPagamento(models.Model):
    pedido_id = models.CharField(max_length=100)
    cliente_id = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    criado_em = models.DateTimeField(auto_now_add=True)