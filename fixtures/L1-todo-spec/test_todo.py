import subprocess
import sys
from pathlib import Path

TODO = Path(__file__).parent / "todo.py"


def run(tmp_path, *args):
    return subprocess.run(
        [sys.executable, str(TODO), *args],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_list_empty(tmp_path):
    r = run(tmp_path, "list")
    assert r.returncode == 0
    assert r.stdout.strip() == "no todos"


def test_add_prints_incrementing_ids(tmp_path):
    r1 = run(tmp_path, "add", "buy milk")
    r2 = run(tmp_path, "add", "walk dog")
    assert r1.stdout.strip() == "added 1"
    assert r2.stdout.strip() == "added 2"
    assert r1.returncode == 0 and r2.returncode == 0


def test_list_shows_items_in_order(tmp_path):
    run(tmp_path, "add", "buy milk")
    run(tmp_path, "add", "walk dog")
    r = run(tmp_path, "list")
    assert r.stdout.splitlines() == ["1 [ ] buy milk", "2 [ ] walk dog"]


def test_done_marks_item(tmp_path):
    run(tmp_path, "add", "buy milk")
    run(tmp_path, "add", "walk dog")
    r = run(tmp_path, "done", "1")
    assert r.returncode == 0
    assert r.stdout.strip() == "done 1"
    r = run(tmp_path, "list")
    assert r.stdout.splitlines() == ["1 [x] buy milk", "2 [ ] walk dog"]


def test_done_is_idempotent(tmp_path):
    run(tmp_path, "add", "buy milk")
    run(tmp_path, "done", "1")
    r = run(tmp_path, "done", "1")
    assert r.returncode == 0
    assert r.stdout.strip() == "done 1"


def test_done_unknown_id_fails(tmp_path):
    run(tmp_path, "add", "buy milk")
    r = run(tmp_path, "done", "99")
    assert r.returncode == 1
    assert r.stdout.strip() == "not found"


def test_persistence_across_invocations(tmp_path):
    run(tmp_path, "add", "first")
    run(tmp_path, "add", "second")
    run(tmp_path, "done", "2")
    r = run(tmp_path, "list")
    assert r.stdout.splitlines() == ["1 [ ] first", "2 [x] second"]
    assert (tmp_path / "todos.json").exists()


def test_ids_not_reused_after_more_adds(tmp_path):
    run(tmp_path, "add", "a")
    run(tmp_path, "add", "b")
    r3 = run(tmp_path, "add", "c")
    assert r3.stdout.strip() == "added 3"


def test_add_text_with_spaces(tmp_path):
    run(tmp_path, "add", "call mom at noon")
    r = run(tmp_path, "list")
    assert r.stdout.splitlines() == ["1 [ ] call mom at noon"]
