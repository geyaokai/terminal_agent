import os
from dotenv import load_dotenv


def load_api_key() -> str:
    """Load GOOGLE_API_KEY from .env and environment.

    Raises a RuntimeError if not found.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("错误：请在 .env 文件中设置 GOOGLE_API_KEY。")
    return api_key


def get_model_name(default: str = "gemini-2.5-flash") -> str:
    """Get model name from env, falling back to default."""
    return os.getenv("GEMINI_MODEL", default)
