# Keyboard Shortcut Autocomplete Professional for NVDA

Version: 1.1.2  
Author: Mohammed Khaled Mahmoud <mohammed.khaled.mahmoud1996@gmail.com>  
License: GNU GPL v2

## Description

Keyboard Shortcut Autocomplete Professional is a powerful text expansion addon for NVDA that significantly enhances your typing productivity. Define custom abbreviations and expand them instantly into full text, saving time and reducing typing errors.

## Key Features

- **Smart Text Expansion**: Convert abbreviations into full text with a simple keystroke
- **Professional Manager Interface**: Intuitive dialog with search, import/export capabilities
- **Multi-language Support**: Works seamlessly with English, Arabic, and other languages
- **Live Expansion Hints**: Get real-time suggestions while typing
- **Undo Functionality**: Easily revert expansions if needed
- **Thread-Safe Operation**: Reliable performance even under heavy use
- **Customizable Shortcuts**: Create unlimited text shortcuts tailored to your needs

## Installation

1. Download the latest `.nvda-addon` file
2. Open the file with NVDA running
3. Follow the installation prompts
4. Restart NVDA to activate the addon

## Quick Start Guide

### Basic Usage

1. **Expand a shortcut**: Type your abbreviation and press `NVDA+E`
2. **Open manager**: Press `NVDA+Shift+K` to add, edit, or delete shortcuts
3. **Toggle addon**: Press `NVDA+Alt+Shift+K` to enable/disable

### Example Shortcuts

The addon comes with useful defaults:
- `ty` → "thank you"
- `brb` → "be right back"
- `asap` → "as soon as possible"
- `ISA` → "In Shaa Allah"
- `moh@` → "mohammed.khaled.mahmoud1996@gmail.com"

## Complete Keyboard Commands

| Command | Key | Description |
|---------|-----|-------------|
| Expand Shortcut | `NVDA+E` | Expands the abbreviation at cursor position |
| Open Manager | `NVDA+Shift+K` | Opens the shortcuts management dialog |
| Toggle Addon | `NVDA+Alt+Shift+K` | Enables or disables the addon |
| Undo Expansion | `NVDA+Shift+E` | Reverts the last text expansion |
| Show Shortcut Info | `NVDA+Shift+S` | Checks if word at cursor is a shortcut |
| List All Shortcuts | `NVDA+Shift+L` | Displays a quick list of all shortcuts |

## Manager Dialog Shortcuts

| Command | Key | Description |
|---------|-----|-------------|
| Add New | `Ctrl+A` | Add a new shortcut |
| Edit | `F2` or `Enter` | Edit selected shortcut |
| Delete | `Delete` | Remove selected shortcut |
| Search | `Alt+S` | Focus search field |

## Advanced Features

### Import/Export

Backup and share your shortcuts:
1. Open the manager (`NVDA+Shift+K`)
2. Click "Export" to save shortcuts to a JSON file
3. Click "Import" to load shortcuts from a file

### Special Characters

In expansion text:
- Use `\n` for new lines
- Use `\t` for tabs

### Creating Effective Shortcuts

**Best Practices:**
- Keep shortcuts short and memorable
- Avoid common words to prevent accidental expansion
- Use consistent patterns (e.g., all email shortcuts end with @)
- Group related shortcuts with prefixes

**Examples:**
- Email signatures: `sig1`, `sig2`, `sigwork`
- Addresses: `addr1`, `addr2`
- Phone numbers: `ph1`, `ph2`
- Templates: `tpl1`, `tpl2`

## Troubleshooting

### Shortcut not expanding?
- Ensure the addon is enabled (`NVDA+Alt+Shift+K`)
- Check if you're in an editable text field
- Verify the shortcut exists in the manager

### Manager dialog not opening?
- Ensure no other NVDA dialog is open
- Try restarting NVDA
- Check NVDA's log for errors

### Expansion in wrong place?
- Make sure cursor is right after the shortcut
- Don't have spaces or punctuation between shortcut and cursor

## Supported Applications

Works in most Windows applications including:
- Microsoft Office (Word, Outlook, Excel)
- Web browsers (Chrome, Firefox, Edge)
- Text editors (Notepad++, VS Code)
- Email clients
- Social media applications
- Chat applications

## Privacy & Data

- All shortcuts are stored locally on your computer
- No data is sent to external servers
- Configuration file location: `%APPDATA%\nvda\keyboardShortcutsPro.json`

## Contributing

Found a bug or have a suggestion? Please visit:
https://github.com/Mohammedkhaled96/keyboard_shortcut_autocomplete_pro
## Changelog

### Version 1.1.1 (2025)
- Complete rewrite with professional interface
- Added search functionality in manager
- Import/Export capabilities
- Live expansion hints
- Undo functionality
- Thread-safe operations
- Enhanced error handling
- Improved text expansion reliability

### Version 1.0.0 (2024)
- Initial release
- Basic text expansion
- Simple shortcuts manager

## Acknowledgments

Special thanks to the NVDA community for their continuous support and feedback.

## License

This addon is licensed under GNU General Public License v2.
For full license text, visit: https://www.gnu.org/licenses/gpl-2.0.html

---

For support, feature requests, or bug reports, please contact:
mohammed.khaled.mahmoud1996@gmail.com