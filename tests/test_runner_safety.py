import shutil
import stat
import subprocess

import pytest

from bench import FIXTURES
from bench.fixture_baseline import (
    FixtureBaselineError,
    SourceFixtureTampered,
    assert_fixture_tree_unchanged,
    reset_fixture_tree,
    snapshot_fixture_tree,
    validate_fixture_baseline,
)
from bench.harnesses import HARNESSES
from bench.runner import select_tasks
from bench.tasks import DEFAULT_TIERS


def test_historical_fixture_baseline_is_valid():
    fingerprint = validate_fixture_baseline(FIXTURES)
    assert len(fingerprint) == 64


def test_fixture_baseline_rejects_solved_fixture(tmp_path):
    copied = tmp_path / "fixtures"
    shutil.copytree(FIXTURES, copied)
    (copied / "L1-todo-spec" / "todo.py").write_text("# already solved\n")
    with pytest.raises(FixtureBaselineError, match="generated file present"):
        validate_fixture_baseline(copied)


def test_source_fixture_snapshot_detects_mutation(tmp_path):
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    source = fixtures / "sample.txt"
    source.write_text("before")
    before = snapshot_fixture_tree(fixtures)
    source.write_text("after")
    with pytest.raises(SourceFixtureTampered, match="sample.txt"):
        assert_fixture_tree_unchanged(fixtures, before)


def test_reset_fixture_tree_restores_committed_tree(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "bench@example.test"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Bench Test"],
        cwd=tmp_path,
        check=True,
    )
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    tracked = fixtures / "task.py"
    tracked.write_text("original\n")
    tracked.chmod(0o755)
    subprocess.run(["git", "add", "fixtures/task.py"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "baseline"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    tracked.write_text("polluted\n")
    tracked.chmod(0o644)
    (fixtures / "generated.txt").write_text("pollution\n")

    changed = reset_fixture_tree(fixtures)

    assert changed == ["generated.txt", "task.py"]
    assert tracked.read_text() == "original\n"
    assert tracked.stat().st_mode & stat.S_IXUSR
    assert not (fixtures / "generated.txt").exists()


def test_task_filter_uses_stable_prefixes():
    tasks = select_tasks(DEFAULT_TIERS, "C2,C3,L1,X1")
    assert [task["id"].split("-", 1)[0] for task in tasks] == ["C2", "C3", "L1", "X1"]


@pytest.mark.parametrize(
    ("harness", "expected"),
    [
        ("opencode", "--dir"),
        ("copilot", "-C"),
        ("codex", "-C"),
        ("pi", "--no-session"),
    ],
)
def test_harness_command_pins_isolated_workdir(harness, expected, tmp_path):
    command, _ = HARNESSES[harness]["build"]("model", "ollama", None, "prompt", tmp_path)
    assert expected in command
    if harness != "pi":
        assert str(tmp_path) in command
