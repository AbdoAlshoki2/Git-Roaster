import json
from typing import Optional

from helpers.settings import get_settings, Settings
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
    
    def _append_to_history(self, role, content):
        """Append message to history and enforce max size."""
        self.chat_history.append(
            self.llm_service.construct_prompt(content, role)
        )
    
    def reload_config(self):
        """Reloads configuration and re-initializes services if settings have changed."""
        new_settings = get_settings()

        if self.settings.ROAST_GITHUB_TOKEN != new_settings.ROAST_GITHUB_TOKEN:
            self.github_service = GitHubService(new_settings.ROAST_GITHUB_TOKEN)

        llm_settings_changed = any([
            self.settings.ROAST_LLM_PROVIDER != new_settings.ROAST_LLM_PROVIDER,
            self.settings.ROAST_DEFAULT_API_KEY != new_settings.ROAST_DEFAULT_API_KEY,
            self.settings.ROAST_LLM_MODEL_ID != new_settings.ROAST_LLM_MODEL_ID,
            self.settings.ROAST_OPENAI_BASE_URL != new_settings.ROAST_OPENAI_BASE_URL,
        ])

        if llm_settings_changed:
            self.llm_service = LLMService(new_settings)
            self.llm_service.set_model(new_settings.ROAST_LLM_MODEL_ID)

            self.chat_history = [
                self.llm_service.construct_prompt(SYSTEM_PROMPT.substitute(), LLMEnum.SYSTEM.value)
            ] if new_settings.ROAST_LLM_PROVIDER != self.settings.ROAST_LLM_PROVIDER else self.chat_history

        self.settings = new_settings


    def _generate_review(self, content: str) -> str:
        """Generates a review using the configured LLM provider."""
        self._append_to_history(LLMEnum.USER.value, content)
        response = self.llm_service.generate_text(messages=self.chat_history)

        if not response:
            raise ConnectionError("Failed to get a response from the LLM service. Check your API key and network.")

        self._append_to_history(LLMEnum.ASSISTANT.value, response)
        return response

    def roast_repo(self, repo_full_name: str, branch: Optional[str] = None) -> str:
        """Generates a review for a given GitHub repository."""
        try:
            repo_data = build_repo_data(self.github_service, repo_full_name, branch=branch)
        except AttributeError:
            raise ValueError(f"Could not find repository '{repo_full_name}'. Please check that the name is correct and that you have access to it.")

        prompt_content = REPO_REVIEW_PROMPT.substitute(repo_data=json.dumps(repo_data, indent=2))

        
        review = self._generate_review(prompt_content)
        return review

    def roast_user(self, username: Optional[str] = None) -> str:
        """Generates a review for a given GitHub user."""
        if not username:
            try:
                username = self.github_service.get_user().login
            except Exception:
                 raise ValueError("Username is required when not authenticated. Please provide a username or set a GitHub token.")
        try:
            user_data = build_user_data(self.github_service, username)
        except AttributeError:
            raise ValueError(f"Could not find user '{username}'. Please check that the username is correct.")

        prompt_content = USER_REVIEW_PROMPT.substitute(user_data=json.dumps(user_data, indent=2))
        review = self._generate_review(prompt_content)
        return review

    def normal_chat(self, message: str) -> str:
        """Generates a response for a given message using the configured LLM provider."""
        prompt_content = USER_MESSAGE_PROMPT.substitute(user_prompt=message)
        response = self._generate_review(prompt_content)
        return response
