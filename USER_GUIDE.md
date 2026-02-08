# Fantasy Football Lottery - User Guide

## Installation

### Running the Executable (Recommended)

1. Extract the `FantasyFootballLottery` folder to your desired location
2. Double-click `FantasyFootballLottery.exe` to start the application
3. No Python installation required!

### Running from Source

If you have Python installed:
```bash
python main.py
```

## First Time Setup

When you first launch the application:

1. Go to **Settings → Configuration** (or press `Ctrl+,`)
2. Configure your league:
   - Enter your league name
   - Set the number of teams
   - Add your league logo (optional)
   - Add all owners and their team information

3. Click **Save** to apply changes
4. Restart the application for changes to take effect

## Using the Application

### Main Screen

The application consists of several sections:

1. **Header** - Displays your league name and logo
2. **Draft Order** - Shows the draft positions as they're selected
3. **Standings** - Displays team standings from the previous season
4. **Lottery Window** - Shows the current pick and owner being selected
5. **Draft Pick Selector** - Buttons to select draft positions

### Running the Lottery

1. Click **"Begin Lottery"** to start
2. The lottery will randomly select an owner
3. The selected owner can choose their draft position using the numbered buttons
4. Click **"Confirm"** to lock in the selection
5. Click **"Next Pick"** to continue to the next owner
6. Repeat until all draft positions are filled

### Configuration Menu

Access via **Settings → Configuration** or press `Ctrl+,`:

- **League Name**: Your fantasy league's name
- **Number of Teams**: Automatically adjusts based on owners added
- **League Logo**: Path to your league logo image
- **Owners Table**:
  - Owner: Owner's name
  - Team Name: Their team name
  - Record: Previous season record (affects lottery odds)
  - Owner Image Path: Path to owner's photo (optional)

### Import/Export Configuration

**Exporting:**
1. Open Configuration (`Ctrl+,`)
2. Click **"Export Config"**
3. Choose a location and filename
4. Save as `.json` file

**Importing:**
1. Open Configuration (`Ctrl+,`)
2. Click **"Import Config"**
3. Select your previously exported `.json` file
4. Click **"Save"** to apply

This is useful for:
- Backing up your configuration
- Sharing configuration with others
- Switching between different leagues

## Configuration File

The application stores settings in `config/league_config.json`:

```json
{
  "league_name": "Your League Name",
  "number_of_teams": 12,
  "logo_path": "./data/logo.png",
  "owners": [
    {
      "owner": "Owner Name",
      "team_name": "Team Name",
      "record": "10-4",
      "image_path": "./data/owner.jpg"
    }
  ]
}
```

You can edit this file directly with a text editor if needed.

## Tips

- **Lottery Odds**: Teams with worse records get better lottery odds
- **Images**: Place logo and owner images in the `data/` folder
- **Backup**: Export your configuration regularly
- **Testing**: Use "Import Config" to test different league setups

## Keyboard Shortcuts

- `Ctrl+,` - Open Configuration

## Troubleshooting

**Application won't start:**
- Ensure the entire folder was copied (not just the .exe)
- Check that `config/` and `data/` folders exist

**Configuration not saving:**
- Check write permissions for the application folder
- Try running as administrator (right-click → Run as administrator)

**Missing images:**
- Verify image paths in the configuration
- Ensure images are in the correct location
- Use relative paths starting with `./data/`

**Changes not appearing:**
- Restart the application after changing configuration
- Check that you clicked "Save" in the configuration window

## Advanced Usage

### Custom Images

1. Add your images to the `data/` folder
2. In Configuration, set the path: `./data/your_image.png`
3. Supported formats: PNG, JPG, JPEG, GIF, BMP

### Multiple Leagues

You can manage multiple leagues by:
1. Exporting each league's configuration
2. Importing the appropriate config when needed
3. Or keeping separate application folders for each league

## Support

For issues or questions:
- Check this guide
- Review the BUILD_README.md for technical details
- Check the configuration file syntax

## Version

Current Version: 1.0

---

Enjoy your draft lottery! 🏈
