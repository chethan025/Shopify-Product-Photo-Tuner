import os
from dotenv import load_dotenv

load_dotenv()

SHOP = os.getenv("SHOP")
TOKEN = os.getenv("TOKEN")
API_VERSION = os.getenv("API_VERSION")
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", 0.6))