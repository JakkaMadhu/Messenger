import os
from dotenv import load_dotenv

load_dotenv()

# Server Connection settings
DEFAULT_HOST = os.environ.get("IP_ADDRESS", "192.168.1.34")
DEFAULT_PORT = int(os.environ.get("PORT_NUMBER", 45999))

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
