"""Canonical benchmark fixture baseline derived from Git history.

The fixture blobs below were introduced by commit 5bf3e09 and remained
unchanged in 525e7a1, where the original-FAIL/fixed-PASS pytest contracts were
added.  Keeping the blob ids here makes fixture contamination fail closed.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


BASELINE_COMMIT = "5bf3e09"

# Git blob ids from commits 5bf3e09 and 525e7a1 (identical in both trees).
BASELINE_BLOBS = {
    "C2-refactor-green/a.py": "b589ff42d02ea664b08fec58b07dac4213f7f98b",
    "C2-refactor-green/b.py": "c5808e95c8a89dbd95f452c24debeab752aca361",
    "C2-refactor-green/test_ab.py": "627f34649ff76735fe0689624d3a2dc440f98adc",
    "C3-misleading-trace/config.py": "894ee95735880633d312eb2d1ed7a7c27d574b27",
    "C3-misleading-trace/main.py": "96881539c871e17fc021ff5cf9bea7f8c5ef3c44",
    "C3-misleading-trace/server.py": "3633592b1b42ea062baa0275855bdeeb92bc3ad4",
    "C3-misleading-trace/settings.json": "8a51a41620ec08f8d7df3edfb9f4fa1fa3afe91f",
    "L1-todo-spec/SPEC.md": "4d0a5f6bd2c3f30a69458bd40cd36d2c7e45618e",
    "L1-todo-spec/test_todo.py": "b903887985600e24bed566c001e3bfac70ceaf35",
    "X1-officecli/.build.py": "6191105e184362a8a8129ee5cb88109004cc458a",
    "X1-officecli/bin/officecli": "9042501f6ec1a217fa060e89816a150068afa673",
    "X1-officecli/report.docx": "72aa6723bb13f2a4ad8d456620b162f8943d7bee",
}

FORBIDDEN_GENERATED_FILES = {
    "C2-refactor-green/utils.py",
    "L1-todo-spec/todo.py",
    "L1-todo-spec/todos.json",
    "X1-officecli/report.txt",
}


class FixtureBaselineError(RuntimeError):
    """Raised when source fixtures no longer match the historical baseline."""


class SourceFixtureTampered(RuntimeError):
    """Raised when a benchmark subprocess changes source fixtures."""


def git_blob_id(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def _repo_root(fixtures: Path) -> Path:
    return fixtures.resolve().parent


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise FixtureBaselineError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def tracked_fixture_entries(fixtures: Path, source: str = "HEAD") -> dict[str, str]:
    repo = _repo_root(fixtures)
    output = _git(repo, "ls-tree", "-rz", source, "--", fixtures.name)
    prefix = f"{fixtures.name}/"
    entries = {}
    for record in output.split("\0"):
        if not record or "\t" not in record:
            continue
        meta, name = record.split("\t", 1)
        if not name.startswith(prefix):
            continue
        mode = meta.split(" ", 1)[0]
        entries[name[len(prefix):]] = mode
    return entries


def tracked_fixture_files(fixtures: Path, source: str = "HEAD") -> set[str]:
    return set(tracked_fixture_entries(fixtures, source))


def reset_fixture_tree(fixtures: Path, source: str = "HEAD") -> list[str]:
    """Restore tracked fixtures from Git and remove untracked generated files."""
    repo = _repo_root(fixtures)
    fixtures.mkdir(parents=True, exist_ok=True)
    tracked = tracked_fixture_entries(fixtures, source)
    changed: list[str] = []

    for relative, mode in sorted(tracked.items()):
        path = fixtures / relative
        data = subprocess.run(
            ["git", "show", f"{source}:{fixtures.name}/{relative}"],
            cwd=repo,
            capture_output=True,
            check=False,
        )
        if data.returncode:
            raise FixtureBaselineError(
                data.stderr.decode(errors="replace").strip()
                or f"cannot read {source}:{fixtures.name}/{relative}"
            )
        before = path.read_bytes() if path.exists() and path.is_file() else None
        path.parent.mkdir(parents=True, exist_ok=True)
        if before != data.stdout:
            path.write_bytes(data.stdout)
            changed.append(relative)
        current_mode = path.stat().st_mode
        current_exec = current_mode & 0o111
        desired_exec = 0o111 if mode == "100755" else 0
        if current_exec != desired_exec:
            desired_mode = ((current_mode & 0o777) ^ current_exec) | desired_exec
            path.chmod(desired_mode)
            if relative not in changed:
                changed.append(relative)

    for path in sorted(fixtures.rglob("*"), reverse=True):
        if path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass
            continue
        relative = str(path.relative_to(fixtures))
        if relative in tracked:
            continue
        path.unlink()
        changed.append(relative)

    return sorted(changed)


def validate_fixture_baseline(fixtures: Path) -> str:
    errors = []
    for relative, expected in BASELINE_BLOBS.items():
        path = fixtures / relative
        if not path.is_file():
            errors.append(f"missing {relative}")
            continue
        actual = git_blob_id(path.read_bytes())
        if actual != expected:
            errors.append(f"modified {relative} ({actual} != {expected})")
        # Git records only the executable bit, not group/other write policy.
        if path.stat().st_mode & 0o111:
            errors.append(f"unexpected executable bit: {relative}")
    for relative in sorted(FORBIDDEN_GENERATED_FILES):
        if (fixtures / relative).exists():
            errors.append(f"generated file present: {relative}")
    if errors:
        detail = "\n  - ".join(errors)
        raise FixtureBaselineError(
            f"fixture baseline {BASELINE_COMMIT} validation failed:\n  - {detail}"
        )
    digest = hashlib.sha256()
    for relative, blob in sorted(BASELINE_BLOBS.items()):
        digest.update(f"{relative}\0{blob}\n".encode())
    return digest.hexdigest()


def snapshot_fixture_tree(fixtures: Path) -> dict[str, str]:
    snapshot = {}
    for path in fixtures.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        content = hashlib.sha256(path.read_bytes()).hexdigest()
        mode = path.stat().st_mode & 0o777
        snapshot[str(path.relative_to(fixtures))] = f"{mode:o}:{content}"
    return snapshot


def assert_fixture_tree_unchanged(
    fixtures: Path, before: dict[str, str]
) -> None:
    after = snapshot_fixture_tree(fixtures)
    if after == before:
        return
    changed = sorted(
        relative
        for relative in set(before) | set(after)
        if before.get(relative) != after.get(relative)
    )
    raise SourceFixtureTampered(
        "benchmark subprocess modified source fixtures: " + ", ".join(changed)
    )
