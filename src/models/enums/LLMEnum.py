from enum import Enum

class LLMProviderEnum(Enum):
    OPENAI = "OPENAI"
    GROQ = "GROQ"


class OpenAIEnum(Enum):
    USER = "user"
    ASSISTANT = "developer"
    SYSTEM = "system"

class GroqEnum(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"