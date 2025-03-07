from __future__ import annotations

from tqdm import tqdm
from typing import Optional

from src.module import OpenAIInput
from src.module import OpenAIService

from src.module import LlamaParserInput
from src.module import LlamaParserService

from src.settings import OpenAISettings
from src.settings import LlamaParserSettings

from ...base import BaseService
from ...base import BaseModel

from ..utils import tokenize
from ..utils import chunk_on_delimiter


class ContentSummarizationInput(BaseModel):
    file_path: str


class ContentSummarizaitonOutput(BaseModel):
    content_sum: str


class ContentSummarizationService(BaseService):
    openai_settings: OpenAISettings
    llamaparser_settings: LlamaParserSettings

    @property
    def parser(self) -> LlamaParserService:
        return LlamaParserService(settings=self.llamaparser_settings)
    
    @property
    def openai(self) -> OpenAIService:
        return OpenAIService(settings=self.openai_settings)

    def process(self, inputs: ContentSummarizationInput) -> ContentSummarizaitonOutput:
        markdown_content = self._parser(inputs.file_path)
        content_sum = self._summarize(markdown_content)
        return ContentSummarizaitonOutput(content_sum=content_sum)

    def _parser(self, file_path: str) -> str:
        markdown_content = self.parser.process(
            inputs=LlamaParserInput(file_path=file_path)
        )
        return markdown_content.content
    
    def _summarize(self, markdown_content: str,
                detail: float = 0,
                model: str = 'gpt-4-turbo',
                additional_instructions: Optional[str] = None,
                minimum_chunk_size: Optional[int] = 500,
                chunk_delimiter: str = ".",
                summarize_recursively=False,
                verbose=False) -> str:
        max_chunks = len(chunk_on_delimiter(markdown_content, minimum_chunk_size, chunk_delimiter, model_name=model))
        min_chunks = 1
        num_chunks = int(min_chunks + detail * (max_chunks - min_chunks))

        document_length = len(tokenize(markdown_content, model_name=model))
        chunk_size = max(minimum_chunk_size, document_length // num_chunks)
        text_chunks = chunk_on_delimiter(markdown_content, chunk_size, chunk_delimiter, model_name=model)

        system_message_content = """
        You are an AI assistant specializing in text analysis and extracting the most important key points from input content. 
        Ensure that the extracted points are concise, clear, and maintain the core meaning of the original text. 
        If the content has a structure, preserve the logical flow between ideas. Highlight important keywords whenever relevant. 
        If numerical data is present, include the most critical figures. 
        Avoid adding assumptions or information that is not explicitly stated in the original text.
        """
        if additional_instructions is not None:
            system_message_content += f"\n\n{additional_instructions}"

        accumulated_summaries = []
        for chunk in tqdm(text_chunks):
            if summarize_recursively and accumulated_summaries:
                accumulated_summaries_string = '\n\n'.join(accumulated_summaries)
                user_message_content = f"""
                Previous summaries:\n\n{accumulated_summaries_string}\n\n
                Text to summarize next:\n\n{chunk}
                Summary:
                """
            else:
                user_message_content = chunk

            response = self.openai.process(
                OpenAIInput(
                    user_prompt=user_message_content,
                    system_prompt=system_message_content,
                )
            )
            accumulated_summaries.append(response.response)

        final_summary = '\n\n'.join(accumulated_summaries)
        return final_summary
