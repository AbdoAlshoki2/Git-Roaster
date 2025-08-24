from typing import Optional
from github import Github, Auth
from beartype import beartype

class GitHubService:
    @beartype
    def __init__(self, token: Optional[str] = None):
        """Initialize the GitHubService with an optional token."""
        if token == "":
            raise ValueError("Token cannot be empty string")

        self.auth = Auth.Token(token=token) if token else None
        self.github_client = Github(auth=self.auth)
        self.user_cache = {}
        self.repo_cache = {}

    @beartype
    def clear_cache(self):
        """Clear all caches manually"""
        self.user_cache = {}
        self.repo_cache = {}
    
    @beartype
    def authenticate(self, token: str):
        """Authenticate with GitHub using a token."""
        if not token:
            raise ValueError("Token cannot be empty")
        
        self.auth = Auth.Token(token=token)
        self.github_client = Github(auth=self.auth)
        self.user_cache = {}
        self.repo_cache = {}

    @beartype
    def get_user(self, username: Optional[str] = None):
        """Get a user's information from GitHub, using a cache to avoid redundant API calls."""
        cache_key = username if username else "_authenticated_user"

        if cache_key in self.user_cache:
            return self.user_cache[cache_key]

        if self.auth is not None:
            user = self.github_client.get_user(login=username) if username else self.github_client.get_user()
        else:
            if not username:
                raise ValueError("Username required for unauthenticated connection")
            user = self.github_client.get_user(login=username)
        
        self.user_cache[cache_key] = user
        return user
    
    @beartype
    def get_repository(self, repo_full_name: str):
        """Get a specific repository from GitHub, using a cache to avoid redundant API calls."""
        if repo_full_name in self.repo_cache:
            return self.repo_cache[repo_full_name]
        
        repo = self.github_client.get_repo(repo_full_name)
        self.repo_cache[repo_full_name] = repo
        return repo
    
    @beartype
    def get_repositories(self, username: Optional[str] = None):
        """Get all repositories of a specific user from GitHub."""
        return self.get_user(username=username).get_repos()

    @beartype
    def get_repository_files_structure(self, repo_full_name: str):
        """Get the files structure of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        files = repo.get_git_tree("HEAD", recursive=True)
        file_names = [file.path for file in files.tree]
        return file_names

    @beartype
    def get_repository_file_content(self, repo_full_name: str, file_path: str):
        """Get the content of a specific file from a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        return repo.get_contents(file_path).decoded_content.decode("utf-8")

    @beartype
    def get_profile_repository(self, username: Optional[str] = None):
        """Get the profile repository (username/username) of a specific user from GitHub."""
        user = self.get_user(username=username)
        username = user.login
        return self.get_repository(username + "/" + username)
        
    