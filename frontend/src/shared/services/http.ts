export async function requestJson<T>(input: RequestInfo | URL, init?: RequestInit): Promise<T> {
  const response = await fetch(input, init)
  if (!response.ok) {
    throw new Error('Request failed')
  }
  return response.json() as Promise<T>
}
