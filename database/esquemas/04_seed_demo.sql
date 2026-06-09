SET NAMES utf8mb4;

USE yummicious_db;

-- Senha bcrypt de "123456" (gerado via scripts/generate_seed_hash.py)
SET @demo_senha = '$2b$12$u8sc6scl1FXhv8gNAaFgVuW4j3GZ1FMAoN.dVs.gY/uuqx.f4O3Ki';

-- Usuarios demo
INSERT INTO usuarios (nome, email, senha, role, referencia_id) VALUES
('Cliente Demo', 'cliente@yummicious.com', @demo_senha, 'CLIENTE', 'cli_demo_001'),
('Burger House', 'burger@burgerhouse.com', @demo_senha, 'RESTAURANTE', '1'),
('Entregador Demo', 'entregador@yummicious.com', @demo_senha, 'ENTREGADOR', 'del_demo_001'),
('Admin Demo', 'admin@yummicious.com', @demo_senha, 'ADMIN', NULL)
ON DUPLICATE KEY UPDATE nome = VALUES(nome), senha = VALUES(senha);

INSERT INTO clientes (id, nome, email, saldo) VALUES
('cli_demo_001', 'Cliente Demo', 'cliente@yummicious.com', 0.00)
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

-- Restaurantes (3)
INSERT INTO restaurantes (id, nome, endereco, cnpj, horario, tipo, status, usuario_id) VALUES
(1, 'Burger House', 'Bloco A, Campus Central', '11.111.111/0001-11', '08:00-22:00', 'Lanches', 'Aberto', 2),
(2, 'Pizza Campus', 'Bloco B, Campus Central', '22.222.222/0001-22', '10:00-23:00', 'Pizza', 'Aberto', NULL),
(3, 'Açaí Federal', 'Bloco C, Campus Central', '33.333.333/0001-33', '09:00-21:00', 'Açaí', 'Aberto', NULL)
ON DUPLICATE KEY UPDATE
    nome = VALUES(nome),
    endereco = VALUES(endereco),
    cnpj = VALUES(cnpj),
    horario = VALUES(horario),
    tipo = VALUES(tipo),
    status = VALUES(status),
    usuario_id = VALUES(usuario_id);

-- Cardápio Burger House (5 itens)
INSERT INTO cardapio (nome, descricao, preco, categoria, id_restaurante) VALUES
('X-Burguer', 'Hambúrguer clássico', 25.00, 'Lanches', 1),
('X-Salada', 'Hambúrguer vegetariano', 28.00, 'Lanches', 1),
('Batata Frita', 'Porção média', 12.00, 'Acompanhamentos', 1),
('Coca-Cola 350ml', 'Refrigerante', 8.00, 'Bebidas', 1),
('Milkshake', 'Morango', 18.00, 'Bebidas', 1)
ON DUPLICATE KEY UPDATE preco = VALUES(preco);

-- Cardápio Pizza Campus (5 itens)
INSERT INTO cardapio (nome, descricao, preco, categoria, id_restaurante) VALUES
('Margherita', 'Molho, mussarela, manjericão', 45.00, 'Pizzas', 2),
('Calabresa', 'Calabresa e cebola', 42.00, 'Pizzas', 2),
('4 Queijos', 'Mussarela, gorgonzola, parmesão, catupiry', 48.00, 'Pizzas', 2),
('Guaraná 350ml', 'Refrigerante', 7.00, 'Bebidas', 2),
('Brownie', 'Com sorvete', 15.00, 'Sobremesas', 2)
ON DUPLICATE KEY UPDATE preco = VALUES(preco);

-- Cardápio Açaí Federal (5 itens)
INSERT INTO cardapio (nome, descricao, preco, categoria, id_restaurante) VALUES
('Açaí 300ml', 'Com granola', 16.00, 'Açaí', 3),
('Açaí 500ml', 'Com banana', 22.00, 'Açaí', 3),
('Granola Extra', 'Porção', 3.00, 'Adicionais', 3),
('Banana Extra', 'Unidade', 2.00, 'Adicionais', 3),
('Água 500ml', 'Sem gás', 4.00, 'Bebidas', 3)
ON DUPLICATE KEY UPDATE preco = VALUES(preco);

-- Pedidos demo (4 estados)
INSERT INTO pedidos (id, id_restaurante, status, cliente_id, valor_total, detalhes) VALUES
(1001, 1, 'Finalizado', 'cli_demo_001', 33.00, '{"itens":[{"nome":"X-Burguer","preco":25,"quantidade":1},{"nome":"Coca-Cola 350ml","preco":8,"quantidade":1}]}'),
(1002, 1, 'Em preparo', 'cli_demo_001', 25.00, '{"itens":[{"nome":"X-Burguer","preco":25,"quantidade":1}]}'),
(1003, 2, 'Pago', 'cli_demo_001', 45.00, '{"itens":[{"nome":"Margherita","preco":45,"quantidade":1}]}'),
(1004, 3, 'Cancelado', 'cli_demo_001', 16.00, '{"itens":[{"nome":"Açaí 300ml","preco":16,"quantidade":1}]}')
ON DUPLICATE KEY UPDATE status = VALUES(status);
