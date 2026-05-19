from core.conexao_banco import ConexaoBanco
import mysql.connector
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RestauranteControle:
    
    @staticmethod
    def cadastrar_restaurante(dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Validação de campos obrigatórios
            campos_obrigatorios = ['nome', 'endereco', 'cnpj', 'horario', 'tipo']
            for campo in campos_obrigatorios:
                if not dados.get(campo):
                    return {"erro": f"Campo {campo} é obrigatório", "status_code": 400}

            # Verificar se nome já existe
            cursor.execute("SELECT id FROM restaurantes WHERE nome = %s", (dados['nome'],))
            if cursor.fetchone():
                return {"erro": "Restaurante com este nome já existe", "status_code": 400}

            # Verificar se CNPJ já existe
            cursor.execute("SELECT id FROM restaurantes WHERE cnpj = %s", (dados['cnpj'],))
            if cursor.fetchone():
                return {"erro": "Restaurante com este CNPJ já existe", "status_code": 400}

            # Inserir restaurante
            query = """
                INSERT INTO restaurantes (nome, endereco, cnpj, horario, tipo, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (dados['nome'], dados['endereco'], dados['cnpj'], dados['horario'], dados['tipo'], 'Fechado')
            cursor.execute(query, valores)
            conn.commit()
            
            restaurante_id = cursor.lastrowid
            return {"mensagem": "Restaurante cadastrado com sucesso", "id": restaurante_id, "status_code": 201}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao cadastrar restaurante", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_restaurante(restaurante_id: int, dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Verificar se o restaurante existe
            cursor.execute("SELECT * FROM restaurantes WHERE id = %s", (restaurante_id,))
            restaurante = cursor.fetchone()
            if not restaurante:
                return {"erro": "Restaurante não encontrado", "status_code": 404}

            # Bloquear edição de CNPJ (Regra de negócio BDD)
            if 'cnpj' in dados:
                return {"erro": "Edição de CNPJ não permitida", "status_code": 400}

            # Construir query dinamicamente
            campos = []
            valores = []
            for campo, valor in dados.items():
                if campo in ['nome', 'endereco', 'horario', 'tipo', 'status']:
                    campos.append(f"{campo} = %s")
                    valores.append(valor)
            
            if not campos:
                return {"erro": "Nenhum campo válido para atualização fornecido", "status_code": 400}

            valores.append(restaurante_id)
            query = f"UPDATE restaurantes SET {', '.join(campos)} WHERE id = %s"
            
            cursor.execute(query, tuple(valores))
            conn.commit()
            
            return {"mensagem": "Restaurante atualizado com sucesso", "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao atualizar restaurante", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def gerenciar_pedido(pedido_id: int, restaurante_id: int, aceitacao: str):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Verifica se o restaurante existe e está aberto
            cursor.execute("SELECT status FROM restaurantes WHERE id = %s", (restaurante_id,))
            restaurante = cursor.fetchone()
            if not restaurante:
                return {"erro": "Restaurante não encontrado", "status_code": 404}
            
            # Embora o BDD não exija erro se fechado aqui, é uma boa prática. 
            # Mas vamos seguir o BDD: "o restaurante 123 está aberto" no background.
            # Ajuste, implementar se o restaurante estiver fechado, nao aceitar pedido

            novo_status = "Em preparo" if aceitacao == "aceito" else "Rejeitado"
            
            # Atualizar pedido
            query = "UPDATE pedidos SET status = %s, id_restaurante = %s WHERE id = %s"
            cursor.execute(query, (novo_status, restaurante_id, pedido_id))
            conn.commit()
            
            return {"mensagem": f"Pedido {novo_status.lower()} com sucesso", "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao gerenciar pedido", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def verificar_horarios_e_atualizar_status():
        """Lógica para abertura/fechamento automático baseada no horário atual"""
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, nome, horario, status FROM restaurantes")
            restaurantes = cursor.fetchall()
            
            agora = datetime.now().time()
            hora_atual_str = agora.strftime("%H:%M")

            for rest in restaurantes:
                horario_func = rest['horario'] # Ex: "08:00-22:00"
                try:
                    inicio_str, fim_str = horario_func.split('-')
                    inicio = datetime.strptime(inicio_str, "%H:%M").time()
                    fim = datetime.strptime(fim_str, "%H:%M").time()

                    esta_aberto = False
                    if inicio <= fim:
                        esta_aberto = inicio <= agora <= fim
                    else: # Horário que vira a noite
                        esta_aberto = agora >= inicio or agora <= fim

                    novo_status = "Aberto" if esta_aberto else "Fechado"
                    
                    if rest['status'] != novo_status:
                        cursor.execute("UPDATE restaurantes SET status = %s WHERE id = %s", (novo_status, rest['id']))
                        logger.info(f"Status do restaurante {rest['nome']} alterado para {novo_status} automaticamente.")
                except Exception as e:
                    logger.error(f"Erro ao processar horário do restaurante {rest['id']}: {e}")
            
            conn.commit()
        except mysql.connector.Error as err:
            logger.error(f"Erro ao verificar horários: {err}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_restaurantes(args: dict = None):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM restaurantes"
            valores = []

            if args:
                filtros = []
                for campo, valor in args.items():
                    if valor is not None:
                        filtros.append(f"{campo} = %s")
                        valores.append(valor)
                
                if filtros:
                    query += " WHERE " + " AND ".join(filtros)

            cursor.execute(query, tuple(valores))
            restaurantes = cursor.fetchall()
            return {"restaurantes": restaurantes, "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao listar restaurantes: {err}")
            return {"erro": "Erro interno ao listar restaurantes", "status_code": 500}
        finally:
            cursor.close()
            conn.close()
