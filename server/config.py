import os
from dotenv import load_dotenv

load_dotenv()

IP_ADDRESS = os.environ.get("IP_ADDRESS", "localhost")
PORT_NUMBER = int(os.environ.get("PORT_NUMBER", 45999))
EMAIL_NAME = os.environ.get("EMAIL_NAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/db_messenger")
