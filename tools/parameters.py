import os
from dotenv import load_dotenv




load_dotenv()

class Config:
    OPENAI_KEY = os.environ.get("OPENAI_KEY")
    SOFIA_DEV_KEY = os.environ.get("SOFIA_DEV_KEY")
    SOFIA_DEV_URL = os.environ.get("SOFIA_DEV_URL")
    BOT_URL = os.environ.get("BOT_URL")


