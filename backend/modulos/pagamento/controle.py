from core.conexao_banco import ConexaoBanco
import mysql.connector
from datetime import datetime
import logging
from uuid import uuid5, NAMESPACE_URL

from modulos.delivery.wires import deliverer_service
from modulos.pagamento.mock_gateway import MockPaymentGateway

logger = logging.getLogger(__name__)

class PagamentoControle:

    @staticmethod
    async def processar_pagamento(pedido_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id, status, valor_total
                FROM pedidos
                WHERE id = %s
            """, (pedido_id,))
            pedido = cursor.fetchone()

            if not pedido:
                return {"erro": "Pedido não encontrado", "status_code": 404}

            if pedido["status"] != "Pendente":
                return {"erro": "Pedido não está pendente", "status_code": 400}

            resultado_gateway = await MockPaymentGateway.processar(
                float(pedido["valor_total"])
            )

            cursor.execute("""
                INSERT INTO transacoes (pedido_id, tipo, valor, status)
                VALUES (%s, %s, %s, %s)
            """, (
                pedido_id,
                "PAGAMENTO",
                pedido["valor_total"],
                "PROCESSADO",
            ))

            cursor.execute("""
                UPDATE pedidos SET status = 'Pago'
                WHERE id = %s
            """, (pedido_id,))

            conn.commit()

            order_uuid = uuid5(NAMESPACE_URL, str(pedido_id))
            try:
                deliverer_service.assign_deliverer(order_uuid, "Zona Sul", None)
            except ValueError:
                pass  # no deliverer available — pedido stays Pago

            return {
                "pedido_id": pedido_id,
                "status": "Pago",
                "transaction_id": resultado_gateway["transaction_id"],
                "status_code": 200,
            }

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco: {err}")
            conn.rollback()
            return {"erro": "Erro interno ao processar pagamento", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def processar_estorno(pedido_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT p.*, c.id as cliente_id, c.saldo 
                FROM pedidos p
                JOIN clientes c ON p.cliente_id = c.id
                WHERE p.id = %s
            """, (pedido_id,))
            pedido = cursor.fetchone()
            
            if not pedido:
                return {"erro": "Pedido não encontrado", "status_code": 404}
            
            if pedido['status'] == 'Em preparo':
                return {
                    "erro": "Pedido não pode ser cancelado após aceite do restaurante",
                    "status_code": 400
                }
            
            if pedido['status'] != 'Pago':
                return {"erro": "Pedido não está pago", "status_code": 400}
            
            cursor.execute("""
                INSERT INTO transacoes (pedido_id, tipo, valor, status)
                VALUES (%s, %s, %s, %s)
            """, (pedido_id, 'ESTORNO', pedido['valor_total'], 'PROCESSADO'))
            
            novo_saldo = float(pedido['saldo']) + float(pedido['valor_total'])
            cursor.execute("""
                UPDATE clientes SET saldo = %s WHERE id = %s
            """, (novo_saldo, pedido['cliente_id']))
            
            cursor.execute("""
                UPDATE pedidos SET status = 'Cancelado'
                WHERE id = %s
            """, (pedido_id,))
            
            conn.commit()
            
            return {
                "mensagem": "Estorno processado com sucesso",
                "pedido_id": pedido_id,
                "valor_estornado": float(pedido['valor_total']),
                "saldo_atual": novo_saldo,
                "status_code": 200
            }
            
        except mysql.connector.Error as err:
            logger.error(f"Erro no banco: {err}")
            conn.rollback()
            return {"erro": "Erro interno ao processar estorno", "status_code": 500}
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def criar_metodo(cliente_id: str, dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id FROM clientes WHERE id = %s", (cliente_id,))
            if not cursor.fetchone():
                return {"erro": "Cliente não encontrado", "status_code": 404}
            
            ano_atual = datetime.now().year
            mes_atual = datetime.now().month
            
            if dados['validade_ano'] < ano_atual or (
                dados['validade_ano'] == ano_atual and dados['validade_mes'] < mes_atual
            ):
                return {"erro": "Data de validade expirada", "status_code": 422}
            
            cursor.execute("""
                INSERT INTO metodos_pagamento 
                (cliente_id, tipo, ultimos_4_digitos, nome_titular, validade_mes, validade_ano)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                cliente_id,
                dados['tipo'],
                dados['numero'][-4:],
                dados['nome_titular'],
                dados['validade_mes'],
                dados['validade_ano']
            ))
            
            conn.commit()
            metodo_id = cursor.lastrowid
            
            return {
                "mensagem": "Método de pagamento criado com sucesso",
                "id": metodo_id,
                "status_code": 201
            }
            
        except mysql.connector.Error as err:
            logger.error(f"Erro no banco: {err}")
            conn.rollback()
            return {"erro": "Erro interno", "status_code": 500}
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def atualizar_metodo(metodo_id: int, cliente_id: str, dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT * FROM metodos_pagamento 
                WHERE id = %s AND cliente_id = %s
            """, (metodo_id, cliente_id))
            metodo = cursor.fetchone()
            
            if not metodo:
                return {"erro": "Método não encontrado", "status_code": 404}
            
            if 'validade_ano' in dados and 'validade_mes' in dados:
                ano_atual = datetime.now().year
                mes_atual = datetime.now().month
                
                if dados['validade_ano'] < ano_atual or (
                    dados['validade_ano'] == ano_atual and dados['validade_mes'] < mes_atual
                ):
                    return {"erro": "Data de validade expirada", "status_code": 422}
            
            campos = []
            valores = []
            for campo, valor in dados.items():
                if campo in ['validade_mes', 'validade_ano']:
                    campos.append(f"{campo} = %s")
                    valores.append(valor)
            
            if not campos:
                return {"erro": "Nenhum campo válido", "status_code": 400}
            
            valores.append(metodo_id)
            valores.append(cliente_id)
            query = f"""
                UPDATE metodos_pagamento 
                SET {', '.join(campos)}, atualizado_em = NOW()
                WHERE id = %s AND cliente_id = %s
            """
            
            cursor.execute(query, tuple(valores))
            conn.commit()
            
            return {"mensagem": "Método atualizado", "status_code": 200}
            
        except mysql.connector.Error as err:
            logger.error(f"Erro no banco: {err}")
            conn.rollback()
            return {"erro": "Erro interno", "status_code": 500}
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def remover_metodo(metodo_id: int, cliente_id: str):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT * FROM metodos_pagamento 
                WHERE id = %s AND cliente_id = %s
            """, (metodo_id, cliente_id))
            metodo = cursor.fetchone()
            
            if not metodo:
                return {"erro": "Método não encontrado", "status_code": 404}
            
            cursor.execute("""
                DELETE FROM metodos_pagamento 
                WHERE id = %s AND cliente_id = %s
            """, (metodo_id, cliente_id))
            
            conn.commit()
            
            return {"status_code": 204}
            
        except mysql.connector.Error as err:
            logger.error(f"Erro no banco: {err}")
            conn.rollback()
            return {"erro": "Erro interno", "status_code": 500}
        finally:
            cursor.close()
            conn.close()