from typing import Optional
from github import Github, Auth, GithubException
from beartype import beartype
from cachetools import TTLCache
import requests
from models.enums.GithubEventEnum import GithubEventEnum

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
        if not user:
            return []
        try:
            return user.get_repos()
        except GithubException as e:
            if e.status == 404:
                return []
            raise e

    @beartype
    def get_repository_files_structure(self, repo_full_name: str):
        """Get the files structure of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        if not repo:
            return []
        try:
            files = repo.get_git_tree("HEAD", recursive=True)
            return [file.path for file in files.tree]
        except GithubException as e:
            if e.status == 404:  # Not found, e.g., empty repo
                return []
            raise e

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
    def get_repo_commits(self, repo_full_name: str, author: Optional[str] = None):
        """Get the commits of a specific repository from GitHub."""
        repo = self.get_repository(repo_full_name)
        if not repo:
            return []
        try:
            return repo.get_commits(author=author) if author else repo.get_commits()
        except GithubException as e:
            if e.status == 404:
                return []
            raise e

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
        try:
            commits = repo.get_commits()
            if commits.totalCount > 0:
                return commits[0].commit.author.date
            return None
        except GithubException as e:
            if e.status == 404:
                return None
            raise e
        


@beartype
def get_event_payload(payload: dict, event_type: GithubEventEnum):
    if event_type == GithubEventEnum.CommitComment:
        comment_obj = payload.get("comment", {})
        return {
            "comment": comment_obj.get("body"),
            "url": comment_obj.get("html_url"),
        } if comment_obj.get("body") else {}

    elif event_type in (GithubEventEnum.Create, GithubEventEnum.Delete):
        return {
            "ref_type": payload.get("ref_type"),
            "ref": payload.get("ref"),
        } if payload.get("ref_type") or payload.get("ref") else {}

    elif event_type == GithubEventEnum.Fork:
        forkee = payload.get("forkee", {})
        parent_full_name = forkee.get("parent", {}).get("full_name") if "parent" in forkee else None
        return {
            "fork": forkee.get("full_name"),
            "parent": parent_full_name,
            "url": forkee.get("html_url"),
        } if forkee.get("full_name") else {}

    elif event_type == GithubEventEnum.Gollum:
        pages = payload.get("pages", [])
        page_titles = [page.get("title") for page in pages if "title" in page]
        return {"gollum_pages": page_titles} if page_titles else {}

    elif event_type == GithubEventEnum.IssueComment:
        comment_obj = payload.get("comment", {})
        return {
            "issue_comment": comment_obj.get("body"),
            "url": comment_obj.get("html_url"),
            "issue_url": payload.get("issue", {}).get("html_url"),
        } if comment_obj.get("body") else {}

    elif event_type == GithubEventEnum.Issues:
        issue_obj = payload.get("issue", {})
        return {
            "issue_title": issue_obj.get("title"),
            "state": issue_obj.get("state"),
            "url": issue_obj.get("html_url"),
        } if issue_obj.get("title") else {}

    elif event_type == GithubEventEnum.Member:
        member_obj = payload.get("member", {})
        return {
            "member": member_obj.get("login"),
            "action": payload.get("action"),
        } if member_obj.get("login") else {}

    elif event_type == GithubEventEnum.Public:
        repo = payload.get("repo", {})
        return {
            "public_repo": repo.get("name"),
        } if repo.get("name") else {}

    elif event_type == GithubEventEnum.PullRequest:
        pr_obj = payload.get("pull_request", {})
        return {
            "pull_request_title": pr_obj.get("title"),
            "number": pr_obj.get("number"),
            "state": pr_obj.get("state"),
            "url": pr_obj.get("html_url"),
        } if pr_obj.get("title") else {}

    elif event_type == GithubEventEnum.PullRequestReview:
        review_obj = payload.get("review", {})
        pr_obj = payload.get("pull_request", {})
        return {
            "pull_request_review": review_obj.get("body"),
            "state": review_obj.get("state"),
            "pr_url": pr_obj.get("html_url"),
        } if review_obj.get("body") else {}

    elif event_type == GithubEventEnum.PullRequestReviewComment:
        comment_obj = payload.get("comment", {})
        pr_obj = payload.get("pull_request", {})
        return {
            "pull_request_review_comment": comment_obj.get("body"),
            "url": comment_obj.get("html_url"),
            "pr_url": pr_obj.get("html_url"),
        } if comment_obj.get("body") else {}

    elif event_type == GithubEventEnum.PullRequestReviewThread:
        thread_obj = payload.get("thread", {})
        pr_obj = payload.get("pull_request", {})
        return {
            "pull_request_review_thread": thread_obj.get("body"),
            "pr_url": pr_obj.get("html_url"),
        } if thread_obj.get("body") else {}

    elif event_type == GithubEventEnum.Push:
        ref = payload.get("ref")
        commits = payload.get("commits", [])
        commit_msgs = [c.get("message") for c in commits if "message" in c]
        return {
            "push_ref": ref,
            "commit_messages": commit_msgs,
            "size": payload.get("size"),
        } if ref or commit_msgs else {}

    elif event_type == GithubEventEnum.Release:
        release_obj = payload.get("release", {})
        return {
            "release_name": release_obj.get("name"),
            "tag_name": release_obj.get("tag_name"),
            "url": release_obj.get("html_url"),
        } if release_obj.get("name") or release_obj.get("tag_name") else {}

    elif event_type == GithubEventEnum.Sponsorship:
        sponsorship_obj = payload.get("sponsorship", {})
        return {
            "sponsorship_tier": sponsorship_obj.get("tier", {}).get("name"),
            "sponsor": sponsorship_obj.get("sponsor", {}).get("login"),
            "sponsoree": sponsorship_obj.get("sponsorable", {}).get("login"),
        } if sponsorship_obj else {}

    elif event_type == GithubEventEnum.Watch:
        repo = payload.get("repo", {})
        return {
            "watch_repo": repo.get("name"),
        } if repo.get("name") else {}

    return {}

@beartype
def get_user_recent_activities(github_service: GitHubService, username: Optional[str] = None):
    user = github_service.get_user(username=username)
    url = f"https://api.github.com/users/{user.login}/events"
    header = {"Accept": "application/vnd.github+json"}
    if github_service.auth is not None:
        header.update({"Authorization": f"Bearer {github_service.auth.token}"})
    response = requests.get(url, headers=header)

    if response.status_code != 200:
        return []
    
    response_json = response.json()
    result = []

    for event in response_json:
        result.append(
            {
                "event_type": event["type"],
                "event_created_at": event["created_at"],
                "event_repo": event["repo"]["name"],
                "is_event_public": event["public"],
                "event_payload": get_event_payload(event["payload"], GithubEventEnum(event["type"])),
            }
        )
    return result


@beartype
def sort_repos_by_create_date(repos, reverse: bool = True):
    return sorted(list(repos), key=lambda repo: repo.created_at, reverse=reverse)

@beartype
def sort_repos_by_recent_update(repos, reverse: bool = True):
    return sorted(list(repos), key=lambda repo: repo.updated_at, reverse=reverse)
    
    