from core.conexao_banco import ConexaoBanco


class ClienteRepository:
    """
    Repositório unificado de clientes.

    A identidade/autenticação fica em `usuarios` (id INT, senha, role, referencia_id)
    e o perfil de negócio fica em `clientes` (id VARCHAR, cpf, telefone, ...).
    O vínculo entre as duas é `usuarios.referencia_id = clientes.id`.
    """

    def __init__(self):
        self.conn = ConexaoBanco.get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    def buscar_usuario_por_email(self, email):
        self.cursor.execute(
            "SELECT id, nome, email, senha, role, referencia_id "
            "FROM usuarios WHERE email = %s",
            (email,),
        )
        return self.cursor.fetchone()

    def buscar_cliente_por_cpf(self, cpf):
        self.cursor.execute(
            "SELECT id FROM clientes WHERE cpf = %s",
            (cpf,),
        )
        return self.cursor.fetchone()

    def buscar_usuario_por_id(self, usuario_id):
        self.cursor.execute(
            "SELECT id, referencia_id FROM usuarios WHERE id = %s",
            (usuario_id,),
        )
        return self.cursor.fetchone()

    def buscar_perfil(self, usuario_id):
        """Perfil completo (usuário + cliente) para a tela 'meus dados'."""
        self.cursor.execute(
            """
            SELECT u.id, u.nome, u.email, u.role, u.referencia_id,
                   c.cpf, c.telefone, c.saldo
            FROM usuarios u
            LEFT JOIN clientes c ON u.referencia_id = c.id
            WHERE u.id = %s
            """,
            (usuario_id,),
        )
        return self.cursor.fetchone()

    def listar(self, filtros=None):
        query = "SELECT id, nome, email, telefone, cpf FROM clientes"
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

    def estatisticas_pedidos(self, cliente_id):
        """Quantidade total, quantidade no mês corrente e preço médio dos pedidos."""
        self.cursor.execute(
            """
            SELECT
                COUNT(*) AS total,
                COALESCE(SUM(
                    YEAR(criado_em) = YEAR(CURDATE())
                    AND MONTH(criado_em) = MONTH(CURDATE())
                ), 0) AS no_mes,
                COALESCE(AVG(valor_total), 0) AS preco_medio
            FROM pedidos
            WHERE cliente_id = %s
            """,
            (cliente_id,),
        )
        return self.cursor.fetchone()

    # ------------------------------------------------------------------
    # Escrita (transações entre as duas tabelas)
    # ------------------------------------------------------------------
    def cadastrar(self, cliente_id, nome, email, cpf, telefone, senha_hash):
        try:
            self.cursor.execute(
                "INSERT INTO clientes (id, nome, email, cpf, telefone) "
                "VALUES (%s, %s, %s, %s, %s)",
                (cliente_id, nome, email, cpf, telefone),
            )
            self.cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, role, referencia_id) "
                "VALUES (%s, %s, %s, 'CLIENTE', %s)",
                (nome, email, senha_hash, cliente_id),
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def atualizar(self, usuario_id, referencia_id, dados_usuario, dados_cliente):
        try:
            if dados_usuario:
                campos = ", ".join(f"{c} = %s" for c in dados_usuario)
                self.cursor.execute(
                    f"UPDATE usuarios SET {campos} WHERE id = %s",
                    (*dados_usuario.values(), usuario_id),
                )

            if dados_cliente and referencia_id:
                campos = ", ".join(f"{c} = %s" for c in dados_cliente)
                self.cursor.execute(
                    f"UPDATE clientes SET {campos} WHERE id = %s",
                    (*dados_cliente.values(), referencia_id),
                )

            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def deletar(self, usuario_id, referencia_id):
        try:
            self.cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            if referencia_id:
                self.cursor.execute(
                    "DELETE FROM clientes WHERE id = %s", (referencia_id,)
                )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def fechar(self):
        self.cursor.close()
        self.conn.close()
