from __future__ import annotations

from typing import Union

from openai import OpenAI
from ..base import BaseModel
from ..settings import OpenAISettings

from ..base import LLMBaseService


class OpenAIInput(BaseModel):
    user_prompt: str
    system_prompt: str = ""
    json_mode: bool = False


class OpenAIOutput(BaseModel):
    response: Union[str, dict]


class OpenAIService(LLMBaseService):
    settings: OpenAISettings

    @property
    def client(self) -> OpenAI:
        """
        Create a OpenAIService client

        Returns:
            OpenAIClient: OpenAI service client
        """
        return OpenAI(api_key=self.settings.openai_api_key)

    def process(self, inputs: OpenAIInput) -> OpenAIOutput:
        """
        Process user input using OpenAI

        Args:
            system_prompt (str): System prompt
            user_prompt (str): User prompt
            json_mode (bool): Whether to parse response as JSON

        Returns:
            OpenAIOutput: OpenAI response
        """
        response = self._inference_by_llm(
            inputs.system_prompt,
            inputs.user_prompt,
            inputs.json_mode,
        )
        return OpenAIOutput(response=response)

    def _inference_by_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        json_mode: bool,
    ) -> str:
        """
        Perform inference using the AWS Sonnet model.

        Args:
            user_prompt (str): The user's input prompt.
            system_prompt (str): The system's instructions.
            json_mode (bool): Whether to return the response in JSON format.

        Returns:
            Optional[Union[str, dict]]: The response from the model, either as a string or a JSON object.
        """
        if system_prompt:
            messages = self._get_system_users_messages(
                user_prompt,
                system_prompt,
            )
        else:
            messages = self._get_users_messages(user_prompt)

        response = self.client.chat.completions.create(
            model=self.settings.openai_model,
            stream=self.settings.openai_stream,
            max_tokens=self.settings.max_tokens,
            temperature=self.settings.temperature,
            top_p=self.settings.top_p,
            messages=messages,
        )
        response = response.choices[0].message.content
        if json_mode:
            return self.json_parse(response)
        return response

    def _get_users_messages(self, user_prompt: str) -> list[dict[str, str]]:
        """
        Process the input request and generate a response from AWS Sonnet.

        Args:
            inputs (AWSSonnetInput): The input data for processing.

        Returns:
            AWSSonnetOutput: The output containing the response from the model.
        """
        return [{"role": "user", "content": user_prompt}]

    def _get_system_users_messages(
        self,
        user_prompt: str,
        system_prompt: str,
    ) -> list[dict[str, str]]:
        """
        Create a system message for the AWS Sonnet model.

        Args:
            system_prompt (str): The system's instructions.

        Returns:
            list[dict]: A formatted system message list for the model.
        """
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
