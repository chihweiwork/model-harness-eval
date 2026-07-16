# Repository Guidelines

Benchmarks "model × coding-agent harness × provider" with programmatic verifiers.
`bench/runner.py:main` is the real entrypoint; `run_bench.py` is `from bench.runner import main; main()`.
`pyproject.toml` also registers `run-bench` → `uv run run-bench <model>`.

## All commands need `uv run`

```bash
uv run pytest                              # verifier test suite
uv run pytest -v                           # verbose fixture tests
uv run python run_bench.py gemma4:12b       # full benchmark (default: 5 runs, all tiers, harness=pi)
uv run run-bench gemma4:12b --runs 1        # same via pyproject.toml entrypoint
uv run python fixtures/X1-officecli/.build.py   # one-time: generate X1 test assets
```

## Harness × Provider architecture

`bench/harnesses.py` defines `HARNESSES` dict. Each entry has `build` (cmd builder), `tools_supported` (bool), `extract` (stdout parser or None).
Providers: `("ollama", "litellm")` only. Map by env vars `OLLAMA_BASE_URL` / `LITELLM_BASE_URL` (defaults `localhost:11434` / `localhost:4000`).

| Harness | `tools_supported` | stdout extract | Litellm path | Ollama path |
|---------|-------------------|----------------|--------------|-------------|
| `pi` | Yes | None | `pi --provider litellm` + `~/.pi/agent/models.json` entry | `pi --provider ollama` |
| `opencode` | No | `extract_opencode_text()` from JSONL `{"type":"text"}` events | `opencode run --model litellm/<m>` | `opencode run --model ollama/<m>` |
| `copilot` | No | None | env `COPILOT_PROVIDER_BASE_URL` + `COPILOT_PROVIDER_API_KEY=sk-1234` | env `COPILOT_PROVIDER_BASE_URL` |
| `codex` | No | None | `OPENAI_BASE_URL=http://localhost:4000` + `codex exec -m <m>` | `codex exec --oss --local-provider ollama -m <m>` |

## Runner judgment pipeline (in this order)

1. Create tempdir, copy fixture (excludes dotfiles and `__pycache__`)
2. SHA-256 protected files → run harness non-interactively → SHA-256 again
3. TIMEOUT → TAMPERED (protected file changed) → EMPTY-* (no stdout, check file snapshot diff) → SILENT-PASS / PASS / FAIL
4. EMPTY-無痕 = no stdout + no file changes; EMPTY-有動工 = no stdout + files changed but verify fails
5. SILENT-PASS = no stdout but files changed AND verify passes

## Tasks

Defined in `bench/tasks.py` (`TASKS` list). Inline tasks use `setup` function; multi-file tasks use `fixture` dir. Smoke tasks (T1/T2/T4) have setup; T3 and R1 have no setup. `protected` files are SHA-256 checked.

| Tier | Tasks | Fixture dirs |
|------|-------|-------------|
| smoke | T1/T2/T3/T4 | inline setup (no dir) |
| complex | C1/C2/C3 | `fixtures/C1-crossfile-bug/`, etc. |
| long | L1 | `fixtures/L1-todo-spec/` |
| cli | X1/X2 | `fixtures/X1-officecli/`, `fixtures/X2-opencli/` |
| real | R1 | uses real `agent-browser` CLI, no fixture |

## Testing pattern (bidirectional verification)

`tests/conftest.py:copy_fixture` mirrors `bench.runner.prepare_dir` logic. Each fixture task has two tests:
- original → verify must **FAIL** (proves bug exists)
- apply `fix_*` from conftest → verify must **PASS** (proves verifier isn't broken)

Test files: `test_verify_complex.py` (C1/C2/C3), `test_verify_long.py` (L1), `test_verify_cli.py` (X1/X2).
Smoke tasks (T1-T4) have no dedicated test file.

## Known quirks

- Only `pi` enforces per-task `tools` restrictions. opencode/copilot/codex ignore `tools`; report marks them.
- X1 fixture has `.build.py` (runs once: `uv run python fixtures/X1-officecli/.build.py`). Dotfiles are excluded from copy, so models never see the build script.
- R1 requires `agent-browser` CLI installed (real tool, not a fixture).
- LiteLLM requires PostgreSQL: run `setup_litellm_db.sh` once, start with `./litellm.sh start`. Runner checks `/v1/models`; pass `--auto-start-litellm` to auto-start.
- `litellm_config.yaml` is gitignored; use `litellm_config.yaml.example` as template. All API keys default to `sk-1234`.
- No CI/CD (no `.github/`).
- Only dep: `pytest>=7.0`.
