import { Component, type ReactNode } from 'react'

const STORAGE_KEY = 'ffl.v1'

interface ErrorBoundaryProps {
  children: ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
}

/**
 * Last line of defense against a blank screen: if anything throws during
 * render (e.g. a corrupted persisted snapshot), show a recovery screen with
 * a way to wipe local data instead of white nothingness.
 */
export default class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false }

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true }
  }

  handleReset = (): void => {
    try {
      localStorage.removeItem(STORAGE_KEY)
    } catch {
      // Storage unavailable — reload alone may still recover.
    }
    window.location.reload()
  }

  render(): ReactNode {
    if (!this.state.hasError) {
      return this.props.children
    }
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-navy px-6 text-center text-white">
        <span className="text-5xl">🏈</span>
        <h1 className="text-2xl font-bold">Something went wrong</h1>
        <p className="max-w-md text-white/60">
          The app hit an unexpected error — usually stale saved data from an older version.
          Resetting clears this browser&apos;s saved league and lottery state.
        </p>
        <button
          type="button"
          className="cursor-pointer rounded-lg bg-accent px-6 py-2.5 font-semibold shadow-lg hover:bg-red-700"
          onClick={this.handleReset}
        >
          Reset and reload
        </button>
      </main>
    )
  }
}
