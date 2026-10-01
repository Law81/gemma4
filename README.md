# Python Project Skeleton

Reusable Python 3.13 project template with uv, Docker, Compose, Git, tests, and linting.

## Customize

1. Replace `project-name` in `pyproject.toml` and `Dockerfile`.
2. Rename `src/project_name` and update the import path in `pyproject.toml`.
3. Replace the example entry point in `src/project_name/main.py`.
4. Add runtime dependencies under `[project].dependencies`.

## Local development

You do not need uv installed on the host to run the project with Docker:

```powershell
docker compose up --build
```

For local development, install uv with the included bootstrap script, then create the environment:

```powershell
.\install-uv.ps1
uv sync
```

Run the application, tests, and checks:

```powershell
uv run project-name
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

After changing dependencies, regenerate and commit `uv.lock`:

```powershell
uv lock
uv sync
```

## Docker

To avoid Hugging Face Hub rate limits, create a read token in your Hugging Face
account, copy `.env.example` to `.env`, and replace the placeholder with your
token. Docker Compose passes `HF_TOKEN` to the application automatically. Keep
`.env` private; it is excluded from Git.

Build and run the production-style image:

```powershell
docker build -t project-name:local .
docker run --rm project-name:local
```

Build and run with Compose:

```powershell
docker compose up --build
```

The image contains uv, uses Python 3.13, and installs the project without requiring uv on the host. The Compose service reads optional values from `.env`.

## Git

```powershell
git init
git add .
git commit -m "Initial project skeleton"
```

Do not commit `.env` files or credentials.