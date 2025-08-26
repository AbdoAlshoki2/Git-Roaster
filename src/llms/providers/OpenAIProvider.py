from ..LLMInterface import LLMInterface
from models.enums.LLMEnum import OpenAIEnum
from openai import OpenAI
from typing import Optional
from beartype import beartype

class OpenAIProvider(LLMInterface):
    @beartype
    def __init__(self, api_key: str, base_url: Optional[str] =None):

        self.api_key = api_key
        self.base_url = base_url if base_url and len(base_url) else None 

        self.client = OpenAI(
            api_key=api_key,
            base_url=self.base_url
        )
        self.model_id = None
        self.enum_type = OpenAIEnum

    @beartype
    def set_model(self, model_id: str):
        self.model_id = model_id

    @beartype
    def generate_text(self, messages: list):

        if not self.client or not self.model_id:
            return None
        
        completion = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages
        )

        if not completion or not completion.choices or not completion.choices[0].message:
            return None

        return completion.choices[0].message.content

    @beartype
    def construct_prompt(self, prompt:str , role:str):
        return {
            "role": role,
            "content": prompt
        }
        