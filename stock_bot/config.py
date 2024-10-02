import os
from dotenv import load_dotenv

# Load environment variables from the .env file (one folder up)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

class Config:
    # Bot token from the .env file
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    # Define the project root path (one folder up)
    PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')

    # Database configuration (SQLite path relative to the project root)
    DB_URL = f"sqlite:///{os.path.join(PROJECT_ROOT, 'telegram_bot.db')}"
