# 🎮 Tic Tac Toe by TheFallenAngel

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

A **professional-grade Tic Tac Toe game** featuring an intelligent AI opponent powered by the minimax algorithm, stunning visual themes, auto-save functionality, and a complete Windows installer.

## ✨ Features

### 🎯 Gameplay
- **Smart AI Opponent** - Uses minimax algorithm for optimal moves (never loses!)
- **First Move Advantage** - You play as X, bot plays as O
- **Perfect Strategy** - Bot will win or draw every time
- **Visual Feedback** - Winning line animation with glow effects

### 🎨 Visual Themes
- **🌙 Dark Theme** - Easy on the eyes, perfect for night gaming
- **☀️ Light Theme** - Clean and professional for daytime
- **🌈 Neon Theme** - Vibrant colors with modern aesthetic

### 💾 Save & Progress
- **Auto-Save** - Game state saves automatically on every move
- **Statistics Tracking** - Wins, Losses, and Draws counter
- **Persistent Data** - Game continues where you left off
- **Configuration Storage** - Saves your theme preferences

### 🖥️ Professional Installation
- **Windows Installer** - One-click setup to Program Files
- **Desktop Shortcut** - Automatic shortcut creation
- **Start Menu Integration** - Appears in Windows Start Menu
- **Clean Uninstaller** - Complete removal with uninstall.bat
- **Admin Privilege Handling** - Automatic elevation when needed

### 🎵 Audio & Effects
- **Sound Effects** - Click, win, lose, and draw sounds (Windows)
- **Visual Feedback** - Button hover effects and glow animations
- **Responsive Design** - UI adapts to window resizing

### ⌨️ Keyboard Shortcuts
- `F11` - Toggle fullscreen mode
- `Esc` - Exit fullscreen
- `Alt+F4` - Close game (auto-saves)

## 📋 Requirements

### System Requirements
| Component | Minimum |
|-----------|---------|
| **OS** | Windows 7/8/10/11 (or Linux/macOS for manual run) |
| **Python** | 3.6 or higher |
| **RAM** | 128 MB |
| **Disk Space** | 10 MB |
| **Display** | 800x600 or higher |

### Python Dependencies
```txt
No external dependencies! Only Python standard library:
- tkinter (GUI)
- json (save/load)
- logging (error tracking)
- subprocess (installation)
- pathlib (file management)
- datetime (timestamps)
```

## 🚀 Installation

### Automatic Installation (Windows - Recommended)

1. **Download** `tictactoe.py`
2. **Right-click** and select **"Run as Administrator"**
3. **Follow** the setup wizard
4. **Launch** from Desktop shortcut or Start Menu

The installer will:
- Copy game to `C:\Program Files (x86)\Tic Tac Toe by TheFallenAngel\`
- Create desktop and Start Menu shortcuts
- Set up virtual environment (optional)
- Configure auto-save directory

### Manual Installation (All Platforms)

```bash
# Clone the repository
git clone https://github.com/thefallenangel7890/TicTacToe-TFA.git

# Navigate to directory
cd TicTacToe-TFA

# Run the game
python tictactoe.py
```

### Linux/macOS Additional Setup

```bash
# Make script executable (if needed)
chmod +x tictactoe.py

# Run with python3
python3 tictactoe.py
```

## 🎮 How to Play

### Basic Rules
1. **You are X** - Make the first move
2. **Bot is O** - AI responds instantly
3. **Get 3 in a row** - Horizontally, vertically, or diagonally
4. **Block the bot** - AI will try to win or block you

### Game Flow
```
Start Game → Your Turn (X) → Click Cell → Bot Thinks → Bot Moves (O) → Repeat
```

### Win Conditions
- Any row of 3 identical marks
- Any column of 3 identical marks
- Either diagonal of 3 identical marks

### Strategy Tips
- **Control the center** - Most powerful position
- **Create forks** - Two ways to win simultaneously
- **Block bot's threats** - Prevent opponent from getting 3 in a row
- **Use corners** - Next best after center

## 📁 File Structure

```
TicTacToe-TFA/
├── tictactoe.py              # Main game application (35KB)
├── README.md                 # Documentation (this file)
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
├── requirements.txt         # Dependencies (none)
│
└── User Data (Auto-created in %APPDATA%):
    ├── config.json          # User preferences
    ├── game_save.json       # Current game state
    ├── version.json         # Version tracking
    └── game.log             # Error logs
