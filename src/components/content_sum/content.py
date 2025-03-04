from __future__ import annotations

from src.module import OpenAIInput
from src.module import OpenAIService
from src.module import LlamaParserInput
from src.module import LlamaParserService

from src.settings import OpenAISettings
from src.settings import LlamaParserSettings

from ...base import BaseService
from ...base import BaseModel


class ContentSummarizationInput(BaseModel):
    file_path: str


class ContentSummarizaitonOutput(BaseModel):
    content_sum: str


class ContentSummarizationService(BaseService):
    openai_settings: OpenAISettings
    llamaparser_settings: LlamaParserSettings

    @property
    def summarizer(self) -> OpenAIService:
        return OpenAIService(self.openai_settings)

    @property
    def parser(self) -> LlamaParserService:
        return LlamaParserService(self.llamaparser_settings)

    def process(self, inputs: ContentSummarizationInput) -> ContentSummarizaitonOutput:
        pass
