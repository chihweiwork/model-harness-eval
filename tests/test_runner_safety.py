import shutil

import pytest

from bench import FIXTURES
from bench.fixture_baseline import (
    FixtureBaselineError,
    SourceFixtureTampered,
    assert_fixture_tree_unchanged,
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
