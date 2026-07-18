import { useAppStore } from './state/store.ts'
import SetupScreen from './screens/SetupScreen.tsx'
import LeagueReviewScreen from './screens/LeagueReviewScreen.tsx'
import ConfigScreen from './screens/ConfigScreen.tsx'
import EventScreen from './screens/EventScreen.tsx'
import ResultsScreen from './screens/ResultsScreen.tsx'

export default function App() {
  const phase = useAppStore((state) => state.phase)

  switch (phase) {
    case 'setup':
      return <SetupScreen />
    case 'review':
      return <LeagueReviewScreen />
    case 'config':
      return <ConfigScreen />
    case 'event':
      return <EventScreen />
    case 'results':
      return <ResultsScreen />
  }
}
