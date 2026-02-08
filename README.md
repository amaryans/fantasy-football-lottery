# Fantasy Football Lottery

A professional draft lottery simulator for fantasy football leagues, built with PyQt5.

## Features

- 🎲 **Lottery Simulation** - Weighted lottery based on previous season records
- 📊 **Interactive Draft Selection** - Visual interface for selecting draft positions
- ⚙️ **Configuration Management** - Easy-to-use settings interface
- 💾 **Import/Export** - Save and share league configurations
- 🎨 **Customizable** - Add league logos and owner images
- 📦 **Standalone Executable** - No Python installation required for end users

## Quick Start

### For Users

See [USER_GUIDE.md](USER_GUIDE.md) for complete instructions on using the application.

### For Developers

#### Running from Source
```bash
python main.py
```

#### Building Executable
```bash
cd build
build.bat       # Windows
python build.py # Cross-platform
```

See [build/BUILD_README.md](build/BUILD_README.md) for detailed build instructions.

## Project Structure

```
fantasy-football-lottery/
├── main.py                    # Application entry point
├── config/                    # Configuration files
│   ├── config_manager.py     # JSON config handler
│   ├── league_config.json    # League settings
│   └── styles.py             # Centralized stylesheets
├── widgets/                   # UI components
│   ├── config_widget.py      # Configuration interface
│   ├── draft_order_widget.py # Draft order display
│   ├── standings_widget.py   # Standings table
│   └── ...
├── lottery/                   # Lottery simulation logic
│   ├── lottery.py            # Main lottery class
│   └── lottery_simulator.py  # Simulation engine
├── data/                      # Images and resources
├── build/                     # Build scripts and config
│   ├── build.bat             # Windows build script
│   ├── build.py              # Cross-platform build
│   ├── requirements.txt      # Python dependencies
│   └── BUILD_README.md       # Build documentation
├── USER_GUIDE.md             # End-user documentation
└── README.md                 # This file
```

## Requirements

- Python 3.8+
- PyQt5
- numpy
- pandas

Install dependencies:
```bash
pip install -r build/requirements.txt
```

## Configuration

The application uses JSON-based configuration stored in `config/league_config.json`:

- League name and settings
- Team information
- Owner records and images
- League logo

Configuration can be managed through:
- Built-in GUI (Settings → Configuration)
- Direct JSON file editing
- Import/Export functionality

## Building for Distribution

To create a standalone executable:

1. Navigate to the build directory:
   ```bash
   cd build
   ```

2. Run the build script:
   ```bash
   build.bat       # Windows
   python build.py # Cross-platform
   ```

3. Find the executable:
   ```
   dist/FantasyFootballLottery/FantasyFootballLottery.exe
   ```

See [build/BUILD_README.md](build/BUILD_README.md) for advanced build options.

## Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user guide for end users
- **[build/BUILD_README.md](build/BUILD_README.md)** - Build instructions and distribution
- **[build/README.md](build/README.md)** - Quick reference for building

## License

MIT License - Feel free to use and modify for your fantasy league!

## Version

Current Version: 1.0
