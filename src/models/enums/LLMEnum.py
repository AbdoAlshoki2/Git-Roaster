from enum import Enum

class LLMProviderEnum(Enum):
    OPENAI = "OPENAI"
    GROQ = "GROQ"


class LLMEnum(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class LLMURLEnum(Enum):
    OPENAI = "https://api.openai.com/v1/chat/completions"
    GROQ = "https://api.groq.com/openai/v1/chat/completions"
