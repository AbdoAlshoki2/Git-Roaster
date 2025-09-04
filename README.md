# Git-Roaster

This is my first Command Line Interface (CLI) tool in python — it roasts GitHub users and repositories.  
I built it mainly to learn more about the GitHub API and CLI tools, so I ended up creating this sarcastic little thing you can run in the terminal. It queries GitHub data and then roasts it mercilessly.  

As the name suggests, this tool lets you review GitHub repos or users in a unique, funny, and sarcastic way. You can also just chat with it to follow up on the previous roast.  

---

## Installation

If you already have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed, you can install Git-Roaster directly:

```bash
uv tool install git+https://github.com/AbdoAlshoki2/Git-Roaster.git
```

Alternatively, you can use [pipx](https://github.com/pypa/pipx):
```bash
pip install pipx
pipx install git+https://github.com/AbdoAlshoki2/Git-Roaster.git
```

---

## Setup

This tool uses different APIs and tokens to work.
First, you need to get an LLM provider API key. Right now, this tool supports GroqAPI and OpenAI interfaces.

You can get the API key from [Groq](https://console.groq.com/), [OpenAI](https://openai.com/api/), or any other LLM provider that supports OpenAI API (e.g. Ollama or OpenRouter).

To set the keys for the LLM provider, you can use the `roast config` command:
```bash
roast config --set-llm-provider openai --set-api-key <your-api-key> 
# or
roast config --set-llm-provider groq --set-api-key <your-api-key>
```

> Notice the `--set-api-key` flag requires to set the llm provider, by default it will use GroqAPI.

Also you can set the model id from any of the above providers, check [GroqAPI models](https://console.groq.com/docs/rate-limits) or [OpenAI models](https://platform.openai.com/docs/models):

```bash
roast config --set-model-id <your-model-id>
```

> Same as api key, this flag works on the default provider (if not set).

For OpenAI (and its variants), you can set a custom base URL. For example, with OpenRouter:
```bash
roast config --set-base-url https://api.openrouter.ai
```

So to fully configure OpenRouter, you could run:
```bash
roast config --set-llm-provider openai --set-api-key <your-api-key> --set-model-id <your-model-id> --set-base-url https://api.openrouter.ai
```

Since this tool fetches data from the GitHub API, you also need a GitHub token.
You can generate one from [GitHub](https://github.com/settings/tokens). Without it, the tool only works on publicly available data.

```bash
roast config --set-github-token <your-github-token>
```

Or just use interactive setup for all keys:

```bash
roast config
```

You can also work with Ollama locally by setting the base URL for OpenAI to `http://localhost:11434` and the model id to the model you want to use, or you can go through this [Colab notebook](https://colab.research.google.com/drive/171w_OF-Xn_eZJPgT206rT95XPiKiRnmK?usp=sharing) (or any free cloud compute) as a server.

---

## Usage

This tool has 3 main commands:

- `roast repo <repo-full-name>`: Roasts a GitHub repository based on its full name.
- `roast user <username>`: Roasts a GitHub user based on their username.
- `roast msg <message>`: Roasts a message based on the message content.

**This tool does not access the files content except the README.md file**

---

## Examples

```bash
roast repo AbdoAlshoki2/Git-Roaster
roast user AbdoAlshoki2
roast msg "Hello, how are you?"
```

For the `roast user`, if you set a GitHub token, you can omit the username to roast your own profile:

```bash
roast user  # roast your own profile
```

For the `roast repo`, by default it uses the default branch of the repository, but you can specify a branch with `--branch` or `-b` flag.

```bash
roast repo AbdoAlshoki2/Git-Roaster --branch "main"
roast repo AbdoAlshoki2/Git-Roaster -b "main"
```

Also this tool support interactive mode, by running `roast` without any arguments you will enter interactive mode:

```bash
roast
Review your Github repo or user profile in a unique, funny, and sarcastic way (type 'exit' or 'quit' to exit interactive mode).
git-roaster >>
```

---
## Notes:
- This tool reviews commits, file structure, README files, and recent activity of a user or repo. It won’t work on private repositories unless you provide a GitHub token.

- This tool does not access the files content (except the `README.md` file).

- It’s limited by your LLM provider’s capabilities. Long contexts may fail with errors like `Error: Failed to get a response from the LLM service. Check your API key and network.`

- Fetching GitHub data may take time depending on repository size.

