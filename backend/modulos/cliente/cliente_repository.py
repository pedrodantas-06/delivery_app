from core.conexao_banco import ConexaoBanco
import mysql.connector


class ClienteRepository:

    def __init__(self):
        self.conn = ConexaoBanco.get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def buscar_por_email(self, email):
        self.cursor.execute(
            "SELECT id, nome, email, senha, role FROM clientes WHERE email = %s",
            (email,)
        )
        return self.cursor.fetchone()

    def buscar_por_cpf(self, cpf):
        self.cursor.execute(
            "SELECT id FROM clientes WHERE cpf = %s",
            (cpf,)
        )
        return self.cursor.fetchone()

    def buscar_por_id(self, cliente_id):
        self.cursor.execute(
            "SELECT id FROM clientes WHERE id = %s",
            (cliente_id,)
        )
        return self.cursor.fetchone()

    def inserir_cliente(self, valores):
        query = """
            INSERT INTO clientes (nome, email, cpf, telefone, senha, role)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    def listar(self, filtros=None):
        query = "SELECT id, nome, email, telefone FROM clientes"
        valores = []

        if filtros:
            clausulas = []
            for campo, valor in filtros.items():
                clausulas.append(f"{campo} = %s")
                valores.append(valor)

            if clausulas:
                query += " WHERE " + " AND ".join(clausulas)

        self.cursor.execute(query, tuple(valores))
        return self.cursor.fetchall()

    def atualizar(self, cliente_id, campos, valores):
        set_clause = ", ".join([f"{campo} = %s" for campo in campos])
        query = f"UPDATE clientes SET {set_clause} WHERE id = %s"

        valores.append(cliente_id)

        self.cursor.execute(query, tuple(valores))
        self.conn.commit()

    def deletar(self, cliente_id):
        query = "DELETE FROM clientes WHERE id = %s"
        self.cursor.execute(query, (cliente_id,))
        self.conn.commit()

    def fechar(self):
        self.cursor.close()
        self.conn.close()