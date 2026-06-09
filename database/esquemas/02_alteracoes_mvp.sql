SET NAMES utf8mb4;

USE yummicious_db;

-- USUÁRIOS (autenticação unificada por role)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    role ENUM('CLIENTE', 'RESTAURANTE', 'ENTREGADOR', 'ADMIN') NOT NULL,
    referencia_id VARCHAR(50) NULL COMMENT 'cliente_id, restaurante_id ou deliverer_uuid',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CARDÁPIO
CREATE TABLE IF NOT EXISTS cardapio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    id_restaurante INT NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id),
    UNIQUE KEY uk_cardapio_nome_rest (nome, id_restaurante)
);

-- Vínculo restaurante ↔ usuário operador
-- Init scripts rodam uma vez em volume vazio; ALTER simples é suficiente aqui.
ALTER TABLE restaurantes
    ADD COLUMN usuario_id INT NULL;

-- Ampliar status de pedido (Pago, Cancelado) para fluxo MVP
ALTER TABLE pedidos
    MODIFY COLUMN status ENUM(
        'Pendente', 'Pago', 'Em preparo', 'Rejeitado',
        'Finalizado', 'Cancelado'
    ) DEFAULT 'Pendente';
