from typing import Optional
from github_service import GitHubService
from beartype import beartype


def build_user_data(github_service: GitHubService, username: Optional[str] = None):
    user = github_service.get_user(username=username)
    return {
        "username" : user.login,
        "bio" : user.bio,
        "profile_readme" : github_service.get_profile_special_repository(username=username)

    }