import os
import sys
from dotenv import load_dotenv

# Dynamically locate the .env file path
if getattr(sys, 'frozen', False):
    # App is running as a packaged executable (.exe)
    base_dir = os.path.dirname(sys.executable)
else:
    # App is running in python interpreter (development)
    base_dir = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

# Server Connection settings
DEFAULT_HOST = os.environ.get("IP_ADDRESS", "zephyr.proxy.rlwy.net")
DEFAULT_PORT = int(os.environ.get("PORT_NUMBER", 28364))

# Modern Dark Theme Color Palette
COLOR_BG = "#121214"            # Dark background
COLOR_CARD = "#1e1e24"          # Container card backgrounds
COLOR_TEXT_PRIMARY = "#ffffff"  # Main text
COLOR_TEXT_MUTED = "#a0a0ab"    # Gray text
COLOR_ACCENT = "#6366f1"        # Indigo primary buttons/accents
COLOR_ACCENT_HOVER = "#4f46e5"  # Button hover state
COLOR_ERROR = "#ef4444"         # Error text
COLOR_SUCCESS = "#22c55e"       # Success indicator text

# Font Configurations
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_TOGGLE = ("Segoe UI", 12)
