from services.github_service import GitHubService, get_user_recent_activities
from services.data_builder import build_user_data, build_repo_data
from helpers.config import get_settings
from llms.LLMProviderFactory import LLMProviderFactory
from models.schemas.prompts import SYSTEM_PROMPT, USER_REVIEW_PROMPT, REPO_REVIEW_PROMPT
import json

settings = get_settings()
github_service = GitHubService(settings.GITHUB_TOKEN)

repo_data = build_repo_data(github_service, "AbdoAlshoki2/mini-rag-study")

provider = LLMProviderFactory.get_provider(settings)
provider.set_model(settings.LLM_MODEL_ID)

lst = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT.substitute()
    },
    {
        "role": "user",
        "content": REPO_REVIEW_PROMPT.substitute(repo_data=json.dumps(repo_data))
    }
]


print(provider.generate_text(lst))
