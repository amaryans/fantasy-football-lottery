# Build Directory

This directory contains all files needed to build the Fantasy Football Lottery application as a standalone executable.

## Contents

- **`requirements.txt`** - Python dependencies for the application
- **`fantasy_football_lottery.spec`** - PyInstaller configuration file
- **`build.bat`** - Windows build script
- **`build.py`** - Cross-platform build script
- **`BUILD_README.md`** - Comprehensive build instructions and documentation

## Quick Build

### Windows
```bash
cd build
build.bat
```

### Cross-Platform
```bash
cd build
python build.py
```

## What Happens

The build scripts will:
1. Install dependencies from `requirements.txt`
2. Clean previous build artifacts
3. Run PyInstaller with the spec file
4. Create the executable in `dist/FantasyFootballLottery/`

## Output Location

After building, find your executable at:
```
../dist/FantasyFootballLottery/FantasyFootballLottery.exe
```

## More Information

See [BUILD_README.md](BUILD_README.md) for:
- Detailed build instructions
- Troubleshooting guide
- Advanced options (icons, installers, etc.)
- Distribution instructions
