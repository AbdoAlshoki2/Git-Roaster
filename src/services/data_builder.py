from typing import Optional
from services.github_service import GitHubService, get_user_recent_activities, sort_repos_by_recent_update
from beartype import beartype


@beartype
def get_repo_general_activities(
    github_service: GitHubService, 
    repo_full_name: str, 
    username: Optional[str] = None, 
    repo_feasability: str = "public"
):
    """Get general activity data for a repository."""
    repo_commits = github_service.get_repo_commits(repo_full_name, author=username)
    activities = []
    
    if repo_commits:
        for commit in repo_commits:
            activities.append({
                "repo_feasability": repo_feasability,
                "event_author": commit.author.login,
                "event_created_at": commit.commit.author.date.isoformat(),
                "event_repo": repo_full_name,
                "event_payload": {
                    "commit_messages": [commit.commit.message]
                }
            })
    return activities


@beartype
def get_detail_repo_commits(
    github_service: GitHubService, 
    repo_full_name: str
):
    """Get detailed commit history for a repository."""
    repo_commits = github_service.get_repo_commits(repo_full_name)
    activities = []
    
    if repo_commits:
        for commit in repo_commits:
            activities.append({
                "event_author": commit.author.login,
                "event_created_at": commit.commit.author.date.isoformat(),
                "event_repo": repo_full_name,
                "event_payload": {
                    "commit_messages": [commit.commit.message],
                    "changed_files_count": commit.files.totalCount,
                    "changed_lines_count": commit.stats.total
                }
            })
    return activities

@beartype
def build_user_data(
    github_service: GitHubService, 
    username: Optional[str] = None
):
    """Build comprehensive user data including profile and activities."""
    user = github_service.get_user(username=username)
    profile_repo = github_service.get_profile_special_repository(username=username)
    
    readme = github_service.get_repo_readme(profile_repo.full_name) if profile_repo else ""
    
    activities = get_user_recent_activities(github_service, username=username)
    
    if not activities:
        repos = github_service.get_repositories(username=username)
        sorted_repos = sort_repos_by_recent_update(repos)
        for repo in sorted_repos[:5]:
            repo_feasability = "private" if repo.private else "public"
            repo_activities = get_repo_general_activities(
                github_service, 
                repo.full_name, 
                username=user.login, 
                repo_feasability=repo_feasability
            )
            activities.extend(repo_activities)

    return {
        "username": user.login,
        "name": user.name,
        "bio": user.bio,
        "profile_readme": readme,
        "activities": activities,
    }


@beartype
def build_repo_data(
    github_service: GitHubService, 
    repo_full_name: str
):
    """Build comprehensive repository data including metadata and activities."""
    repo = github_service.get_repository(repo_full_name)
    
    return {
        "repo_full_name": repo_full_name,
        "repo_feasability": "private" if repo.private else "public",
        "repo_description": repo.description,
        "repo_readme": github_service.get_repo_readme(repo_full_name) or "",
        "repo_license": github_service.get_repo_license(repo_full_name),
        "activities": get_detail_repo_commits(github_service, repo_full_name),
        "stars_count": github_service.get_repo_stars_count(repo_full_name),
        "forks_count": github_service.get_repo_forks_count(repo_full_name),
        "languages": github_service.get_repo_languages(repo_full_name),
        "files_structure": github_service.get_repository_files_structure(repo_full_name)
    }