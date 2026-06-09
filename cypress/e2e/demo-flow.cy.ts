const DEMO_PASSWORD = '123456'

const DEMO_USERS = [
  { role: 'cliente', email: 'cliente@yummicious.com', path: '/customer' },
  { role: 'restaurante', email: 'burger@burgerhouse.com', path: '/restaurant' },
  { role: 'entregador', email: 'entregador@yummicious.com', path: '/deliverer' },
  { role: 'admin', email: 'admin@yummicious.com', path: '/admin' },
] as const

function loginAs(email: string, password: string) {
  cy.visit('/login')
  cy.get('[data-cy=email]').clear().type(email)
  cy.get('[data-cy=password]').clear().type(password)
  cy.get('[data-cy=login-submit]').click()
}

describe('Demo MVP — login por role', () => {
  DEMO_USERS.forEach(({ role, email, path }) => {
    it(`login ${role} redireciona para ${path}`, () => {
      loginAs(email, DEMO_PASSWORD)
      cy.url().should('include', path)
    })
  })
})
