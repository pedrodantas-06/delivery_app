Feature: Cardápio do aplicativo de delivery

  Permite que cada restaurante possua seu próprio cardápio, contendo itens com nome, preço e descrição opcional. 
  Cada item pertence a uma única categoria. 
  O cardápio pode ser acessado por meio de um link público e persistente, não sendo necessário login para visualização.

Cenário 1 – Cadastro de item no cardápio com dados válidos O responsável pelo restaurante acessa a área de gerenciamento do cardápio e preenche o formulário de novo item com nome, preço e, opcionalmente, descrição. Ao confirmar, o item aparece listado no cardápio do restaurante. O cenário valida o fluxo feliz de adição de um item.

Cenário 2 – Tentativa de cadastro de item com dados inválidos ou incompletos O responsável tenta cadastrar um item deixando o nome em branco ou inserindo um preço negativo/zero. O sistema deve exibir mensagens de erro adequadas e impedir o cadastro. O cenário valida as regras de validação do formulário.