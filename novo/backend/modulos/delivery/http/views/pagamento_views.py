#TO-DO from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from modulos.delivery.infrastructure.models.pagamento_model import MetodoPagamento, Cupom, TransacaoPagamento
from datetime import datetime

class MetodosPagamentoView(APIView):
    def get(self, request):
        cliente_id = request.headers.get('X-Cliente-ID')
        metodos = MetodoPagamento.objects.filter(cliente_id=cliente_id)
        data = [{'id': m.id, 'tipo': m.tipo, 'ultimos_4_digitos': m.ultimos_4_digitos} for m in metodos]
        return Response({'metodos': data})

    def post(self, request):
        cliente_id = request.headers.get('X-Cliente-ID')
        dados = request.data
        
        # Validação básica
        if not dados.get('numero_cartao'):
            return Response({'erro': 'Número do cartão é obrigatório'}, status=400)
        
        # Criar método
        metodo = MetodoPagamento.objects.create(
            cliente_id=cliente_id,
            tipo=dados.get('tipo'),
            token_cartao=f"tok_{dados.get('numero_cartao')[-4:]}",
            ultimos_4_digitos=dados.get('numero_cartao')[-4:],
            nome_titular=dados.get('nome_titular'),
            validade_mes=dados.get('validade_mes'),
            validade_ano=dados.get('validade_ano'),
            padrao=dados.get('padrao', False)
        )
        
        return Response({'id': metodo.id, 'mensagem': 'Método adicionado'}, status=201)

class MetodoPagamentoDetailView(APIView):
    def delete(self, request, metodo_id):
        cliente_id = request.headers.get('X-Cliente-ID')
        metodo = MetodoPagamento.objects.get(id=metodo_id, cliente_id=cliente_id)
        
        # Não pode remover o único método
        if MetodoPagamento.objects.filter(cliente_id=cliente_id).count() <= 1:
            return Response({'erro': 'Não pode remover único método'}, status=400)
        
        metodo.delete()
        return Response(status=204)

    def put(self, request, metodo_id):
        cliente_id = request.headers.get('X-Cliente-ID')
        metodo = MetodoPagamento.objects.get(id=metodo_id, cliente_id=cliente_id)
        
        if 'validade_mes' in request.data:
            metodo.validade_mes = request.data['validade_mes']
        if 'validade_ano' in request.data:
            metodo.validade_ano = request.data['validade_ano']
        metodo.save()
        
        return Response({'mensagem': 'Atualizado com sucesso'})

class AplicarCupomView(APIView):
    def post(self, request):
        cupom_codigo = request.data.get('cupom_codigo')
        valor_pedido = float(request.data.get('valor_pedido', 0))
        
        try:
            cupom = Cupom.objects.get(codigo=cupom_codigo, ativo=True)
        except Cupom.DoesNotExist:
            return Response({'valido': False, 'erro': 'Cupom inválido'}, status=422)
        
        # Calcular desconto
        desconto = 0
        if cupom.tipo == 'PERCENTUAL':
            desconto = valor_pedido * (cupom.valor / 100)
        elif cupom.tipo == 'FIXO':
            desconto = float(cupom.valor)
        
        return Response({
            'valido': True,
            'desconto': desconto,
            'valor_final': valor_pedido - desconto
        })

class ProcessarPagamentoView(APIView):
    def post(self, request, pedido_id):
        cliente_id = request.headers.get('X-Cliente-ID')
        metodo_id = request.data.get('metodo_pagamento_id')
        valor = float(request.data.get('valor_pedido', 0))
        
        transacao = TransacaoPagamento.objects.create(
            pedido_id=pedido_id,
            cliente_id=cliente_id,
            valor=valor,
            status='APROVADO'
        )
        
        return Response({
            'transacao_id': transacao.id,
            'status': 'APROVADO',
            'valor_pago': valor
        })

class EstornarPagamentoView(APIView):
    def post(self, request, pedido_id):
        cliente_id = request.headers.get('X-Cliente-ID')
        
        try:
            transacao = TransacaoPagamento.objects.get(pedido_id=pedido_id, cliente_id=cliente_id)
        except TransacaoPagamento.DoesNotExist:
            return Response({'erro': 'Transação não encontrada'}, status=404)
        
        transacao.status = 'ESTORNADO'
        transacao.save()
        
        return Response({
            'estorno_id': f'est_{transacao.id}',
            'valor_estornado': transacao.valor,
            'mensagem': 'Estorno realizado'
        })

class ComprovanteView(APIView):
    def get(self, request, pedido_id):
        cliente_id = request.headers.get('X-Cliente-ID')
        
        try:
            transacao = TransacaoPagamento.objects.get(pedido_id=pedido_id, cliente_id=cliente_id)
        except TransacaoPagamento.DoesNotExist:
            return Response({'erro': 'Transação não encontrada'}, status=404)
        
        return Response({
            'pedido_id': pedido_id,
            'valor_pago': transacao.valor,
            'status': transacao.status,
            'data': transacao.criado_em
        })