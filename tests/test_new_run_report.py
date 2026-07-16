from pathlib import Path

from bench.new_run_report import (
    _score,
    build_html,
    build_markdown,
    capability_reports,
    incompatible_reports,
    logical_model,
    select_reports,
)


ROOT = Path(__file__).resolve().parents[1]
NEW_RUN = ROOT / "results" / "new-run"


def reports():
    paths = [
        path for path in sorted(NEW_RUN.glob("*.md"))
        if path.name != "analysis-report.md"
    ]
    return select_reports(paths)


def test_new_run_matrix_is_complete_and_isolated():
    dataset, superseded = reports()
    assert len(dataset) == 28
    assert len(superseded) == 3
    assert all(report.schema == 2 and report.isolated for report in dataset)
    assert all(len(report.tasks) == 11 for report in dataset)
    assert sum(sum(task.runs for task in report.tasks.values()) for report in dataset) == 1540
    assert len(capability_reports(dataset)) == 20
    assert len(incompatible_reports(dataset)) == 8

    pi_devstral = next(
        report
        for report in capability_reports(dataset)
        if report.harness == "pi" and logical_model(report) == "devstral-2-123b"
    )
    assert pi_devstral.path.name == "pi_litellm_bedrock_mistral.devstral-2-123b_20260716-121646.md"
    assert _score(pi_devstral.tasks) == 48


def test_report_surfaces_data_quality_and_new_winner():
    dataset, superseded = reports()
    rendered = build_html(dataset, superseded)
    markdown = build_markdown(dataset, superseded)
    assert "pi × laguna-xs-2.1" in rendered
    assert "17.3s" in rendered
    assert "附錄：資料口徑" in rendered
    assert "測試設計與分數解讀" in rendered
    assert "Devstral 在 Pi 為 48/55，其餘三個 harness 各 52/55" in markdown
    assert "stdout 同時含 take、restock" in markdown
    assert "copilot × devstral-2-123b" in rendered
    assert "opencode × devstral-2-123b" in rendered
    assert "正式能力組合" in rendered
    assert '<div class="value">20</div>' in rendered
    assert "依模型看速度" in rendered
    assert "依 Harness 看速度" in rendered
    assert "33B" in rendered
    assert "3B" in rendered
    assert "只列相容性診斷" in rendered
    assert "以下只用於交代資料選取與排除規則" in rendered
    assert 'aria-label="速度與品質散佈圖"' in rendered
    assert '<div class="chart">None</div>' not in rendered


def test_harness_percentages_use_the_current_common_model_count():
    dataset, superseded = reports()
    rendered = build_html(dataset, superseded)

    for score, percentage in (
        (266, "96.7%"),
        (266, "96.7%"),
        (263, "95.6%"),
        (252, "91.6%"),
    ):
        assert f"{score}/275" in rendered
        assert percentage in rendered

    assert "121.4%" not in rendered


def test_conclusions_are_first_and_wrong_devstral_id_is_excluded():
    dataset, superseded = reports()
    rendered = build_html(dataset, superseded)
    markdown = build_markdown(dataset, superseded)

    assert rendered.index('<section id="recommendations">') < rendered.index('<section id="overview">')
    assert rendered.index('<section id="scope">') > rendered.index('<section id="speed">')
    assert markdown.index("## 結論與建議") < markdown.index("## 附錄：資料口徑")
    html_body, html_appendix = rendered.split('<section id="scope">', 1)
    markdown_body, markdown_appendix = markdown.split("## 附錄：資料口徑", 1)
    assert "舊 49/55" not in html_body
    assert "舊 49/55" not in markdown_body
    assert "舊 49/55" in html_appendix
    assert "舊 Devstral 49/55" in markdown_appendix
    assert "pi × devstral-2-123b" in rendered
    assert "48/55" in rendered
    assert "204/220" in rendered
