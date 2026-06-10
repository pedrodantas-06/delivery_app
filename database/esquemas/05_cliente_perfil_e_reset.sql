SET NAMES utf8mb4;

USE yummicious_db;

-- Perfil do cliente: dados pessoais que ficam na tabela de perfil (clientes),
-- enquanto a autenticação (senha/role) vive em `usuarios`.
ALTER TABLE clientes
    ADD COLUMN cpf VARCHAR(14) NULL UNIQUE,
    ADD COLUMN telefone VARCHAR(20) NULL;

-- Tokens de recuperação de senha ("esqueci a senha").
-- Guardamos apenas o hash do token (nunca o token em claro).
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    token_hash VARCHAR(64) NOT NULL,
    expira_em TIMESTAMP NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_reset_token_hash (token_hash)
);
