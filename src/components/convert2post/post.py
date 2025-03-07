from __future__ import annotations

from src.module import OpenAIInput
from src.module import OpenAIService
from src.settings import OpenAISettings

from ...base import BaseModel
from ...base import BaseService
from .prompt import SYSTEM_PROMPT
from .prompt import USER_PROMPT


class ConvertPostInput(BaseModel):
    summary_content: str
    tone: str
    target_platform: str


class ConvertPostOutput(BaseModel):
    post: str


class ConvertPostService(BaseService):
    openai_settings: OpenAISettings

    @property
    def openai(self) -> OpenAIService:
        return OpenAIService(settings=self.openai_settings)

    def process(self, inputs: ConvertPostInput) -> ConvertPostOutput:
        # Create user prompt
        user_prompt = USER_PROMPT.format(
            summary_content=inputs.summary_content,
            tone=inputs.tone,
            target_platform=inputs.target_platform,
        )
        content = self.openai.process(
            OpenAIInput(
                user_prompt=user_prompt,
                system_prompt=SYSTEM_PROMPT,
            ),
        )
        return ConvertPostOutput(post=content.response)
