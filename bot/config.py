import os

from dotenv import load_dotenv

def getenv_or_error(name: str, default: str = None, required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and value is None:
        raise EnvironmentError(f"Required environment variable '{name}' is not set.")
    return value

load_dotenv(
    dotenv_path='.env'
)

# Bot

BOT_TOKEN = getenv_or_error("BOT_TOKEN", required=True)
