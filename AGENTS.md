# AGENTS.md
> Source-of-truth for agent behavior in this repo. This is a community convention (not an official vendor spec). Follow these rules for all automated edits.

## Goals
- Stand up a production-viable **infrastructure baseline** with strict safety rails.
- Prefer **fast, low-cost** changes; escalate to deep reasoning only when required.
- Keep **diffs ≤ 300 lines** per PR; chunk large tasks into sequential PRs.

## Repository Profile
- Runtime: Python 3.11
- Packaging: `pyproject.toml` (PEP 621) + export `requirements.txt`
- Lint/Format/Type: ruff, black, mypy
- Tests: pytest + coverage + xdist
- DB: PostgreSQL 16 (+pgvector); Dev: SQLite (FTS5)
- CI: GitHub Actions
- Containers: Docker/Compose
- Paths of interest: `src/brand-nexus/`, `tests/`, `.github/workflows/`, `deployment/`

## Safety & Approvals
- **Approval Mode:** Default **suggest**; **auto-apply** only in these paths:  
  `src/brandnexus/{core,utils,models}/`, `tests/`, `.github/workflows/`, root meta files.  
  **Suggest-only** (never auto-apply): `security/`, `deployment/`, `database/`, `enterprise/`, `infra/`, `secrets/`.
- **Denylist (never run):** `rm -rf /`, package publishing, cloud credential changes, network calls to non-allowlisted domains.
- **Allowlist (shell):** `uv/poetry`, `pip`, `pytest`, `ruff`, `black`, `mypy`, `git`, `make`, `python -m` tools.
- Always include: command transcript, changed file list, and rationale.

## Router Hints (GPT-5)
- Default model: **fast path** (speed/low-cost).
- **Escalate to deep reasoning** only if:  
  (a) tests fail twice, (b) cross-module edit spans >3 directories, (c) security-sensitive files touched, (d) schema/migration planning required.
- Reasoning effort: `auto`; Verbosity: `medium`.

## Context Budget
- Prefer: `README`, this `AGENTS.md`, `pyproject.toml`, `Makefile`, nearest module files, recent commits (≤20 lines each).
- Avoid pulling large binaries/logs; summarize long files before proposing changes.

## Task Patterns

### P1 — **Scaffold & Structure** (Wave 1)
1. Create/confirm:
   - Root: `.gitignore`, `.editorconfig`, `.pre-commit-config.yaml`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `.env.example`
   - Packaging: `pyproject.toml` with ruff/black/mypy/pytest sections; export `requirements.txt` + `requirements-dev.txt`
   - Make: `Makefile` targets: `setup`, `lint`, `fmt`, `typecheck`, `test:unit`, `test:all`, `cov`, `build`
2. Modularize monolith into:

src/brand-nexus/
config/{settings.py,environment.py}
core/{indexer.py,classifier.py,search.py,database.py}
models/{document.py,schemas.py}
mcp/{server.py,tools.py,resources.py}
security/{auth.py,validation.py}
utils/{file_utils.py,helpers.py}

3. PR rules: ≤300 LOC, include tree diff and TODOs where stubs created.

### P2 — **Testing Baseline** (Wave 2)
1. Create `tests/` tree with `unit/`, `integration/`, `e2e/`, `performance/`, `fixtures/`.
2. Add initial unit tests for `indexer`, `classifier`, `search`, `database` (smoke tests OK).
3. Enforce coverage gate at **70%** initially; raise later.

### P3 — **CI & Quality** (Wave 3)
1. Add workflows:
- `lint.yml`: ruff + black --check + mypy
- `test.yml`: pytest (xdist), coverage upload (XML)
- `security.yml`: bandit on `src/`, secret scan (gitleaks/trufflehog), dependency audit (`pip-audit`)
2. Add `.github/ISSUE_TEMPLATE/*` and `PULL_REQUEST_TEMPLATE.md`.
3. Require “green CI” for merge.

### P4 — **Containers & Dev UX** (Wave 4)
1. `Dockerfile` (multi-stage: builder/runtime), `.dockerignore`.
2. `docker-compose.yml` with `app`, `db` (postgres), `vector` ext optional; healthchecks.
3. Entrypoints + `make compose:up`/`:down`.

### Next Waves (Short-term → Medium-term)
- **Security:** `security/SECURITY.md`, input validation, auth scaffolds.
- **Monitoring:** `health/health_checks.py`, basic `/healthz` later; add logging config (structlog).
- **DB Migrations:** `database/migrations/*` (Alembic), runner script.
- **Docs:** `docs/` skeleton mirroring guides listed in planning doc.

## Coding Conventions
- Style: follow `ruff.toml` + `black` defaults; type hints required in new/edited code.
- Commits: Conventional Commits; PR title prefix `[agent]`.
- Update/add tests with code changes; **no failing tests in PR**.

## Observability & Artifacts
- Include in PR comment: summary of change, commands run, test results, coverage %, and file change inventory.
- On failure: attach minimal reproduction (commands + error text).

## File Generation Matrix (initial must-create)
- Root: `.gitignore`, `.editorconfig`, `.pre-commit-config.yaml`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `.env.example`, `pyproject.toml`, `requirements*.txt`, `Makefile`
- Trees: `src/brandnexus/...` (as above), `tests/...`, `.github/workflows/{lint.yml,test.yml,security.yml}`, `Dockerfile`, `.dockerignore`, `docker-compose.yml`

## Examples & Templates (lightweight)
- Provide minimal content stubs (e.g., `settings.py` with `pydantic-settings`, `conftest.py` with tmp_path fixture, `Makefile` targets).
- Prefer smallest viable file contents that pass CI.

## Review Checklist (agent must verify before proposing merge)
- [ ] Diff ≤300 LOC and scoped to one wave.
- [ ] All CI jobs green; coverage ≥70% (if tests touched).
- [ ] No edits in suggest-only paths unless explicitly requested.
- [ ] PR body includes commands, outputs (truncated), and rationale.
