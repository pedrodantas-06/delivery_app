Feature: Cardápio do aplicativo de delivery

  Permite que cada restaurante possua seu próprio cardápio, contendo itens com nome, preço e descrição opcional. 
  Cada item pertence a uma única categoria. 
  O cardápio pode ser acessado por meio de um link público e persistente, não sendo necessário login para visualização.

Cenário baseado em GUI
	Cenário: submissão bem-sucedida da autoavaliação

	Dado que estou na página "Avaliação"
	E consigo ver a lista de metas com os conceitos atribuídos pelo professor
	E consigo ver os botões "Select" com campos de autoavaliação vazios para todas as metas
	Quando clico no botão "Select" da meta "Entender conceitos de requisitos"
	E seleciono o conceito "MA"
	E clico no botão "Select" da meta "Especificar requisitos com qualidade"
	E seleciono o conceito "MPA"
	E clico no botão "Select" da meta "Entender conceitos de gerência de configuração"
	E seleciono o conceito "MA"
	E clico no botão "Envie"
	Então sou redirecionado para a página de confirmação de envio