```

## 💻 Technical Details

### AI Implementation (Minimax Algorithm)
```python
def minimax(board, is_maximizing):
    """
    Recursive algorithm that simulates all possible moves
    Returns score: +1 (bot win), -1 (human win), 0 (draw)
    """
```

**Complexity:** O(9!) = 362,880 maximum positions evaluated  
**Response Time:** < 50ms on modern hardware

### Save System
- **Format:** JSON
- **Location:** `%APPDATA%\Tic Tac Toe by TheFallenAngel\`
- **Data saved:** Board state, game status, theme, statistics
- **Trigger:** Every move and on window close

### Logging System
- **Level:** INFO and ERROR
- **Location:** `%APPDATA%\...\game.log`
- **Rotation:** Manual only (for debugging)
- **Contents:** Errors, saves, loads, game events

## 🎯 Statistics Tracking

The game tracks your performance:

| Statistic | Description | Reset |
|-----------|-------------|-------|
| **Wins** | Games you've won | Manual only |
| **Losses** | Games bot has won | Manual only |
| **Draws** | Tied games | Manual only |
| **Total Games** | Sum of all games | Manual only |

*Note: Statistics persist between sessions*

## 🔧 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **"Failed to install" error** | Run as Administrator |
| **Game won't start** | Check Python installation: `python --version` |
| **No sound effects** | Sound only works on Windows |
| **Theme not changing** | Restart the game |
| **Save file corrupted** | Delete `%APPDATA%\...\game_save.json` |
| **Bot not responding** | Check game.log for errors |

### Error Logs
Check `%APPDATA%\Tic Tac Toe by TheFallenAngel\game.log` for:
- Python tracebacks
- Save/load errors
- Theme application issues
- Installation failures

## 🗑️ Uninstallation

### Windows (Automatic)
1. Run `uninstall.bat` from installation folder
2. Or use Windows Control Panel → Programs → Uninstall

### Manual Uninstallation
```bash
# Remove installation directory
rmdir /s /q "C:\Program Files (x86)\Tic Tac Toe by TheFallenAngel"

# Remove user data
rmdir /s /q "%APPDATA%\Tic Tac Toe by TheFallenAngel"

# Remove shortcuts
del "%USERPROFILE%\Desktop\Tic Tac Toe by TheFallenAngel.lnk"
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Tic Tac Toe by TheFallenAngel.lnk"
```

## 📊 Version History

### v1.0.0 (Current)
- ✅ Initial release
- ✅ Minimax AI implementation
- ✅ Three themes (Dark, Light, Neon)
- ✅ Auto-save functionality
- ✅ Windows installer
- ✅ Statistics tracking
- ✅ Fullscreen support
- ✅ Sound effects (Windows)

### Planned Features (v1.1.0)
- 🔜 Two-player mode
- 🔜 Difficulty levels (Easy, Medium, Hard)
- 🔜 Custom themes
- 🔜 Online leaderboards
- 🔜 Achievements system
- 🔜 Animation speed controls

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit** changes: `git commit -m 'Add AmazingFeature'`
4. **Push** to branch: `git push origin feature/AmazingFeature`
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/TicTacToe-TFA.git

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Run in development mode
python tictactoe.py
```

## 📝 License

Distributed under the **MIT License**. See `LICENSE` file for more information.

```
MIT License

Copyright (c) 2024 TheFallenAngel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👤 Author

**TheFallenAngel**

- GitHub: [@thefallenangel7890](https://github.com/thefallenangel7890)
- Project Link: [https://github.com/thefallenangel7890/TicTacToe-TFA](https://github.com/thefallenangel7890/TicTacToe-TFA)

## 🙏 Acknowledgments

- Minimax algorithm implementation based on classic AI theory
- Tkinter for cross-platform GUI support
- Windows API for sound and installation features
- All beta testers and contributors

## 📞 Support

For support, questions, or suggestions:
1. **Open an issue** on GitHub
2. **Check** the troubleshooting guide above
3. **Review** `game.log` for errors
4. **Contact** via GitHub discussions

## ⭐ Show Your Support

If you found this project helpful:
- ⭐ Star the repository on GitHub
- 🐛 Report bugs or issues
- 💡 Suggest new features
- 🔄 Share with others

## 📜 License & EULA

This project includes two legal documents:

- **MIT License** - Open source license for code usage and distribution
- **EULA** - End User License Agreement with specific usage terms

By using this software, you agree to both documents. See the `LICENSE` and `EULA` files in the repository root for full details.

---

**Made with ❤️ by TheFallenAngel**
