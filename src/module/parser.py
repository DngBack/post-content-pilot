from __future__ import annotations

from llama_cloud_services import LlamaParse
import nest_asyncio

from ..base import BaseModel
from ..base import BaseService

from ..settings import LlamaParserSettings

nest_asyncio.apply()


class LlamaParserInput(BaseModel):
    file_path: str


class LlamaParserOutput(BaseModel):
    content: str


class LlamaParserService(BaseService):
    settings: LlamaParserSettings

    @property
    def parser(self) -> LlamaParse:
        return LlamaParse(
            api_key=self.settings.api_key,  # can also be set in your env as LLAMA_CLOUD_API_KEY
            result_type="markdown",  # "markdown" and "text" are available
            num_workers=4,  # if multiple files passed, split in `num_workers` API calls
            verbose=True,
            language="en",  # Optionally you can define a language, default=en
        )

    def process(self, inputs: LlamaParserInput) -> LlamaParserOutput:
        # Load data
        documents = self.parser.load_data(inputs.file_path)
        return LlamaParserOutput(content=documents[0].get_content())
