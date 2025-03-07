from __future__ import annotations

from typing import Optional

from src.module import LlamaParserInput
from src.module import LlamaParserService
from src.module import OpenAIInput
from src.module import OpenAIService
from src.settings import LlamaParserSettings
from src.settings import OpenAISettings
from tqdm import tqdm

from ...base import BaseModel
from ...base import BaseService
from ..utils import chunk_on_delimiter
from ..utils import tokenize


class ContentSummarizationInput(BaseModel):
    file_path: str


class ContentSummarizaitonOutput(BaseModel):
    content_sum: str


class ContentSummarizationService(BaseService):
    """
    Service for processing and summarizing content.
    Attributes:
        openai_settings (OpenAISettings): Configuration settings for OpenAI API.
        llamaparser_settings (LlamaParserSettings): Configuration settings for the LlamaParser service.
    """
    openai_settings: OpenAISettings
    llamaparser_settings: LlamaParserSettings

    @property
    def parser(self) -> LlamaParserService:
        """
        Returns an instance of LlamaParserService with the provided settings.
        """
        return LlamaParserService(settings=self.llamaparser_settings)

    @property
    def openai(self) -> OpenAIService:
        """
        Returns an instance of OpenAIService with the provided settings.
        """
        return OpenAIService(settings=self.openai_settings)

    def process(self, inputs: ContentSummarizationInput) -> ContentSummarizaitonOutput:
        """
        Main processing function that orchestrates the summarization process.

        Args:
            inputs (ContentSummarizationInput): The input containing file path.

        Returns:
            ContentSummarizaitonOutput: The summarized output.
        """
        markdown_content = self._parser(inputs.file_path)
        content_sum = self._summarize(markdown_content)
        return ContentSummarizaitonOutput(content_sum=content_sum)

    def _parser(self, file_path: str) -> str:
        """
        Parses the file and extracts markdown content.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The extracted markdown content.
        """
        markdown_content = self.parser.process(
            inputs=LlamaParserInput(file_path=file_path),
        )
        return markdown_content.content

    def _summarize(
        self, markdown_content: str,
        detail: float = 0,
        model: str = 'gpt-4-turbo',
        additional_instructions: Optional[str] = None,
        minimum_chunk_size: Optional[int] = 500,
        chunk_delimiter: str = '.',
        summarize_recursively=False,
        verbose=False,
    ) -> str:
        """
        Summarizes the given markdown content using OpenAI API.

        Args:
            markdown_content (str): The content to be summarized.
            detail (float): Level of detail in the summary (0 to 1).
            model (str): The OpenAI model to use for summarization.
            additional_instructions (Optional[str]): Extra instructions for the summarization.
            minimum_chunk_size (Optional[int]): Minimum chunk size for content splitting.
            chunk_delimiter (str): Delimiter used for splitting text into chunks.
            summarize_recursively (bool): Whether to summarize recursively.
            verbose (bool): Whether to display progress.

        Returns:
            str: The summarized content.
        """
        max_chunks = len(
            chunk_on_delimiter(
                markdown_content, minimum_chunk_size, chunk_delimiter, model_name=model,
            ),
        )
        min_chunks = 1
        num_chunks = int(min_chunks + detail * (max_chunks - min_chunks))

        document_length = len(tokenize(markdown_content, model_name=model))
        chunk_size = max(minimum_chunk_size, document_length // num_chunks)
        text_chunks = chunk_on_delimiter(
            markdown_content, chunk_size, chunk_delimiter, model_name=model,
        )

        system_message_content = """
        You are an AI assistant specializing in text analysis and extracting the most important key points from input content.
        Ensure that the extracted points are concise, clear, and maintain the core meaning of the original text.
        If the content has a structure, preserve the logical flow between ideas. Highlight important keywords whenever relevant.
        If numerical data is present, include the most critical figures.
        Avoid adding assumptions or information that is not explicitly stated in the original text.
        """
        if additional_instructions is not None:
            system_message_content += f'\n\n{additional_instructions}'

        accumulated_summaries = []
        for chunk in tqdm(text_chunks):
            if summarize_recursively and accumulated_summaries:
                accumulated_summaries_string = '\n\n'.join(
                    accumulated_summaries,
                )
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
                ),
            )
            accumulated_summaries.append(response.response)

        final_summary = '\n\n'.join(accumulated_summaries)
        return final_summary
