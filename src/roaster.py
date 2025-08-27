import json
from typing import Optional

from helpers.config import get_settings, Settings
from llms.LLMProviderFactory import LLMProviderFactory
from models.schemas.prompts import SYSTEM_PROMPT, REPO_REVIEW_PROMPT, USER_REVIEW_PROMPT, USER_MESSAGE_PROMPT
from services.data_builder import build_repo_data, build_user_data
from services.github_service import GitHubService


class GitRoaster:

    def __init__(self, settings: Settings = None):
        self.settings = settings or get_settings()
        self.github_service = GitHubService(self.settings.ROAST_GITHUB_TOKEN)
        self.llm_provider = LLMProviderFactory.get_provider(self.settings)
        self.llm_provider.set_model(self.settings.ROAST_LLM_MODEL_ID)
        self.chat_history = [
            {
                "role": self.llm_provider.enum_type.SYSTEM.value,
                "content": SYSTEM_PROMPT.substitute()
            }
        ]


    def _generate_review(self, content: str) -> str:
        """Generates a review using the configured LLM provider."""
        self.chat_history.append(
            {
                "role": self.llm_provider.enum_type.USER.value,
                "content": content
            }
        )
        response = self.llm_provider.generate_text(messages=self.chat_history)
        self.chat_history.append(
            {
                "role": self.llm_provider.enum_type.ASSISTANT.value,
                "content": response
            }
        )
        return response

    def roast_repo(self, repo_full_name: str) -> str:
        """Generates a review for a given GitHub repository."""
        print(f"Collecting data from: {repo_full_name}...")
        repo_data = build_repo_data(self.github_service, repo_full_name)
        prompt_content = REPO_REVIEW_PROMPT.substitute(repo_data=json.dumps(repo_data, indent=2))
        
        print("Roasting...")
        review = self._generate_review(prompt_content)
        return review

    def roast_user(self, username: Optional[str] = None) -> str:
        """Generates a review for a given GitHub user."""
        if not username:
            username = self.github_service.get_user().login

        print(f"Collecting data from: {username}...")
        user_data = build_user_data(self.github_service, username)
        prompt_content = USER_REVIEW_PROMPT.substitute(user_data=json.dumps(user_data, indent=2))

        print("Roasting...")
        review = self._generate_review(prompt_content)
        return review

    def normal_chat(self, message: str) -> str:
        """Generates a response for a given message using the configured LLM provider."""
        prompt_content = USER_MESSAGE_PROMPT.substitute(user_prompt=message)
        response = self._generate_review(prompt_content)
        return response
