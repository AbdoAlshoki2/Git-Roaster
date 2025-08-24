from typing import Optional
from github import Github, Auth


class GitHubService:
    def __init__(self, token: Optional[str] = None):
        if token == "":
            raise ValueError("Token cannot be empty string")
        self.auth = Auth.Token(token=token) if token else None
        self.github_client = Github(auth=self.auth)
    
    def authenticate(self, token: str):
        if not token:
            raise ValueError("Token cannot be empty")
        self.auth = Auth.Token(token=token)
        self.github_client = Github(auth=self.auth)

    def get_user(self, username: Optional[str] = None):
        if self.auth is not None:
            return self.github_client.get_user(login=username) if username else self.github_client.get_user()
        else:
            if not username:
                raise ValueError("Username required for unauthenticated connection")
            return self.github_client.get_user(login=username)