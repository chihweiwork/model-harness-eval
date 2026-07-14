# Repository Guidelines

## Project Structure & Module Organization

This repository evaluates model, harness, and provider combinations with programmatic checks. `run_bench.py` is the thin CLI entry point. Core code lives in `bench/`: `runner.py` handles execution and reporting, `tasks.py` defines benchmark tasks and verifiers, and `harnesses.py` registers harness command builders. `tests/` contains pytest coverage for verifier correctness. `fixtures/` holds task projects copied into temporary workspaces during runs. `results/` stores generated Markdown benchmark reports. LiteLLM configuration starts from `litellm_config.yaml.example`; keep real credentials out of the repo.

## Build, Test, and Development Commands

- `pytest`: run the verifier test suite configured in `pyproject.toml`.
- `pytest -v`: show each fixture verification case.
- `python3 run_bench.py gemma4:12b`: run the default benchmark matrix for one model.
- `python3 run_bench.py gemma4:12b --runs 1 --tier complex,cli`: run a shorter targeted benchmark.
- `python3 run_bench.py gemma4:12b --harness pi,opencode,copilot,codex`: compare harnesses.
- `./litellm.sh start`: start the LiteLLM proxy before `--provider litellm` runs.

## Coding Style & Naming Conventions

Use Python 3.10+ and standard-library-first code. Follow the existing style: 4-space indentation, small functions, explicit `Path` usage for filesystem work, and task dictionaries with stable keys such as `id`, `tier`, `verify`, `timeout`, `tools`, and `prompt`. Name verifiers `verify_<task>` and setup helpers `setup_<task>`. Keep runner output and report fields stable unless tests and docs are updated together.

## Testing Guidelines

Tests use pytest. Fixture-based tasks should have two-way tests: the original fixture must fail verification, and the applied reference fix must pass. Add reference fix helpers in `tests/conftest.py`, then add tier-specific tests such as `test_verify_complex.py`, `test_verify_long.py`, or `test_verify_cli.py`. Run `pytest` before using new tasks in benchmarks.

## Commit & Pull Request Guidelines

Recent history uses Conventional Commit prefixes such as `feat:`, `fix:`, `refactor:`, `docs:`, and `chore:`. Keep commits focused and mention affected harnesses, providers, or task tiers when relevant. Pull requests should include a short purpose statement, verification output, any generated report paths, and notes for configuration-sensitive changes such as LiteLLM, Ollama, or external CLI requirements.

## Security & Configuration Tips

Do not commit real `litellm_config.yaml`, cloud credentials, local model secrets, or generated temp workspaces. Prefer `.example` files for shareable configuration.
