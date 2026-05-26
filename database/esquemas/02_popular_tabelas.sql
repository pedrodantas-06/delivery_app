SET NAMES utf8mb4;

USE yummicious_db;

-- RESTAURANTES
INSERT INTO restaurantes (id, nome, endereco, cnpj, horario, tipo, status) VALUES
(1, 'Restaurante Teste', 'Rua Teste, 123', '00.000.000/0001-00', '10:00-22:00', 'Teste', 'Aberto')
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

-- CLIENTES
INSERT INTO clientes (id, nome, email, saldo) VALUES 
('cli_123', 'Ana Vitória', 'ana@email.com', 0.00)
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

-- PEDIDOS
INSERT INTO pedidos (id, id_restaurante, status, cliente_id, valor_total) VALUES
(123, 1, 'Pago', 'cli_123', 100.00)
ON DUPLICATE KEY UPDATE status = VALUES(status);

-- MÉTODOS DE PAGAMENTO (opcional)
INSERT INTO metodos_pagamento (cliente_id, tipo, ultimos_4_digitos, nome_titular, validade_mes, validade_ano) VALUES
('cli_123', 'CREDIT_CARD', '1111', 'ANA VITORIA', 12, 2028)
ON DUPLICATE KEY UPDATE tipo = VALUES(tipo);

-- Mostrar resultado
SELECT 'Banco recriado com sucesso!' as Status;
SELECT * FROM clientes;
SELECT * FROM pedidos;