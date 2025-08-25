from typing import Optional
from github import Github, Auth, GithubException, PaginatedList
from beartype import beartype
from cachetools import TTLCache

class GitHubService:
    @beartype
    def __init__(self, token: Optional[str] = None):
        """Initialize the GitHubService with an optional token."""
        if token == "":
            raise ValueError("Token cannot be empty string")

        self.auth = Auth.Token(token=token) if token else None
        self.github_client = Github(auth=self.auth)
        self.user_cache = TTLCache(maxsize=100, ttl=3600)
        self.repo_cache = TTLCache(maxsize=100, ttl=3600)

    @beartype
    def clear_cache(self):
        """Clear all caches manually"""
        self.user_cache.clear()
        self.repo_cache.clear()
    
    @beartype
    def authenticate(self, token: str):
        """Authenticate with GitHub using a token."""
        if not token:
            raise ValueError("Token cannot be empty")
        
        self.auth = Auth.Token(token=token)
        self.github_client = Github(auth=self.auth)
        self.user_cache = TTLCache(maxsize=100, ttl=3600)
        self.repo_cache = TTLCache(maxsize=100, ttl=3600)

    @beartype
    def get_user(self, username: Optional[str] = None):
        """Get a user's information from GitHub, using a cache to avoid redundant API calls."""
        cache_key = username if username else "_authenticated_user"

        if cache_key in self.user_cache:
            return self.user_cache[cache_key]
        try:
            if self.auth is not None:
                user = self.github_client.get_user(login=username) if username else self.github_client.get_user()
            else:
                if not username:
                    raise ValueError("Username required for unauthenticated connection")
                user = self.github_client.get_user(login=username)
            self.user_cache[cache_key] = user
            return user
        except GithubException as e:
            if e.status == 404:
                return None  # User not found
            raise e
    
    @beartype
    def get_repository(self, repo_full_name: str):
        """Get a specific repository from GitHub, using a cache to avoid redundant API calls."""
        if repo_full_name in self.repo_cache:
            return self.repo_cache[repo_full_name]
        try:
            repo = self.github_client.get_repo(repo_full_name)
            self.repo_cache[repo_full_name] = repo
            return repo
        except GithubException as e:
            if e.status == 404:
                return None
            raise e
    
    @beartype
    def get_repositories(self, username: Optional[str] = None):
        """Get all repositories of a specific user from GitHub."""
        user = self.get_user(username=username)
        return user.get_repos() if user else []

    @beartype
    def get_repository_files_structure(self, repo_full_name: str):
        """Get the files structure of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        if not repo:
            return []
        files = repo.get_git_tree("HEAD", recursive=True)
        return [file.path for file in files.tree]

    @beartype
    def get_repository_file_content(self, repo_full_name: str, file_path: str):
        """Get the content of a specific file from a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        if not repo:
            return None
        try:
            file_content = repo.get_contents(file_path)
            return file_content.decoded_content.decode("utf-8")
        except GithubException as e:
            if e.status == 404:
                return None
            raise e

    @beartype
    def get_profile_special_repository(self, username: Optional[str] = None):
        """Get the profile repository (username/username) of a specific user from GitHub."""
        user = self.get_user(username=username)
        if not user:
            return None
        username = user.login
        return self.get_repository(f"{username}/{username}")
        
    @beartype
    def get_repo_commits(self, repo_full_name: str):
        """Get the commits of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        return repo.get_commits() if repo else []

    @beartype
    def get_repo_stars_count(self, repo_full_name: str):
        """Get the stars count of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        return repo.stargazers_count if repo else 0
    
    @beartype
    def get_repo_forks_count(self, repo_full_name: str):
        """Get the fork count of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        return repo.forks_count if repo else 0

    @beartype
    def get_repo_languages(self, repo_full_name: str):
        """Get the languages of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        return repo.get_languages() if repo else {}

    @beartype
    def get_repo_readme(self, repo_full_name: str) -> Optional[str]:
        """Get the README content of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        if not repo:
            return None
        try:
            readme = repo.get_readme()
            return readme.decoded_content.decode("utf-8")
        except GithubException as e:
            if e.status == 404:
                return None
            raise e

    @beartype
    def get_repo_license(self, repo_full_name: str):
        """Get the license of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        if not repo:
            return None
        try:
            return repo.get_license()
        except GithubException as e:
            if e.status == 404:
                return None
            raise e

    @beartype
    def get_repo_last_commit_date(self, repo_full_name: str):
        """Get the date of the last commit of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        if not repo:
            return None
        commits = repo.get_commits()
        if commits.totalCount > 0:
            return commits[0].commit.author.date
        return None
        


@beartype
def sort_repos_by_create_date(repos, reverse: bool = True):
    return sorted(list(repos), key=lambda repo: repo.created_at, reverse=reverse)

@beartype
def sort_repos_by_recent_update(repos, reverse: bool = True):
    return sorted(list(repos), key=lambda repo: repo.updated_at, reverse=reverse)
    
    