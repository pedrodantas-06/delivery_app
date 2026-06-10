import { requestJson } from '../../../shared/services/http'

const API_BASE = '/api/v1'

export interface RegisterPayload {
  nome: string
  email: string
  cpf: string
  telefone: string
  senha: string
}

export interface RegisterResponse {
  mensagem: string
  cliente_id: string
}

export interface ForgotPasswordResponse {
  mensagem: string
  // Presente apenas em modo dev (sem envio real de e-mail).
  token?: string
}

export async function registerCliente(payload: RegisterPayload) {
  return requestJson<RegisterResponse>(`${API_BASE}/clientes/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export async function forgotPassword(email: string) {
  return requestJson<ForgotPasswordResponse>(`${API_BASE}/auth/forgot-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  })
}

export async function resetPassword(token: string, novaSenha: string) {
  return requestJson<{ mensagem: string }>(`${API_BASE}/auth/reset-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token, nova_senha: novaSenha }),
  })
}
