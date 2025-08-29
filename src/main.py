import typer
from roaster import GitRoaster
from typing_extensions import Annotated
from typing import Optional
from helpers.setup import check_and_setup, setup_config

app = typer.Typer(
    name="git-roaster",
    help="Review your Github repo or user profile in a unique, funny, and sarcastic way.",
    add_completion=False
)


@app.command(help="Roast a GitHub repository.")
def repo(
    repo_full_name: Annotated[str, typer.Argument(..., help="The full name of the repository (e.g., 'AbdoAlshoki2/Git-Roaster').")]
):
    """Roasts a GitHub repository based on its full name."""
    try:
        check_and_setup()
        roaster = GitRoaster()
        review = roaster.roast_repo(repo_full_name)
        print(review)
    except Exception as e:
        print(f":x: [bold red]An error occurred:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command(help="Roast a GitHub user.")
def user(
    username: Annotated[Optional[str], typer.Argument(..., help="The username of the GitHub user.")] = None
):
    """Roasts a GitHub user based on their username."""
    try:
        check_and_setup()
        roaster = GitRoaster()
        review = roaster.roast_user(username)
        print(review)
    except Exception as e:
        print(f":x: [bold red]An error occurred:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command(help="Configure Git-Roaster settings.")
def setup():
    """Run the configuration setup."""
    setup_config()


if __name__ == "__main__":
    app()
