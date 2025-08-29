import json
from typing import Optional

from helpers.config import get_settings, Settings
from models.enums.LLMEnum import LLMEnum
from services.llm_service import LLMService
from models.schemas.prompts import REPO_REVIEW_PROMPT, USER_REVIEW_PROMPT, USER_MESSAGE_PROMPT, SYSTEM_PROMPT
from services.data_builder import build_repo_data, build_user_data
from services.github_service import GitHubService


class GitRoaster:

    def __init__(self, settings: Settings = None):
        self.settings = settings or get_settings()
        self.github_service = GitHubService(self.settings.ROAST_GITHUB_TOKEN)
        self.llm_service = LLMService(self.settings)
        self.llm_service.set_model(self.settings.ROAST_LLM_MODEL_ID)
        self.chat_history = [
            self.llm_service.construct_prompt(SYSTEM_PROMPT.substitute(), LLMEnum.SYSTEM.value)
        ]


    def _generate_review(self, content: str) -> str:
        """Generates a review using the configured LLM provider."""

        self.chat_history.append(
            self.llm_service.construct_prompt(content, LLMEnum.USER.value)
        )
        response = self.llm_service.generate_text(messages=self.chat_history)

        self.chat_history.append(
            self.llm_service.construct_prompt(response, LLMEnum.ASSISTANT.value)
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
