from dotenv import load_dotenv
import os

load_dotenv()

class Settings():
    origins: list = ["*"]
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))
    database_url: str = os.getenv("DATABASE_URL", "")
    openai: str = os.getenv("OPENAI_APIKEY","")
    anthropic: str = os.getenv("ANTHROPIC_APIKEY","")
    broker_url: str = os.getenv("broker_url", "")
    result_backend: str = os.getenv("result_backend", "")
settings = Settings()
