export interface Restaurant {
  id: number
  nome: string
  endereco: string
  horario: string
  tipo: string
  status: string
}

export interface MenuItem {
  id: number
  nome: string
  descricao: string
  preco: number
  categoria: string
  id_restaurante: number
  disponivel: boolean | number
}

export interface MenuResponse {
  restaurante: string
  itens: MenuItem[]
  total: number
}

export interface CartItem {
  id: number
  nome: string
  preco: number
  quantidade: number
}

export interface Order {
  id: number
  id_restaurante: number
  status: string
  cliente_id: string
  valor_total: number
  detalhes: string | Record<string, unknown>
}

export interface CreateOrderPayload {
  id_restaurante: number
  cliente_id: string
  itens: { nome: string; preco: number; quantidade: number }[]
  endereco_entrega: string
}

export interface CreateOrderResponse {
  id: number
  status: string
  valor_total: number
  mensagem: string
}
