import { defineFeature, loadFeature } from 'jest-cucumber'

type DelivererStatus = 'AVAILABLE' | 'OCCUPIED' | 'OFFLINE'

type Deliverer = {
  name: string
  phone: string
  region: string
  status: DelivererStatus
}

const feature = loadFeature('./tests/deliverer.feature')

class DelivererStore {
  private deliverers: Deliverer[] = []

  clear() {
    this.deliverers = []
  }

  create(deliverer: Omit<Deliverer, 'status'>): Deliverer {
    const created: Deliverer = { ...deliverer, status: 'AVAILABLE' }
    this.deliverers.push(created)
    return created
  }
}

defineFeature(feature, (test) => {
  let store: DelivererStore
  let response: Deliverer | undefined

  beforeEach(() => {
    store = new DelivererStore()
    response = undefined
  })

  test('cadastrar entregador com sucesso', ({ given, when, then }) => {
    given('nenhum entregador existe', () => {
      store.clear()
    })

    when(
      'eu cadastro um entregador com nome "Ana" telefone "11999999999" regiao "Zona Sul"',
      () => {
        response = store.create({
          name: 'Ana',
          phone: '11999999999',
          region: 'Zona Sul',
        })
      },
    )

    then('o entregador "Ana" deve ficar com status "AVAILABLE"', () => {
      expect(response?.status).toBe('AVAILABLE')
    })
  })
})