import Loading from './Loading'

function LoadingState({ label = 'Processando...' }: { label?: string }) {
  return (
    <div className="loading-state" role="status" aria-live="polite">
      <Loading label={label} />
    </div>
  )
}

export default LoadingState
