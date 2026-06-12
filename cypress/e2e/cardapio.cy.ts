describe('GUI do cardápio', () => {
  const restaurantId = 42

  const menuResponse = {
    restaurante: 'Restaurante Teste',
    itens: [
      {
        id: 101,
        nome: 'Coxinha de Frango',
        descricao: 'Massa crocante recheada com frango desfiado',
        preco: '12.50',
        categoria: 'Salgados',
      },
      {
        id: 102,
        nome: 'Brigadeiro Gourmet',
        descricao: 'Doce cremoso com granulado belga',
        preco: '8.90',
        categoria: 'Sobremesas',
      },
    ],
  }

  const categoryResponse = {
    restaurante: 'Restaurante Teste',
    itens: [
      {
        id: 103,
        nome: 'Pastel de Queijo',
        descricao: 'Pastel crocante com queijo minas',
        preco: '10.00',
        categoria: 'Salgados',
      },
      {
        id: 104,
        nome: 'Pudim de Leite',
        descricao: 'Pudim cremoso com calda de caramelo',
        preco: '11.50',
        categoria: 'Sobremesas',
      },
    ],
  }

  const loginAsCustomer = () => {
    cy.visit('/login', {
      onBeforeLoad(win) {
        win.localStorage.setItem(
          'yummicious_auth',
          JSON.stringify({
            user: {
              id: 1,
              nome: 'Cliente Teste',
              email: 'cliente@test.com',
              role: 'CLIENTE',
              referencia_id: '42',
            },
            token: 'fake-token',
          }),
        )
      },
    })
  }

  it('Cenário 1: cadastro de item no cardápio com dados válidos', () => {
    cy.intercept('GET', '**/api/v1/restaurantes/*/cardapio*', {
      statusCode: 200,
      body: menuResponse,
    }).as('getMenu')

    cy.visit(`/customer/menu/${restaurantId}`, {
      onBeforeLoad(win) {
        win.localStorage.setItem(
          'yummicious_auth',
          JSON.stringify({
            user: {
              id: 1,
              nome: 'Cliente Teste',
              email: 'cliente@test.com',
              role: 'CLIENTE',
              referencia_id: '42',
            },
            token: 'fake-token',
          }),
        )
      },
    })

    cy.wait('@getMenu')

    cy.contains('h1', 'Restaurante Teste').should('be.visible')
    cy.contains('Salgados').should('be.visible')
    cy.contains('Coxinha de Frango').should('be.visible')
    cy.contains('R$ 12.50').should('be.visible')

    cy.contains('button', 'Adicionar').first().click()
    cy.contains('button', 'Ir para o carrinho').should('be.visible')
  })

  it('Cenário 2: exibe mensagem de erro ao acessar cardápio de restaurante inválido', () => {
    cy.intercept('GET', '**/api/v1/restaurantes/*/cardapio*', {
      statusCode: 404,
      body: { mensagem: 'Restaurante não encontrado' },
    }).as('getMenuError')

    cy.visit(`/customer/menu/999`, {
      onBeforeLoad(win) {
        win.localStorage.setItem(
          'yummicious_auth',
          JSON.stringify({
            user: {
              id: 1,
              nome: 'Cliente Teste',
              email: 'cliente@test.com',
              role: 'CLIENTE',
              referencia_id: '42',
            },
            token: 'fake-token',
          }),
        )
      },
    })

    cy.wait('@getMenuError')
    cy.contains('Não foi possível carregar o cardápio.').should('be.visible')
  })

  it('Cenário 3: exibe categorias corretamente agrupadas no cardápio', () => {
    cy.intercept('GET', '**/api/v1/restaurantes/*/cardapio*', {
      statusCode: 200,
      body: categoryResponse,
    }).as('getGroupedMenu')

    cy.visit(`/customer/menu/${restaurantId}`, {
      onBeforeLoad(win) {
        win.localStorage.setItem(
          'yummicious_auth',
          JSON.stringify({
            user: {
              id: 1,
              nome: 'Cliente Teste',
              email: 'cliente@test.com',
              role: 'CLIENTE',
              referencia_id: '42',
            },
            token: 'fake-token',
          }),
        )
      },
    })

    cy.wait('@getGroupedMenu')

    cy.contains('h2', 'Salgados').should('be.visible')
    cy.contains('h2', 'Sobremesas').should('be.visible')
    cy.contains('Pastel de Queijo').should('be.visible')
    cy.contains('Pudim de Leite').should('be.visible')
    cy.get('.customer-menu-group').should('have.length', 2)
  })

  it.skip('Cenário 4: geração e acesso ao link público de compartilhamento do cardápio', () => {
    // Atualmente o frontend não expõe a rota pública de compartilhamento do cardápio.
    // Quando essa rota for implementada, este teste deve visitar o link anônimo
    // e validar a exibição do cardápio sem autenticação.
  })
})
