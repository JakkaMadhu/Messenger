import os
from dotenv import load_dotenv

load_dotenv()

IP_ADDRESS = os.environ.get("IP_ADDRESS", "0.0.0.0")
PORT_NUMBER = int(os.environ.get("PORT", os.environ.get("PORT_NUMBER", 45999)))
EMAIL_NAME = os.environ.get("EMAIL_NAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
import urllib.parse

# Dynamic MongoDB Connection Configuration
MONGODB_USER = os.environ.get("MONGODB_USER")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
MONGODB_HOST = os.environ.get("MONGODB_HOST")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "db_messenger")
MONGODB_APP_NAME = os.environ.get("MONGODB_APP_NAME")

if MONGODB_USER and MONGODB_PASSWORD and MONGODB_HOST:
    # URL-encode credentials dynamically in case they contain special characters (e.g. '@', ':')
    encoded_user = urllib.parse.quote_plus(MONGODB_USER)
    encoded_password = urllib.parse.quote_plus(MONGODB_PASSWORD)
    
    # Construct SRV connection string for MongoDB Atlas
    MONGODB_URI = f"mongodb+srv://{encoded_user}:{encoded_password}@{MONGODB_HOST}/{MONGODB_DB_NAME}?retryWrites=true&w=majority"
    if MONGODB_APP_NAME:
        MONGODB_URI += f"&appName={MONGODB_APP_NAME}"
else:
    # Fallback to single connection string or local default
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/db_messenger")

