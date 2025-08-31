from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print
from rich.markdown import Markdown

with Progress(SpinnerColumn(), TextColumn("{task.description}")) as progress:
    task = progress.add_task("Initializing Git-Roaster...", total=None)

    import typer
    from roaster import GitRoaster
    from typing_extensions import Annotated
    from typing import Optional
    from helpers.cli_setup import (
        ensure_config_exists, setup_config, update_github_token, update_llm_provider, update_api_key, update_model_id, update_base_url, save_config
    )

    ensure_config_exists()
    roaster = GitRoaster()

    app = typer.Typer(
        name="git-roaster",
        help="Review your Github repo or user profile in a unique, funny, and sarcastic way.",
        add_completion=False
    )

    progress.update(task, description="Initialization complete!", completed=1)


def with_spinner(task_name: str, fn, *args):
    """Run a function with a spinner, return its result."""
    try:
        with Progress(SpinnerColumn(), TextColumn("{task.description}")) as progress:
            task = progress.add_task(task_name, total=None)
            result = fn(*args)
            progress.update(task, description="Done!", completed=1)
        
        print()
        try:
            print(Markdown(result))
        except Exception:
            print(result)
        print()
        return result
    except (ConnectionError, ValueError) as e:
        print(f":x: [bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f":x: [bold red]An unexpected error occurred:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command(help="Roast a GitHub repository.")
def repo(
    repo_full_name: Annotated[
        str,
        typer.Argument(..., help="The full name of the repository (e.g., 'AbdoAlshoki2/Git-Roaster').")
    ],
    branch: Annotated[
        Optional[str],
        typer.Option("--branch", "-b", help="The branch to roast. Defaults to the repository's default branch.")
    ] = None
):
    """Roasts a GitHub repository based on its full name."""
    with_spinner("Collecting & roasting repo data...", roaster.roast_repo, repo_full_name, branch)


@app.command(help="Roast a GitHub user.")
def user(
    username: Annotated[
        Optional[str],
        typer.Argument(..., help="The username of the GitHub user.")
    ] = None
):
    """Roasts a GitHub user based on their username."""
    with_spinner("Collecting & roasting user data...", roaster.roast_user, username)


@app.command(help="Configure Git-Roaster settings.")
def config(
    github_token: Annotated[
        Optional[str],
        typer.Option("--set-github-token", help="Set the GitHub token.")
    ] = None,
    llm_provider: Annotated[
        Optional[str],
        typer.Option("--set-llm-provider", help="Set the LLM provider (e.g., OPENAI, GROQ).")
    ] = None,
    api_key: Annotated[
        Optional[str],
        typer.Option("--set-api-key", help="Set the API key for the current LLM provider.")
    ] = None,
    model_id: Annotated[
        Optional[str],
        typer.Option("--set-model-id", help="Set the LLM model ID.")
    ] = None,
    base_url: Annotated[
        Optional[str],
        typer.Option("--set-base-url", help="Set the base URL for OpenAI.")
    ] = None,
):
    """Run the configuration setup and reload the roaster instance."""
    settings = roaster.settings
    if github_token:
        settings = update_github_token(settings, github_token)
    if llm_provider:
        settings = update_llm_provider(settings, llm_provider)
    if api_key:
        settings = update_api_key(settings, api_key)
    if model_id:
        settings = update_model_id(settings, model_id)
    if base_url:
        settings = update_base_url(settings, base_url)
    
    if any([github_token, llm_provider, api_key, model_id, base_url]):
        save_config(settings)
    else:
        setup_config(settings.model_dump())

    roaster.reload_config()


if __name__ == "__main__":
    app()
