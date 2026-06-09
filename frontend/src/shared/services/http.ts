export async function requestJson<T>(
  input: RequestInfo | URL,
  init?: RequestInit,
  token?: string | null,
): Promise<T> {
  const headers = new Headers(init?.headers)
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }
  const response = await fetch(input, { ...init, headers })
  if (!response.ok) {
    throw new Error('Request failed')
  }
  return response.json() as Promise<T>
}
