describe('GUI de entregadores', () => {
  it('cadastra um entregador e atualiza a lista', () => {
    const deliverers = [
      {
        id: '1',
        name: 'Ana',
        phone: '11999999999',
        region: 'Zona Sul',
        status: 'AVAILABLE',
      },
    ]

    cy.intercept('GET', '/api/deliverers/**', (req) => {
      req.reply({ items: deliverers })
    }).as('loadDeliverers')

    cy.intercept('POST', '/api/deliverers/', (req) => {
      deliverers.splice(0, deliverers.length, {
        id: '1',
        name: req.body.name,
        phone: req.body.phone,
        region: req.body.region,
        status: 'AVAILABLE',
      })

      req.reply({
        id: '1',
        name: req.body.name,
        phone: req.body.phone,
        region: req.body.region,
        status: 'AVAILABLE',
      })
    }).as('createDeliverer')

    cy.visit('/')
    cy.wait('@loadDeliverers')

    cy.get('[data-cy="register-deliverer"]').within(() => {
      cy.get('[data-cy="deliverer-name"]').type('Ana')
      cy.get('[data-cy="deliverer-phone"]').type('11999999999')
      cy.get('[data-cy="deliverer-region"]').type('Zona Sul')
      cy.get('[data-cy="submit-deliverer"]').click()
    })

    cy.wait('@createDeliverer')
    cy.contains('Ana').should('be.visible')
  })
})