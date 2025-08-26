from typing import Optional
from services.github_service import GitHubService, get_user_recent_activities, sort_repos_by_recent_update
from beartype import beartype


@beartype
def get_repo_activities(github_service: GitHubService, repo_full_name: str, username: Optional[str] = None, repo_feasability: str = "public"):
    repo_commits = github_service.get_repo_commits(repo_full_name, author=username)
    activities = []
    if repo_commits:
        for commit in repo_commits:
            activities.append(
                {
                    "repo_feasability": repo_feasability,
                    "event_type": "PushEvent",
                    "event_created_at": commit.commit.author.date.isoformat(),
                    "event_repo": repo_full_name,
                    "event_payload": {
                        "push_ref": "refs/heads/main",
                        "commit_messages": [commit.commit.message]
                    }
                }
            )
    return activities

@beartype
def build_user_data(github_service: GitHubService, username: Optional[str] = None):
    user = github_service.get_user(username=username)
    profile_repo = github_service.get_profile_special_repository(username=username)
    readme = ""
    if profile_repo:
        readme = github_service.get_repo_readme(profile_repo.full_name)
    activities = get_user_recent_activities(github_service, username=username)

    if not activities:
        repos = github_service.get_repositories(username=username)
        sorted_repos = sort_repos_by_recent_update(repos)
        for repo in sorted_repos[:5]:
            repo_feasability = "private" if repo.private else "public"
            repo_activities = get_repo_activities(github_service, repo.full_name, username=user.login, repo_feasability=repo_feasability)
            activities.extend(repo_activities)

    return {
        "username": user.login,
        "name" : user.name,
        "bio": user.bio,
        "profile_readme": readme if readme else "",
        "activities": activities,
    }