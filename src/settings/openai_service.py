from __future__ import annotations

from ..base import BaseModel


class OpenAISettings(BaseModel):
    openai_api_key: str
    openai_model: str
    openai_embedding: str
    openai_stream: bool
    max_tokens: int
    temperature: float
    top_p: float
