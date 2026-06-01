from core.conexao_banco import ConexaoBanco
import mysql.connector
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CardapioControle:
    
    @staticmethod
    def cadastrar_item(dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Validação de campos obrigatórios
            campos_obrigatorios = ['nome', 'descricao', 'preco', 'categoria', 'id_restaurante']
            for campo in campos_obrigatorios:
                if not dados.get(campo):
                    return {"erro": f"Campo {campo} é obrigatório", "status_code": 400}

            # Validar que o restaurante existe
            cursor.execute("SELECT id FROM restaurantes WHERE id = %s", (dados['id_restaurante'],))
            if not cursor.fetchone():
                return {"erro": "Restaurante não encontrado", "status_code": 404}

            # Verificar se o item já existe no cardápio do restaurante
            cursor.execute(
                "SELECT id FROM cardapio WHERE nome = %s AND id_restaurante = %s", 
                (dados['nome'], dados['id_restaurante'])
            )
            if cursor.fetchone():
                return {"erro": "Item com este nome já existe neste cardápio", "status_code": 400}

            # Validar preço
            try:
                preco = float(dados['preco'])
                if preco < 0:
                    return {"erro": "Preço não pode ser negativo", "status_code": 400}
            except ValueError:
                return {"erro": "Preço deve ser um número válido", "status_code": 400}

            # Inserir item no cardápio
            query = """
                INSERT INTO cardapio (nome, descricao, preco, categoria, id_restaurante, disponivel, criado_em)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            disponivel = dados.get('disponivel', True)
            valores = (
                dados['nome'], 
                dados['descricao'], 
                preco, 
                dados['categoria'], 
                dados['id_restaurante'], 
                disponivel,
                datetime.now()
            )
            cursor.execute(query, valores)
            conn.commit()
            
            item_id = cursor.lastrowid
            return {
                "mensagem": "Item cadastrado com sucesso", 
                "id": item_id, 
                "status_code": 201
            }

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao cadastrar item", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_cardapio(filtros: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM cardapio WHERE 1=1"
            valores = []

            # Aplicar filtros
            if 'id_restaurante' in filtros:
                query += " AND id_restaurante = %s"
                valores.append(filtros['id_restaurante'])
            
            if 'categoria' in filtros:
                query += " AND categoria = %s"
                valores.append(filtros['categoria'])
            
            if 'disponivel' in filtros:
                query += " AND disponivel = %s"
                valores.append(filtros['disponivel'])

            if 'nome' in filtros:
                query += " AND nome LIKE %s"
                valores.append(f"%{filtros['nome']}%")

            query += " ORDER BY criado_em DESC"

            cursor.execute(query, tuple(valores))
            itens = cursor.fetchall()

            return {
                "itens": itens,
                "total": len(itens),
                "status_code": 200
            }

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao listar cardápio", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obter_item(item_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM cardapio WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            
            if not item:
                return {"erro": "Item não encontrado", "status_code": 404}

            return {"item": item, "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao obter item", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_item(item_id: int, dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Verificar se o item existe
            cursor.execute("SELECT * FROM cardapio WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            if not item:
                return {"erro": "Item não encontrado", "status_code": 404}

            # Validar preço se fornecido
            if 'preco' in dados:
                try:
                    preco = float(dados['preco'])
                    if preco < 0:
                        return {"erro": "Preço não pode ser negativo", "status_code": 400}
                    dados['preco'] = preco
                except ValueError:
                    return {"erro": "Preço deve ser um número válido", "status_code": 400}

            # Construir query dinamicamente
            campos = []
            valores = []
            for campo, valor in dados.items():
                if campo in ['nome', 'descricao', 'preco', 'categoria', 'disponivel']:
                    campos.append(f"{campo} = %s")
                    valores.append(valor)
            
            if not campos:
                return {"erro": "Nenhum campo válido para atualização fornecido", "status_code": 400}

            # Adicionar timestamp de atualização
            campos.append("atualizado_em = %s")
            valores.append(datetime.now())
            valores.append(item_id)

            query = f"UPDATE cardapio SET {', '.join(campos)} WHERE id = %s"
            
            cursor.execute(query, tuple(valores))
            conn.commit()
            
            return {"mensagem": "Item atualizado com sucesso", "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao atualizar item", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deletar_item(item_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Verificar se o item existe
            cursor.execute("SELECT * FROM cardapio WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            if not item:
                return {"erro": "Item não encontrado", "status_code": 404}

            # Deletar item
            cursor.execute("DELETE FROM cardapio WHERE id = %s", (item_id,))
            conn.commit()
            
            return {"mensagem": "Item deletado com sucesso", "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao deletar item", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obter_cardapio_por_restaurante(restaurante_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Verificar se o restaurante existe
            cursor.execute("SELECT * FROM restaurantes WHERE id = %s", (restaurante_id,))
            restaurante = cursor.fetchone()
            if not restaurante:
                return {"erro": "Restaurante não encontrado", "status_code": 404}

            # Obter cardápio do restaurante
            cursor.execute(
                "SELECT * FROM cardapio WHERE id_restaurante = %s ORDER BY categoria, nome",
                (restaurante_id,)
            )
            itens = cursor.fetchall()

            return {
                "restaurante": restaurante['nome'],
                "itens": itens,
                "total": len(itens),
                "status_code": 200
            }

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao obter cardápio", "status_code": 500}
        finally:
            cursor.close()
            conn.close()
