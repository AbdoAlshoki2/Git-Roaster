from ..LLMInterface import LLMInterface
from models.enums.LLMEnum import GroqEnum
from groq import Groq
from typing import Optional
from beartype import beartype

class GroqProvider(LLMInterface):
    @beartype
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Groq(api_key=api_key)
        self.model_id = None
        self.enum_type = GroqEnum
    
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