from abc import ABC, abstractmethod

class LLMInterface(ABC):
    
    @abstractmethod
    def set_model(self, model_id: str):
        pass

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list = []):
        pass

    @abstractmethod
    def construct_prompt(self, prompt:str , role:str):
        pass