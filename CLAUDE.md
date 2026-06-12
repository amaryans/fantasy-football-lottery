# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fantasy Football Lottery is a PyQt5 desktop application that runs a weighted draft lottery for fantasy football leagues. Owners are assigned lottery chances inversely proportional to their previous season record, then each winner selects their preferred draft position via a GUI.

## Commands

```bash
# Run the application
python main.py

# Install dependencies
pip install -r build/requirements.txt

# Build standalone executable (Windows)
cd build && build.bat

# Build standalone executable (cross-platform)
cd build && python build.py
```

Built executable outputs to `dist/FantasyFootballLottery/FantasyFootballLottery.exe`.

## Architecture

**Entry point:** `main.py` — creates `MainWindow(QMainWindow)` which orchestrates the lottery flow.

**Core modules:**

- **`lottery/`** — Simulation engine. `LotterySim` generates weighted chances from team records (worst record = most chances). `Simulator` implements the combinatorial lottery algorithm using 4-ball combinations mapped to team seeds via a hash table.
- **`config/`** — `ConfigManager` is a **singleton** that loads/saves `config/league_config.json`. All modules access league data (owners, records, images, league name) through this singleton. `styles.py` contains all QSS stylesheet constants (primary color: `#013369` navy blue).
- **`widgets/`** — PyQt5 UI components communicating via **signal/slot pattern**:
  - `LotteryWindowWidget` emits `next_pick_clicked` → `MainWindow` runs lottery pick
  - `DraftPickSelectorWidget` emits `pick_confirmed(position, owner_name)` → `MainWindow` updates draft order
  - `ConfigWidget` opens as a separate window from Settings menu (Ctrl+,)

**Data flow:** ConfigManager loads JSON → LotterySim generates pick order → UI reveals picks one-by-one → each winner selects draft position → DraftOrderWidget updates.

## Key Files

- `config/league_config.json` — League configuration (owners, records, images, league name)
- `config/styles.py` — Centralized QSS stylesheets for all widgets
- `build/fantasy_football_lottery.spec` — PyInstaller spec for executable builds
- `data/` — Images (league logos, owner photos)

## Dependencies

Python 3.8+, PyQt5, numpy, pandas, PyInstaller (build only). Defined in `build/requirements.txt`.

## Notes

- No test suite exists currently.
- The app window defaults to 1920x1080.
- File paths in the codebase use relative paths (e.g., `./config/`, `./data/`), so the app must be run from the project root.
