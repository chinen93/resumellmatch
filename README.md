# ResumeLLMatch

ResumeLLMatch is a Python prototype for augmenting resume and job description matching with a local LLM workflow.
It combines STAR-format experience data, job description extraction, and local Ollama LLM inference to help evaluate and rewrite candidate STAR entries.

## What it does

- Parses and caches job descriptions using a local LLM prompt.
- Imports STAR metadata and entries from CSV files and stores them in SQLite.
- Matches job descriptions against STAR records with an LLM-driven score and explanation.
- Rewrites STAR experience entries into resume-style bullet points.
- Stores LLM prompts and responses in a local cache to avoid duplicate calls.

## Architecture

### Core components

- `src/main.py` - application logic and handlers.
  - `handle_job()` reads a job description, parses it with the LLM, caches parsed output, and matches it against STAR content.
  - `handle_star()` imports STAR metadata and entries from CSV files into storage.
  - `handle_resume()` is a placeholder for future resume processing.

- `main.py` - CLI entrypoint using `click`.
  - `--job` runs `handle_job`
  - `--star` runs `handle_star`
  - `--resume` runs `handle_resume`

- `src/llm/client/ollama.py` - Ollama LLM wrapper.
- `src/llm/prompt/` - prompt templates for the LLM.
- `src/storage/` - data persistence with SQLAlchemy and SQLite.
- `src/data_ingestion/` - helpers for loading text, JSON, and CSV files.
- `src/core/` - domain dataclasses and import/processing logic.

## Storage and data

- Production database: `output/storage.db`
- Test database: `output/test_storage.db`

### Important storage tables

- `job_descriptions`
- `job_descriptions_parsed`
- `star_metadatas`
- `star_entries`
- `skills`
- `llm_cache`
- `matches`

## Setup

1. Create the Python environment and install dependencies:

```sh
python -m pip install -r requirements.txt
```

2. Ensure Ollama is installed and available in your environment.
   The project uses the `ollama` Python package and expects a local Ollama runtime.

3. Add environment variables via `.env` if needed.
   The application reads settings from `config/.env` by default.

## Usage

Run the CLI from the project root:

```sh
python main.py --star
python main.py --job
python main.py --resume
```

## Database migrations

This project includes Alembic migrations for schema changes.

Generate a migration script:

```sh
alembic revision --autogenerate -m "Add a description of your change"
```

Apply migrations:

```sh
alembic upgrade head
```

Rollback one revision:

```sh
alembic downgrade -1
```

## Tests

Run the built-in test suite with Python's unittest:

```sh
python -m unittest discover tests
```
