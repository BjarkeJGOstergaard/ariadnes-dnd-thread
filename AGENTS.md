# AGENTS.md

Instructions for AI coding agents (and humans) working in this repository.
Read this file before changing anything.

## Project in one paragraph

Ariadne's Dnd Thread is an open-source D&D tool and a public portfolio project.
It has three planned areas: **Campaign Memory** (RAG over Obsidian Markdown notes,
answers with source citations), **Encounter Analysis** (simulator and DM sparring),
and **Analytics** (Power BI / Databricks). Only **Campaign Memory** is in scope
for now. Do not start work on the other two areas.

The owner wants to understand the key concepts, not just receive working code.
When a design choice matters, explain the why briefly in the PR description.

## Stop and ask first

Stop and ask the owner before doing any of the following. Do not decide these
yourself, even if the task seems to require it:

- **Scope changes**: adding features, endpoints or areas that the issue/spec does not mention.
- **Architecture changes**: new services, new top-level folders, changing the monorepo or workspace layout, changing how components talk to each other.
- **Major technical choices**: a new framework, database, ORM, embedding model, LLM provider, queue, or any dependency that shapes the design.
- **Anything that deletes data**: `docker compose down -v`, dropping tables, rewriting git history.
- **Anything touching secrets or real campaign data.**

If the spec is ambiguous, ask one question at a time and offer a recommended answer.
Facts that can be looked up in the repo should be looked up, not asked.

## Working agreement

- One task at a time, tied to one GitHub issue and, where it exists, one spec in `specs/`.
- Flow: issue -> spec (`specs/*.md`) -> owner approves -> implement -> tests -> PR -> CI -> owner reviews the diff -> merge.
- Tests are mandatory. No behaviour change without a test that proves it.
- Keep changes small and reviewable. Do not mix refactors with features.
- Do not add dependencies casually. Every new dependency needs a one-line reason.
- Verify before claiming something works: run the command, read the output.

## Repository layout

```
backend/          Python backend (own pyproject.toml, src/ariadnes_dnd_thread/, tests/)
frontend/         React + TypeScript UI (kept simple)
specs/            Markdown specs: the precise technical contract per task
infrastructure/   Infra files (Postgres init scripts now, Terraform later)
scripts/          Helper scripts
.github/workflows/  CI
docker-compose.yml  Local services (PostgreSQL + pgvector)
pyproject.toml    Root: declares the uv workspace only
uv.lock           Single lockfile for the whole workspace (committed)
```

The Python package name is `ariadnes_dnd_thread`. The old working name `dnd-ai` is retired.

## Stack

- Python 3.12, managed with **uv** (uv workspace; `backend/` is the member).
- **FastAPI** as the API boundary.
- **PostgreSQL 17 + pgvector** (`pgvector/pgvector:pg17`) for relational data, documents, chunks and embeddings. No SQLite, no Chroma/Qdrant.
- **Alembic** will own the schema. The Postgres init script only enables the `vector` extension.
- **Ruff** for linting and formatting, **pytest** for tests.
- LLMs sit behind a small `LLMProvider` abstraction (Ollama, OpenAI, Anthropic, ...). Application code calls `llm.generate(...)` and never a vendor SDK directly.
- No large custom agent framework. Domain logic lives in plain functions and services (for example `search_campaign`); agents call them as tools. MCP is an integration layer built later, on top of the real functionality.

## Commands

Local services:

```bash
cp .env.example .env              # first time only, then set your own POSTGRES_PASSWORD
docker compose up -d              # start PostgreSQL + pgvector
docker compose ps                 # should show the db container as healthy
docker compose exec db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
docker compose down               # stop (keeps data)
```

Python (these apply once the backend skeleton exists):

```bash
uv sync                                        # install dependencies
uv run --package backend pytest                # run tests
uv run ruff check .                            # lint
uv run ruff format .                           # format
uv add --package backend <dependency>          # add a backend dependency
```

Never run `docker compose down -v` without asking: it deletes the database volume.

## Conventions

- Type hints on all public functions. Prefer small, pure functions that are easy to test.
- Configuration comes from environment variables, loaded from `.env` in development. Never hard-code credentials, URLs or model names.
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`).
- Work on a branch and open a PR. Do not push directly to `main` once CI exists.
- Pin infrastructure versions deliberately (for example the Postgres image tag). Do not use `latest`.
- Work inside the WSL filesystem, not under `/mnt/c`.

## Secrets and privacy

- `.env` is git-ignored and must stay that way. Only `.env.example` is committed, with placeholder values.
- Never print, log, commit or paste real passwords or API keys.
- The public demo uses the 5e SRD (CC-BY) and an **invented** campaign.
- The owner's real campaign notes and homebrew stay private. Never commit them, never send them to a cloud LLM. `LLMProvider` must be able to force a local model for real campaign data.

## Design rules that must not be broken

- **Citations are the point.** Every answer from Campaign Memory must trace back to its source chunks. Do not ship an answer path that drops sources.
- **Simulation is code, not an LLM.** Encounter simulation (later) must be a reproducible Monte Carlo with a seeded RNG. An agent may propose inputs and interpret results, but the numbers come from the simulator.
- **Retrieval quality is measured.** A small evaluation set (questions with expected sources) will be kept in the repo. Changes to chunking, embeddings or retrieval should be checked against it.

## Definition of done

A task is done when: the code matches the spec, tests pass locally and in CI, `ruff` is clean, no secrets are in the diff, docs are updated if behaviour changed, and the PR description explains the key decisions in plain language.
