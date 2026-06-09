import json
import logging

import mysql.connector

from core.conexao_banco import ConexaoBanco

logger = logging.getLogger(__name__)


class PedidoControle:
    @staticmethod
    def criar(dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            itens = dados.get("itens", [])
            if not itens:
                return {"erro": "Pedido deve conter ao menos um item", "status_code": 400}

            valor_total = sum(
                float(item["preco"]) * int(item["quantidade"]) for item in itens
            )

            detalhes = json.dumps(
                {
                    "itens": itens,
                    "endereco_entrega": dados.get("endereco_entrega"),
                },
                ensure_ascii=False,
            )

            query = """
                INSERT INTO pedidos (id_restaurante, status, cliente_id, valor_total, detalhes)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (
                dados["id_restaurante"],
                "Pendente",
                dados["cliente_id"],
                valor_total,
                detalhes,
            )
            cursor.execute(query, valores)
            conn.commit()

            pedido_id = cursor.lastrowid
            return {
                "id": pedido_id,
                "status": "Pendente",
                "valor_total": valor_total,
                "mensagem": "Pedido criado com sucesso",
                "status_code": 201,
            }

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao criar pedido", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_cliente(cliente_id: str):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM pedidos WHERE cliente_id = %s ORDER BY id DESC",
                (cliente_id,),
            )
            pedidos = cursor.fetchall()
            return {"pedidos": pedidos, "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao listar pedidos", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_todos():
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
            pedidos = cursor.fetchall()
            return {"pedidos": pedidos, "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao listar pedidos", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_restaurante(restaurante_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM pedidos WHERE id_restaurante = %s ORDER BY id DESC",
                (restaurante_id,),
            )
            pedidos = cursor.fetchall()
            return {"pedidos": pedidos, "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao listar pedidos", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obter(pedido_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM pedidos WHERE id = %s", (pedido_id,))
            pedido = cursor.fetchone()
            if not pedido:
                return {"erro": "Pedido não encontrado", "status_code": 404}
            return {"pedido": pedido, "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao obter pedido", "status_code": 500}
        finally:
            cursor.close()
            conn.close()
