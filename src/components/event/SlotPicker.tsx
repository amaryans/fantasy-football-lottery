import type { Team } from '../../data/types.ts'
import Button from '../common/Button.tsx'

interface SlotPickerProps {
  team: Team
  totalSlots: number
  takenSlots: ReadonlySet<number>
  onPick: (slot: number) => void
}

export default function SlotPicker({ team, totalSlots, takenSlots, onPick }: SlotPickerProps) {
  return (
    <div className="flex w-full max-w-xs flex-col gap-3 rounded-2xl border border-white/15 bg-white/5 p-4">
      <p className="text-center text-sm text-white/70">
        <span className="font-semibold text-white">{team.teamName}</span> — choose your draft slot
      </p>
      <div className="grid grid-cols-4 gap-2">
        {Array.from({ length: totalSlots }, (_, i) => i + 1).map((slot) => {
          const isTaken = takenSlots.has(slot)
          return (
            <Button
              key={slot}
              variant={isTaken ? 'ghost' : 'secondary'}
              disabled={isTaken}
              aria-label={`Draft slot ${slot}`}
              className="px-0 py-2 text-center tabular-nums"
              onClick={() => onPick(slot)}
            >
              {slot}
            </Button>
          )
        })}
      </div>
    </div>
  )
}
