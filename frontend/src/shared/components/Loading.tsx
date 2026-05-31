function Loading({ label = 'Carregando...' }: { label?: string }) {
  return <p className="loading">{label}</p>
}

export default Loading
