# Ariadne's Dnd Thread

> Follow the thread back to the source.

An open-source D&D tool that answers questions about your campaign **and shows
exactly where each answer came from**. Named after Ariadne's thread: every
answer carries citations that lead back to the original notes.

**Status:** early development. The foundation (repo, tooling, local database) is in place.
No application code yet.

## What it will do

1. **Campaign Memory** (current focus): index your Obsidian Markdown notes (world, NPCs, places, history, session logs) and ask questions in natural language, for example *"What do we know about the merchant Alrik?"*. Answers cite the notes they are based on.
2. **Encounter Analysis** (later): estimate difficulty and character-death risk with a reproducible Monte Carlo simulator, and spar with an AI about enemies and tactics. Simulation is deterministic code; the AI proposes and interprets.
3. **Analytics** (later): encounter and campaign analytics with Power BI and Databricks.

## Design goals

- **Local-first.** Runs on your own machine with local models (for example via Ollama). Cloud models are optional.
- **Private by default.** Real campaign data can be forced onto local models only.
- **Provider-agnostic.** LLMs sit behind a small `LLMProvider` interface.
- **Citations everywhere.** No answer without sources.
- **Measured quality.** Retrieval is checked against a small evaluation set.

## Tech stack

| Layer | Choice |
| --- | --- |
| Language / tooling | Python 3.12, [uv](https://docs.astral.sh/uv/) workspace |
| API | FastAPI |
| Database | PostgreSQL 17 + [pgvector](https://github.com/pgvector/pgvector) |
| Migrations | Alembic (planned) |
| Frontend | React + TypeScript (planned, intentionally simple) |
| Local services | Docker Compose |
| CI/CD | GitHub Actions (planned) |
| Cloud demo | Azure, defined with Terraform (planned) |

## Repository layout

```
backend/            Python backend (own pyproject.toml, src/ariadnes_dnd_thread/, tests/)
frontend/           React + TypeScript UI
specs/              Technical specs, one per task
infrastructure/     Postgres init scripts now, Terraform later
scripts/            Helper scripts
.github/workflows/  CI
docker-compose.yml  Local PostgreSQL + pgvector
```

## Getting started

Prerequisites: Docker (with Compose), [uv](https://docs.astral.sh/uv/), and Git.
On Windows, use WSL 2 with Docker Desktop's WSL integration and work inside the WSL filesystem.

```bash
git clone https://github.com/BjarkeJGOstergaard/ariadnes-dnd-thread.git
cd ariadnes-dnd-thread

cp .env.example .env        # then edit .env and set your own POSTGRES_PASSWORD
docker compose up -d        # start PostgreSQL with pgvector
docker compose ps           # the db service should report "healthy"
```

Quick check that pgvector works:

```bash
docker compose exec db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  -c "SELECT '[1,2,3]'::vector <-> '[1,2,4]'::vector;"
```

The result should be `1`.

Good to know:

- `POSTGRES_PASSWORD` and the init scripts only apply the **first** time the volume is created. Changing them later requires `docker compose down -v`, which deletes all database data.
- If port 5432 is already in use, change `POSTGRES_PORT` in `.env`.
- The database only listens on `127.0.0.1`.

## Roadmap

- [x] Repo, uv workspace layout, monorepo structure
- [x] Docker Compose with PostgreSQL + pgvector
- [ ] FastAPI backend skeleton (health endpoint, tests, settings, DB connection check)
- [ ] Obsidian ingestion (chunking, embeddings, incremental re-indexing)
- [ ] RAG with citations and an evaluation set
- [ ] Simple React UI (question box, answer, sources)
- [ ] CI with GitHub Actions
- [ ] Agent tools and MCP integration
- [ ] Encounter simulator
- [ ] Analytics (Power BI, Databricks)
- [ ] Azure deployment as a demo

## Working with AI agents

Conventions and the rules for when an agent must stop and ask are in [AGENTS.md](AGENTS.md).

## Demo data and licensing

The public demo uses material from the 5e System Reference Document and an invented campaign.
The owner's real campaign notes and homebrew are never part of this repository.

This work includes material taken from the System Reference Document 5.1 ("SRD 5.1")
by Wizards of the Coast LLC, available at
<https://dnd.wizards.com/resources/systems-reference-document>.
The SRD 5.1 is licensed under the Creative Commons Attribution 4.0 International License,
available at <https://creativecommons.org/licenses/by/4.0/legalcode>.

The code in this repository is released under the [MIT License](LICENSE).
