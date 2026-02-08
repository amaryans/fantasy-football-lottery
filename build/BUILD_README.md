# Building Fantasy Football Lottery Application

This guide explains how to build the Fantasy Football Lottery application as a standalone executable.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Quick Start

### Option 1: Using the Build Script (Recommended)

**Windows:**
```bash
cd build
build.bat
```

**Cross-platform:**
```bash
cd build
python build.py
```

The scripts automatically handle paths and work from the project root.

### Option 2: Manual Build

From the project root directory:

1. **Install dependencies:**
   ```bash
   pip install -r build/requirements.txt
   ```

2. **Build the executable:**
   ```bash
   pyinstaller build/fantasy_football_lottery.spec --clean
   ```

## Output

After building, you'll find:
- **Executable:** `dist/FantasyFootballLottery/FantasyFootballLottery.exe`
- **Distribution folder:** `dist/FantasyFootballLottery/`

The entire `FantasyFootballLottery` folder needs to be distributed together as it contains all necessary dependencies and resources.

## Distribution

To distribute the application:

1. Copy the entire `dist/FantasyFootballLottery/` folder
2. Share it with users
3. Users can run `FantasyFootballLottery.exe` without installing Python

### Creating a ZIP Archive

```bash
# Windows PowerShell
Compress-Archive -Path dist\FantasyFootballLottery -DestinationPath FantasyFootballLottery-v1.0.zip

# Or using 7-Zip, WinRAR, etc.
```

## File Structure

```
dist/FantasyFootballLottery/
├── FantasyFootballLottery.exe    # Main executable
├── config/                        # Configuration files
│   ├── league_config.json        # League settings
│   └── ...
├── data/                          # Images and data
│   └── ...
├── _internal/                     # Python runtime and dependencies
└── ...
```

## Configuration

The application uses `config/league_config.json` for settings. Users can:
- Use the built-in Configuration menu (Settings → Configuration)
- Manually edit `league_config.json`
- Import/Export configuration files

## Troubleshooting

### Build Fails

**Error: "Python is not installed"**
- Ensure Python 3.8+ is installed and in your PATH
- Try: `python --version` to verify

**Error: "PyInstaller not found"**
- Run: `pip install pyinstaller`

**Error: "Module not found"**
- Run: `pip install -r requirements.txt`

### Runtime Issues

**Application won't start:**
- Make sure the entire folder is copied (not just the .exe)
- Check that config/ and data/ folders exist
- Try running from command line to see error messages

**Missing configuration:**
- The app will create default `league_config.json` on first run
- Check the config/ folder exists

## Advanced Options

### Adding an Icon

1. Create or obtain an `.ico` file (256x256 recommended)
2. Save it as `app_icon.ico` in the project root
3. Edit `fantasy_football_lottery.spec`:
   ```python
   exe = EXE(
       ...
       icon='app_icon.ico',  # Update this line
       ...
   )
   ```
4. Rebuild: `pyinstaller fantasy_football_lottery.spec --clean`

### Creating a Single-File Executable

Edit `fantasy_football_lottery.spec` and change:
```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,      # Add these three lines
    a.zipfiles,      #
    a.datas,         #
    [],
    name='FantasyFootballLottery',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)
```

Then remove the `COLLECT` section and rebuild.

### Reducing Size

- Use `upx=True` in the spec file (already enabled)
- Exclude unnecessary packages in the spec file
- Consider using `--onefile` mode (single executable, but slower startup)

## Creating an Installer (Optional)

For a professional installer, use Inno Setup:

1. Download Inno Setup: https://jrsoftware.org/isdl.php
2. Create a script (`installer.iss`):

```inno
[Setup]
AppName=Fantasy Football Lottery
AppVersion=1.0
DefaultDirName={pf}\Fantasy Football Lottery
DefaultGroupName=Fantasy Football Lottery
OutputDir=installer_output
OutputBaseFilename=FantasyFootballLottery-Setup

[Files]
Source: "dist\FantasyFootballLottery\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Fantasy Football Lottery"; Filename: "{app}\FantasyFootballLottery.exe"
Name: "{commondesktop}\Fantasy Football Lottery"; Filename: "{app}\FantasyFootballLottery.exe"
```

3. Compile with Inno Setup to create `FantasyFootballLottery-Setup.exe`

## Support

For issues or questions:
- Check the main README.md
- Review error messages in the console
- Ensure all dependencies are installed

## Version History

- **v1.0** - Initial release with configuration management and lottery simulation
