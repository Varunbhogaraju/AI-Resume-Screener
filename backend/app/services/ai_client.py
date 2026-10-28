from openai import OpenAI

from backend.app.core.config import settings


client = OpenAI(
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)