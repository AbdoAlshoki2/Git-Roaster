from services.github_service import GitHubService, get_user_recent_activities
from services.data_builder import build_user_data
from helpers.config import get_settings
from llms.LLMProviderFactory import LLMProviderFactory

settings = get_settings()
github_service = GitHubService(settings.GITHUB_TOKEN)

user_data = build_user_data(github_service)

result = ""
for key, val in user_data.items():
    result += f"{key}: {val}\n"

provider = LLMProviderFactory.get_provider(settings)
provider.set_model(settings.LLM_MODEL_ID)

lst = [
    {
        "role": "system",
        "content": "You are expert github reviewer, review this user data and give me a summary of it"
    },
    {
        "role": "user",
        "content": result
    }
]

print(provider.generate_text(lst))
