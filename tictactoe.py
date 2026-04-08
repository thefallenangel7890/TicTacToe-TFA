#!/usr/bin/env python3
"""
Tic Tac Toe - Professional Application
Installs to: C:\Program Files (x86)\Tic Tac Toe by TheFallenAngel
Features: Auto-update checking, progress saving, virtual environment, smart setup
"""

import sys
import os
import subprocess
import importlib.metadata
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import logging
import json
import shutil
import ctypes
from datetime import datetime, timedelta

# Application constants
APP_NAME = "Tic Tac Toe by TheFallenAngel"
APP_ID = "TicTacToe_TFA"
INSTALL_PATH = Path("C:/Program Files (x86)") / APP_NAME
DATA_PATH = Path(os.getenv('APPDATA')) / APP_NAME
VERSION_FILE = DATA_PATH / "version.json"
CONFIG_FILE = DATA_PATH / "config.json"
SAVE_FILE = DATA_PATH / "game_save.json"
LOG_FILE = DATA_PATH / "game.log"
VENV_PATH = INSTALL_PATH / "venv"

# Create data directory if it doesn't exist
DATA_PATH.mkdir(parents=True, exist_ok=True)

# Configure logging
class UnicodeStreamHandler(logging.StreamHandler):
    """Custom handler to handle Unicode characters on Windows"""
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            try:
                stream.write(msg + self.terminator)
            except UnicodeEncodeError:
                msg_ascii = msg.encode('ascii', 'ignore').decode('ascii')
                stream.write(msg_ascii + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Remove existing handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Add file handler
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Add console handler with Unicode support
console_handler = UnicodeStreamHandler()
console_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(console_handler)

def is_admin():
    """Check if running as administrator"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch the script with administrator privileges"""
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        return True
    except Exception:
        return False

class ApplicationInstaller:
    """Handles application installation and setup"""
    
    CURRENT_VERSION = "1.0.0"
    CHECK_INTERVAL_DAYS = 7
    
    @staticmethod
    def is_installed():
        """Check if application is already installed"""
        return CONFIG_FILE.exists() and CONFIG_FILE.read_text() if CONFIG_FILE.exists() else False
    
    @staticmethod
    def install_to_program_files():
        """Install application to Program Files"""
        try:
            # Create installation directory if it doesn't exist
            if not INSTALL_PATH.exists():
                INSTALL_PATH.mkdir(parents=True)
                logger.info(f"Created installation directory: {INSTALL_PATH}")
            
            # Copy current script to installation directory
            current_script = Path(sys.argv[0])
            target_script = INSTALL_PATH / "tictactoe.py"
            
            if current_script != target_script:
                shutil.copy2(current_script, target_script)
                logger.info(f"Installed to: {target_script}")
            
            # Create launcher batch file
            launcher = INSTALL_PATH / "launch_game.bat"
            with open(launcher, 'w') as f:
                f.write(f'''@echo off
cd /d "{INSTALL_PATH}"
"{sys.executable}" tictactoe.py
pause
''')
            
            # Create desktop shortcut
            ApplicationInstaller.create_desktop_shortcut()
            
            # Add to start menu
            ApplicationInstaller.add_to_start_menu()
            
            # Create uninstaller
            ApplicationInstaller.create_uninstaller()
            
            return True
        except Exception as e:
            logger.error(f"Installation failed: {e}")
            return False
    
    @staticmethod
    def create_desktop_shortcut():
        """Create desktop shortcut"""
        try:
            desktop = Path(os.path.expanduser("~/Desktop"))
            shortcut_path = desktop / f"{APP_NAME}.lnk"
            
            # Create shortcut using PowerShell
            ps_script = f'''
            $WScriptShell = New-Object -ComObject WScript.Shell
            $Shortcut = $WScriptShell.CreateShortcut("{shortcut_path}")
            $Shortcut.TargetPath = "{sys.executable}"
            $Shortcut.Arguments = '"{INSTALL_PATH / "tictactoe.py"}"'
            $Shortcut.WorkingDirectory = "{INSTALL_PATH}"
            $Shortcut.Description = "{APP_NAME}"
            $Shortcut.Save()
            '''
            subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
            logger.info("Desktop shortcut created")
        except Exception as e:
            logger.warning(f"Could not create desktop shortcut: {e}")
    
    @staticmethod
    def add_to_start_menu():
        """Add to start menu"""
        try:
            start_menu = Path(os.getenv('APPDATA')) / "Microsoft/Windows/Start Menu/Programs"
            shortcut_path = start_menu / f"{APP_NAME}.lnk"
            
            ps_script = f'''
            $WScriptShell = New-Object -ComObject WScript.Shell
            $Shortcut = $WScriptShell.CreateShortcut("{shortcut_path}")
            $Shortcut.TargetPath = "{sys.executable}"
            $Shortcut.Arguments = '"{INSTALL_PATH / "tictactoe.py"}"'
            $Shortcut.WorkingDirectory = "{INSTALL_PATH}"
            $Shortcut.Description = "{APP_NAME}"
            $Shortcut.Save()
            '''
            subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
            logger.info("Added to Start Menu")
        except Exception as e:
            logger.warning(f"Could not add to Start Menu: {e}")
    
    @staticmethod
    def create_uninstaller():
        """Create uninstaller"""
        uninstall_script = INSTALL_PATH / "uninstall.bat"
        with open(uninstall_script, 'w') as f:
            f.write(f'''@echo off
echo Uninstalling {APP_NAME}...
echo.

REM Kill any running instances
taskkill /f /im python.exe /fi "WINDOWTITLE eq {APP_NAME}*" 2>nul

REM Remove installation directory
echo Removing installation files...
rmdir /s /q "{INSTALL_PATH}" 2>nul

REM Remove user data
echo Removing user data...
rmdir /s /q "{DATA_PATH}" 2>nul

REM Remove desktop shortcut
del /f /q "%USERPROFILE%\\Desktop\\{APP_NAME}.lnk" 2>nul

REM Remove start menu shortcut
del /f /q "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{APP_NAME}.lnk" 2>nul

echo.
echo {APP_NAME} has been uninstalled successfully.
echo.
timeout /t 3
''')
        logger.info("Uninstaller created")
    
    @staticmethod
    def setup_virtual_environment():
        """Setup virtual environment in installation directory"""
        if not INSTALL_PATH.exists():
            INSTALL_PATH.mkdir(parents=True)
        
        if not VENV_PATH.exists():
            logger.info("Creating virtual environment...")
            try:
                subprocess.run([sys.executable, "-m", "venv", str(VENV_PATH)], 
                             check=True, capture_output=True)
                logger.info("Virtual environment created")
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to create virtual environment: {e}")
                return False
        return True
    
    @staticmethod
    def get_pip_path():
        """Get pip path in virtual environment"""
        if VENV_PATH.exists():
            if sys.platform == "win32":
                return VENV_PATH / "Scripts" / "pip.exe"
            else:
                return VENV_PATH / "bin" / "pip"
        return None
    
    @staticmethod
    def upgrade_pip():
        """Upgrade pip in virtual environment"""
        pip_path = ApplicationInstaller.get_pip_path()
        if pip_path and pip_path.exists():
            logger.info("Upgrading pip...")
            try:
                subprocess.run([str(pip_path), "install", "--upgrade", "pip"], 
                             capture_output=True, check=True)
                logger.info("Pip upgraded successfully")
                return True
            except Exception as e:
                logger.warning(f"Could not upgrade pip: {e}")
        return False
    
    @staticmethod
    def install_requirements():
        """Install required packages"""
        requirements = []
        pip_path = ApplicationInstaller.get_pip_path()
        
        if pip_path and pip_path.exists():
            logger.info("Installing required packages...")
            for package in requirements:
                try:
                    subprocess.run([str(pip_path), "install", package], 
                                 capture_output=True, check=True)
                    logger.info(f"Installed: {package}")
                except Exception as e:
                    logger.warning(f"Could not install {package}: {e}")
    
    @staticmethod
    def check_for_updates():
        """Check for available updates"""
        try:
            # Read last check time
            if VERSION_FILE.exists():
                with open(VERSION_FILE, 'r') as f:
                    data = json.load(f)
                    last_check = datetime.fromisoformat(data.get('last_check', '2000-01-01'))
                    
                    # Check if we need to check again
                    if datetime.now() - last_check < timedelta(days=ApplicationInstaller.CHECK_INTERVAL_DAYS):
                        return None
            
            # Update last check time
            with open(VERSION_FILE, 'w') as f:
                json.dump({'last_check': datetime.now().isoformat(), 
                          'current_version': ApplicationInstaller.CURRENT_VERSION}, f)
            
            return None
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return None

class SmartSetup:
    """Handles smart setup and quick launch"""
    
    @staticmethod
    def is_first_run():
        """Check if this is first run"""
        return not CONFIG_FILE.exists()
    
    @staticmethod
    def quick_launch():
        """Quick launch without full setup"""
        logger.info("Quick launch mode - Starting game...")
        return True
    
    @staticmethod
    def full_setup():
        """Perform full setup on first run"""
        logger.info("=" * 60)
        logger.info("First-time setup - Installing application...")
        logger.info("=" * 60)
        
        # Check admin rights
        if not is_admin():
            logger.error("Administrator privileges required for installation!")
            logger.info("Please run as administrator for first-time setup.")
            return False
        
        # Install to Program Files
        if not ApplicationInstaller.install_to_program_files():
            logger.error("Failed to install to Program Files")
            return False
        
        # Setup virtual environment
        if not ApplicationInstaller.setup_virtual_environment():
            logger.warning("Virtual environment setup failed, continuing anyway")
        
        # Upgrade pip
        ApplicationInstaller.upgrade_pip()
        
        # Install requirements
        ApplicationInstaller.install_requirements()
        
        # Save config
        config = {
            'installed': True,
            'install_date': datetime.now().isoformat(),
            'version': ApplicationInstaller.CURRENT_VERSION,
            'setup_complete': True,
            'install_path': str(INSTALL_PATH)
        }
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info("Setup completed successfully!")
        return True

class GameState:
    """Handle game save/load functionality"""
    
    @staticmethod
    def save_game(board, game_active, theme, stats):
        """Save game state"""
        try:
            save_data = {
                'board': board,
                'game_active': game_active,
                'theme': theme,
                'stats': stats,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(SAVE_FILE, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            logger.info("Game saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save game: {e}")
            return False
    
    @staticmethod
    def load_game():
        """Load game state"""
        try:
            if SAVE_FILE.exists():
                with open(SAVE_FILE, 'r') as f:
                    save_data = json.load(f)
                logger.info("Game loaded successfully")
                return save_data
        except Exception as e:
            logger.error(f"Failed to load game: {e}")
        return None

# ---------- Optional sound (Windows only) ----------
SOUND_AVAILABLE = False
try:
    import winsound
    SOUND_AVAILABLE = True
    logger.info("Sound support enabled")
except ImportError:
    logger.info("Sound support not available")

# ---------- Constants ----------
EMPTY = " "
HUMAN = "X"
BOT = "O"

THEMES = {
    "Dark": {
        "root_bg": "#020617",
        "card_bg": "#020617",
        "button_bg": "#111827",
        "button_hover": "#1f2937",
        "button_fg": "#e5e7eb",
        "title_fg": "#e5e7eb",
        "subtitle_fg": "#9ca3af",
        "status_user_fg": "#f97316",
        "status_bot_fg": "#38bdf8",
        "status_win_fg": "#22c55e",
        "status_lose_fg": "#ef4444",
        "status_draw_fg": "#e5e7eb",
        "reset_bg": "#f97316",
        "reset_hover": "#fb923c",
        "reset_fg": "#111827",
        "footer_fg": "#4b5563",
        "win_line": "#22c55e",
        "glow": "#facc15",
    },
    "Light": {
        "root_bg": "#e5e7eb",
        "card_bg": "#f9fafb",
        "button_bg": "#e5e7eb",
        "button_hover": "#d1d5db",
        "button_fg": "#111827",
        "title_fg": "#111827",
        "subtitle_fg": "#4b5563",
        "status_user_fg": "#2563eb",
        "status_bot_fg": "#16a34a",
        "status_win_fg": "#16a34a",
        "status_lose_fg": "#b91c1c",
        "status_draw_fg": "#374151",
        "reset_bg": "#2563eb",
        "reset_hover": "#1d4ed8",
        "reset_fg": "#f9fafb",
        "footer_fg": "#6b7280",
        "win_line": "#16a34a",
        "glow": "#fde047",
    },
    "Neon": {
        "root_bg": "#020617",
        "card_bg": "#020617",
        "button_bg": "#020617",
        "button_hover": "#0f172a",
        "button_fg": "#e5e7eb",
        "title_fg": "#22d3ee",
        "subtitle_fg": "#a855f7",
        "status_user_fg": "#22c55e",
        "status_bot_fg": "#eab308",
        "status_win_fg": "#22c55e",
        "status_lose_fg": "#f97316",
        "status_draw_fg": "#e5e7eb",
        "reset_bg": "#a855f7",
        "reset_hover": "#c084fc",
        "reset_fg": "#020617",
        "footer_fg": "#64748b",
        "win_line": "#22d3ee",
        "glow": "#f97316",
    },
}

class TicTacToeBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME}")
        
        # Set initial window size
        self.base_width = 400
        self.base_height = 450
        self.root.geometry(f"{self.base_width}x{self.base_height}")
        
        # Allow window resizing
        self.root.resizable(True, True)
        self.root.minsize(350, 400)
        
        self.current_theme_name = "Dark"
        self.theme = THEMES[self.current_theme_name]
        
        # Game stats
        self.stats = {
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'total_games': 0
        }
        
        # Initialize attributes
        self.buttons = []
        self.board = [EMPTY] * 9
        self.game_active = True
        self.last_win_combo = None
        self.thinking_step = 0
        self.is_fullscreen = False
        self.win_line_coords = None
        self.win_canvas = None
        self.reset_button = None
        self.status_label = None
        self.title_label = None
        self.subtitle_label = None
        self.footer_label = None
        self.theme_label = None
        self.theme_menu = None
        self.card = None
        self.card_inner = None
        self.board_frame = None
        self.stats_label = None
        
        # Initialize font sizes
        self.current_font_sizes = {
            'title': 20,
            'subtitle': 10,
            'status': 11,
            'reset': 10,
            'footer': 8,
            'button': 20,
            'stats': 9
        }
        
        self.set_icon()
        self.center_window(self.base_width, self.base_height)
        
        # Load saved game
        self.load_saved_game()
        
        # Setup UI
        self.setup_ui()
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Fullscreen shortcuts
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        # Save game on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_saved_game(self):
        """Load saved game state"""
        saved_data = GameState.load_game()
        if saved_data:
            self.board = saved_data.get('board', [EMPTY] * 9)
            self.game_active = saved_data.get('game_active', True)
            self.current_theme_name = saved_data.get('theme', 'Dark')
            self.stats = saved_data.get('stats', self.stats)
            logger.info("Previous game loaded")
    
    def save_current_game(self):
        """Save current game state"""
        GameState.save_game(self.board, self.game_active, self.current_theme_name, self.stats)
    
    def on_closing(self):
        """Handle window closing"""
        self.save_current_game()
        self.root.destroy()
    
    def setup_ui(self):
        """Setup the complete UI"""
        # Configure root
        self.root.configure(bg=self.theme["root_bg"])
        
        # Main container
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.card = tk.Frame(self.root, bg=self.theme["root_bg"], highlightthickness=0)
        self.card.grid(row=0, column=0, sticky="nsew")
        
        self.card.grid_rowconfigure(0, weight=1)
        self.card.grid_columnconfigure(0, weight=1)
        
        self.card_inner = tk.Frame(self.card, bg=self.theme["card_bg"])
        self.card_inner.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure grid
        for i in range(8):
            self.card_inner.grid_rowconfigure(i, weight=1 if i == 5 else 0)
        self.card_inner.grid_columnconfigure(0, weight=1)
        self.card_inner.grid_columnconfigure(1, weight=0)
        self.card_inner.grid_columnconfigure(2, weight=0)
        
        # Theme switcher
        self.theme_var = tk.StringVar(value=self.current_theme_name)
        self.theme_label = tk.Label(
            self.card_inner,
            text="Theme:",
            font=("Segoe UI", 9),
            anchor="e",
            bg=self.theme["card_bg"],
            fg=self.theme["subtitle_fg"],
        )
        self.theme_label.grid(row=0, column=1, sticky="e", pady=(0, 5), padx=(0, 4))
        
        self.theme_menu = tk.OptionMenu(
            self.card_inner,
            self.theme_var,
            *THEMES.keys(),
            command=self.change_theme,
        )
        self.theme_menu.grid(row=0, column=2, sticky="e", pady=(0, 5))
        
        # Title
        self.title_label = tk.Label(
            self.card_inner,
            text="Tic Tac Toe",
            font=("Segoe UI", self.current_font_sizes['title'], "bold"),
            bg=self.theme["card_bg"],
            fg=self.theme["title_fg"],
        )
        self.title_label.grid(row=1, column=0, columnspan=3, pady=(0, 4))
        
        # Subtitle
        self.subtitle_label = tk.Label(
            self.card_inner,
            text="Human (X) vs Bot (O)",
            font=("Segoe UI", self.current_font_sizes['subtitle']),
            bg=self.theme["card_bg"],
            fg=self.theme["subtitle_fg"],
        )
        self.subtitle_label.grid(row=2, column=0, columnspan=3, pady=(0, 10))
        
        # Stats
        self.update_stats_display()
        
        # Status
        self.status_label = tk.Label(
            self.card_inner,
            text="Your turn (X)" if self.game_active else "Game Over",
            font=("Segoe UI", self.current_font_sizes['status']),
            bg=self.theme["card_bg"],
            fg=self.theme["status_user_fg"],
        )
        self.status_label.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        # Board
        self.board_frame = tk.Frame(self.card_inner, bg=self.theme["card_bg"])
        self.board_frame.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)
        
        # Create buttons
        self.create_responsive_buttons()
        
        # Canvas for win line
        self.win_canvas = tk.Canvas(
            self.board_frame,
            bg=self.theme["card_bg"],
            highlightthickness=0,
            bd=0,
        )
        self.win_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.root.update_idletasks()
        self.root.tk.call("lower", self.win_canvas._w)
        
        # Reset button
        self.reset_button = tk.Button(
            self.card_inner,
            text="Reset Game",
            font=("Segoe UI", self.current_font_sizes['reset'], "bold"),
            bg=self.theme["reset_bg"],
            fg=self.theme["reset_fg"],
            activebackground=self.theme["reset_hover"],
            activeforeground=self.theme["reset_fg"],
            relief="flat",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.reset_game,
        )
        self.reset_button.grid(row=6, column=0, columnspan=3, pady=(0, 8))
        self.add_hover_effect(self.reset_button,
                              base=self.theme["reset_bg"],
                              hover=self.theme["reset_hover"])
        
        # Footer
        self.footer_label = tk.Label(
            self.card_inner,
            text="F11: Fullscreen | Esc: Exit | Auto-saves progress",
            font=("Segoe UI", self.current_font_sizes['footer']),
            bg=self.theme["card_bg"],
            fg=self.theme["footer_fg"],
        )
        self.footer_label.grid(row=7, column=0, columnspan=3, pady=(5, 0))
        
        # Apply theme and load board state
        self.apply_theme()
        self.load_board_state()
    
    def update_stats_display(self):
        """Update stats display"""
        if hasattr(self, 'stats_label') and self.stats_label:
            self.stats_label.destroy()
        
        self.stats_label = tk.Label(
            self.card_inner,
            text=f"Wins: {self.stats['wins']} | Losses: {self.stats['losses']} | Draws: {self.stats['draws']}",
            font=("Segoe UI", self.current_font_sizes['stats']),
            bg=self.theme["card_bg"],
            fg=self.theme["subtitle_fg"],
        )
        self.stats_label.grid(row=3, column=0, columnspan=3, pady=(0, 8))
    
    def load_board_state(self):
        """Load board state from saved game"""
        for i, value in enumerate(self.board):
            if value != EMPTY:
                self.buttons[i].config(text=value)
    
    def create_responsive_buttons(self):
        """Create responsive buttons"""
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                text="",
                font=("Segoe UI", self.current_font_sizes['button'], "bold"),
                relief="flat",
                bg=self.theme["button_bg"],
                fg=self.theme["button_fg"],
                activebackground=self.theme["button_hover"],
                activeforeground=self.theme["button_fg"],
                bd=0,
                command=lambda idx=i: self.human_move(idx),
                cursor="hand2",
            )
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
            self.add_hover_effect(btn,
                                  base=self.theme["button_bg"],
                                  hover=self.theme["button_hover"])
            self.buttons.append(btn)
    
    def on_window_resize(self, event):
        """Handle window resize"""
        if event.widget == self.root and hasattr(self, 'title_label'):
            scale_factor = min(event.width / self.base_width, event.height / self.base_height, 1.5)
            
            sizes = {
                'title': max(14, int(20 * scale_factor)),
                'subtitle': max(8, int(10 * scale_factor)),
                'status': max(9, int(11 * scale_factor)),
                'reset': max(8, int(10 * scale_factor)),
                'footer': max(7, int(8 * scale_factor)),
                'button': max(14, int(20 * scale_factor)),
                'stats': max(8, int(9 * scale_factor))
            }
            
            self.title_label.configure(font=("Segoe UI", sizes['title'], "bold"))
            self.subtitle_label.configure(font=("Segoe UI", sizes['subtitle']))
            self.status_label.configure(font=("Segoe UI", sizes['status']))
            self.reset_button.configure(font=("Segoe UI", sizes['reset'], "bold"))
            self.footer_label.configure(font=("Segoe UI", sizes['footer']))
            self.stats_label.configure(font=("Segoe UI", sizes['stats']))
            
            for btn in self.buttons:
                btn.configure(font=("Segoe UI", sizes['button'], "bold"))
            
            self.current_font_sizes = sizes
    
    def set_icon(self):
        """Set window icon"""
        try:
            icon_paths = ["tictactoe.ico", "icon.ico", "game.ico"]
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    break
        except Exception:
            pass
    
    def center_window(self, width, height):
        """Center window on screen"""
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen"""
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
    
    def add_hover_effect(self, widget, base, hover):
        """Add hover effect"""
        def on_enter(_):
            widget["bg"] = hover
        
        def on_leave(_):
            widget["bg"] = base
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def apply_theme(self):
        """Apply theme"""
        if not hasattr(self, 'theme'):
            return
        
        self.theme = THEMES[self.current_theme_name]
        
        self.root.configure(bg=self.theme["root_bg"])
        if self.card:
            self.card.configure(bg=self.theme["root_bg"])
        if self.card_inner:
            self.card_inner.configure(bg=self.theme["card_bg"])
        if self.board_frame:
            self.board_frame.configure(bg=self.theme["card_bg"])
        if self.win_canvas:
            self.win_canvas.configure(bg=self.theme["card_bg"])
        
        if self.title_label:
            self.title_label.configure(bg=self.theme["card_bg"], fg=self.theme["title_fg"])
        if self.subtitle_label:
            self.subtitle_label.configure(bg=self.theme["card_bg"], fg=self.theme["subtitle_fg"])
        if self.footer_label:
            self.footer_label.configure(bg=self.theme["card_bg"], fg=self.theme["footer_fg"])
        if self.status_label:
            self.status_label.configure(bg=self.theme["card_bg"])
        if self.stats_label:
            self.stats_label.configure(bg=self.theme["card_bg"], fg=self.theme["subtitle_fg"])
        
        if self.theme_label:
            self.theme_label.configure(bg=self.theme["card_bg"], fg=self.theme["subtitle_fg"])
        
        if self.theme_menu:
            self.theme_menu.configure(
                bg=self.theme["button_bg"],
                fg=self.theme["button_fg"],
                activebackground=self.theme["button_hover"],
                activeforeground=self.theme["button_fg"],
            )
            menu = self.theme_menu["menu"]
            if menu:
                menu.configure(
                    bg=self.theme["button_bg"],
                    fg=self.theme["button_fg"],
                    activebackground=self.theme["button_hover"],
                    activeforeground=self.theme["button_fg"],
                )
        
        for btn in self.buttons:
            btn.configure(
                bg=self.theme["button_bg"],
                fg=self.theme["button_fg"],
                activebackground=self.theme["button_hover"],
                activeforeground=self.theme["button_fg"],
            )
        
        if self.reset_button:
            self.reset_button.configure(
                bg=self.theme["reset_bg"],
                fg=self.theme["reset_fg"],
                activebackground=self.theme["reset_hover"],
                activeforeground=self.theme["reset_fg"],
            )
    
    def change_theme(self, value):
        """Change theme"""
        self.current_theme_name = value
        self.apply_theme()
        self.save_current_game()
    
    def play_sound(self, kind):
        """Play sound"""
        if not SOUND_AVAILABLE:
            return
        try:
            if kind == "click":
                winsound.MessageBeep(winsound.MB_OK)
            elif kind == "win":
                winsound.Beep(880, 120)
                winsound.Beep(988, 160)
            elif kind == "lose":
                winsound.Beep(220, 200)
                winsound.Beep(196, 240)
            elif kind == "draw":
                winsound.Beep(600, 150)
        except Exception:
            pass
    
    def human_move(self, index):
        """Handle human move"""
        try:
            if not self.game_active or self.board[index] != EMPTY:
                return
            
            self.board[index] = HUMAN
            self.buttons[index]["text"] = HUMAN
            self.glow_button(self.buttons[index])
            self.play_sound("click")
            
            result = self.check_game_state()
            if result:
                self.end_game(result)
                return
            
            self.start_bot_thinking()
            self.save_current_game()
        except Exception as e:
            logger.error(f"Error in human_move: {e}")
    
    def start_bot_thinking(self):
        """Start bot thinking animation"""
        self.thinking_step = 0
        self.animate_thinking()
    
    def animate_thinking(self):
        """Animate bot thinking"""
        try:
            if not self.game_active:
                return
            dots = "." * ((self.thinking_step % 3) + 1)
            self.status_label.config(
                text=f"Bot thinking{dots}",
                fg=self.theme["status_bot_fg"],
            )
            self.thinking_step += 1
            if self.thinking_step >= 4:
                self.root.after(150, self.bot_move)
            else:
                self.root.after(250, self.animate_thinking)
        except Exception as e:
            logger.error(f"Error in animate_thinking: {e}")
    
    def bot_move(self):
        """Execute bot move"""
        try:
            if not self.game_active:
                return
            
            best_index = self.find_best_move()
            if best_index is not None:
                self.board[best_index] = BOT
                self.buttons[best_index]["text"] = BOT
            
            result = self.check_game_state()
            if result:
                self.end_game(result)
            else:
                self.status_label.config(
                    text="Your turn (X)",
                    fg=self.theme["status_user_fg"],
                )
            self.save_current_game()
        except Exception as e:
            logger.error(f"Error in bot_move: {e}")
    
    def check_game_state(self):
        """Check game state"""
        try:
            winner, combo = self.get_winner()
            self.last_win_combo = combo
            
            if winner == HUMAN:
                return "HUMAN_WIN"
            elif winner == BOT:
                return "BOT_WIN"
            elif all(cell != EMPTY for cell in self.board):
                return "DRAW"
            return None
        except Exception as e:
            logger.error(f"Error in check_game_state: {e}")
            return None
    
    def get_winner(self):
        """Get winner"""
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        
        for combo in winning_combinations:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] != EMPTY:
                return self.board[a], combo
        return None, None
    
    def glow_button(self, btn):
        """Glow effect"""
        try:
            base_bg = self.theme["button_bg"]
            glow_bg = self.theme["glow"]
            btn.config(bg=glow_bg)
            self.root.after(150, lambda: btn.config(bg=base_bg))
        except Exception:
            pass
    
    def animate_win_line(self, combo, step=0, steps=18):
        """Animate win line"""
        try:
            if combo is None or not self.win_canvas:
                return
            
            if step == 0:
                self.root.update_idletasks()
                self.root.tk.call("raise", self.win_canvas._w)
                
                b_start = self.buttons[combo[0]]
                b_end = self.buttons[combo[2]]
                
                x1 = b_start.winfo_x() + b_start.winfo_width() / 2
                y1 = b_start.winfo_y() + b_start.winfo_height() / 2
                x2 = b_end.winfo_x() + b_end.winfo_width() / 2
                y2 = b_end.winfo_y() + b_end.winfo_height() / 2
                
                self.win_line_coords = (x1, y1, x2, y2)
            
            if self.win_line_coords is None or step > steps:
                return
            
            x1, y1, x2, y2 = self.win_line_coords
            t = step / steps
            xe = x1 + (x2 - x1) * t
            ye = y1 + (y2 - y1) * t
            
            self.win_canvas.delete("win_line")
            line_width = max(3, int(6 * min(self.root.winfo_width(), self.root.winfo_height()) / 400))
            self.win_canvas.create_line(
                x1, y1, xe, ye,
                width=line_width,
                fill=self.theme["win_line"],
                capstyle="round",
                tags="win_line",
            )
            
            self.root.after(20, lambda: self.animate_win_line(combo, step + 1, steps))
        except Exception as e:
            logger.error(f"Error in animate_win_line: {e}")
    
    def end_game(self, result):
        """End game"""
        try:
            self.game_active = False
            
            if result == "HUMAN_WIN":
                self.status_label.config(text="You win!", fg=self.theme["status_win_fg"])
                self.play_sound("win")
                self.animate_win_line(self.last_win_combo)
                self.stats['wins'] += 1
                self.stats['total_games'] += 1
                messagebox.showinfo("Game Over", "You win!")
            elif result == "BOT_WIN":
                self.status_label.config(text="Bot wins!", fg=self.theme["status_lose_fg"])
                self.play_sound("lose")
                self.animate_win_line(self.last_win_combo)
                self.stats['losses'] += 1
                self.stats['total_games'] += 1
                messagebox.showinfo("Game Over", "Bot wins!")
            elif result == "DRAW":
                self.status_label.config(text="It's a draw!", fg=self.theme["status_draw_fg"])
                self.play_sound("draw")
                self.stats['draws'] += 1
                self.stats['total_games'] += 1
                messagebox.showinfo("Game Over", "It's a draw!")
            
            self.update_stats_display()
            self.save_current_game()
        except Exception as e:
            logger.error(f"Error in end_game: {e}")
    
    def reset_game(self):
        """Reset game"""
        try:
            self.board = [EMPTY] * 9
            for btn in self.buttons:
                btn.config(text="", bg=self.theme["button_bg"])
            self.game_active = True
            self.last_win_combo = None
            self.win_line_coords = None
            
            if self.win_canvas:
                self.win_canvas.delete("all")
                self.root.tk.call("lower", self.win_canvas._w)
            
            self.status_label.config(text="Your turn (X)", fg=self.theme["status_user_fg"])
            self.save_current_game()
            logger.info("Game reset")
        except Exception as e:
            logger.error(f"Error in reset_game: {e}")
    
    def find_best_move(self):
        """Find best move using minimax"""
        try:
            best_score = -float("inf")
            best_move = None
            
            for i in range(9):
                if self.board[i] == EMPTY:
                    self.board[i] = BOT
                    score = self.minimax(False)
                    self.board[i] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = i
            return best_move
        except Exception as e:
            logger.error(f"Error in find_best_move: {e}")
            return None
    
    def minimax(self, is_maximizing):
        """Minimax algorithm"""
        try:
            winner, _ = self.get_winner()
            if winner == BOT:
                return 1
            elif winner == HUMAN:
                return -1
            elif all(cell != EMPTY for cell in self.board):
                return 0
            
            if is_maximizing:
                best_score = -float("inf")
                for i in range(9):
                    if self.board[i] == EMPTY:
                        self.board[i] = BOT
                        score = self.minimax(False)
                        self.board[i] = EMPTY
                        best_score = max(score, best_score)
                return best_score
            else:
                best_score = float("inf")
                for i in range(9):
                    if self.board[i] == EMPTY:
                        self.board[i] = HUMAN
                        score = self.minimax(True)
                        self.board[i] = EMPTY
                        best_score = min(score, best_score)
                return best_score
        except Exception as e:
            logger.error(f"Error in minimax: {e}")
            return 0

def main():
    """Main entry point"""
    try:
        print(f"\n{APP_NAME} - Professional Edition\n")
        
        # Check if first run
        if SmartSetup.is_first_run():
            print("=" * 60)
            print("FIRST TIME SETUP REQUIRED")
            print("=" * 60)
            print("\nThis application needs to be installed with administrator privileges.")
            print("Please run this script as Administrator for first-time setup.\n")
            
            if is_admin():
                print("Administrator detected. Proceeding with installation...\n")
                if SmartSetup.full_setup():
                    print("\nInstallation completed successfully!")
                    print(f"Game installed to: {INSTALL_PATH}")
                    print("\nYou can now launch the game from:")
                    print("  - Desktop shortcut")
                    print("  - Start Menu")
                    print(f"  - Or run: {INSTALL_PATH / 'launch_game.bat'}\n")
                    input("Press Enter to launch the game...")
                else:
                    print("\nInstallation failed. Please check the error messages above.")
                    input("\nPress Enter to exit...")
                    sys.exit(1)
            else:
                print("ERROR: Administrator privileges required for installation!")
                print("\nPlease run this script as Administrator:")
                print("1. Right-click on Command Prompt or PowerShell")
                print("2. Select 'Run as administrator'")
                print("3. Navigate to this script's folder")
                print(f"4. Run: {Path(sys.argv[0]).name}\n")
                input("Press Enter to exit...")
                sys.exit(1)
        else:
            # Quick launch - already installed
            print("Quick launch mode - Starting game...\n")
            
            # Check for updates in background (non-intrusive)
            update_available = ApplicationInstaller.check_for_updates()
            if update_available:
                print(f"Note: Update available (version {update_available})")
                print("Please check for updates manually if needed.\n")
        
        # Launch game
        root = tk.Tk()
        app = TicTacToeBotApp(root)
        logger.info("Game launched successfully")
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Failed to launch game: {e}")
        print(f"\nError: {e}")
        print("\nCheck game.log for details")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
