import json
from pathlib import Path

from bench.report import build_html, load_dataset


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def test_selection_is_unique_complete_and_archived():
    manifest_path = RESULTS / "selection.json"
    manifest, dataset, task_order, coverage = load_dataset(RESULTS, manifest_path)
    assert len(manifest["selected_files"]) == 28
    assert len(dataset) == 28
    assert len(task_order) == 7
    assert set(coverage.values()) == {0}
    assert len({report.key for report, _ in dataset.values()}) == 28
    for filename in manifest["archived_files"]:
        assert not (RESULTS / filename).exists()
        assert (RESULTS / "archive" / filename).exists()


def test_report_is_reproducible_from_markdown_and_manifest():
    manifest, dataset, task_order, coverage = load_dataset(
        RESULTS, RESULTS / "selection.json"
    )
    rendered = build_html(manifest, dataset, task_order, coverage)
    assert "28 個唯一完整組合" in rendered
    assert "目前滿分</div><div class=\"value\">35" in rendered
    assert "gemma4:12b 只有一輪前導資料" in rendered
    assert "223</td><td>48" not in rendered


def test_manifest_pins_git_history_baseline():
    manifest = json.loads((RESULTS / "selection.json").read_text())
    assert manifest["fixture_baseline_commit"] == "5bf3e09"
