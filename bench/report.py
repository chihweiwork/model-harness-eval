"""Build the benchmark HTML report from selected Markdown result files."""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SUMMARY_RE = re.compile(
    r"^\| (?P<task>[^|]+) \| (?P<tier>[^|]+) \| "
    r"(?P<passed>\d+)/(?P<runs>\d+) \| (?P<silent>\d+) \| "
    r"(?P<empty>\d+) \| (?P<avg>[\d.]+) \|$"
)
RUN_RE = re.compile(r"^### run \d+ — (?P<status>[^\n(]+) \((?P<seconds>[\d.]+)s\)")
META_RE = re.compile(r"\b(?P<key>\w+)=(?P<value>\S+)")


@dataclass(frozen=True)
class TaskResult:
    task: str
    tier: str
    passed: int
    runs: int
    silent: int
    empty: int
    average: float
    statuses: Counter


@dataclass(frozen=True)
class BenchmarkReport:
    path: Path
    model: str
    harness: str
    provider: str
    date: datetime
    schema: int
    isolated: bool
    tasks: dict[str, TaskResult]

    @property
    def key(self):
        return self.model, self.harness, self.provider


def _metadata(line: str) -> dict[str, str]:
    return {match.group("key"): match.group("value") for match in META_RE.finditer(line)}


def parse_report(path: Path) -> BenchmarkReport:
    text = path.read_text()
    lines = text.splitlines()
    title = lines[0].removeprefix("# model-harness-eval: ")
    parts = [part.strip() for part in title.split("×")]
    model = parts[0]
    meta = _metadata(lines[1])
    harness = meta.get("harness", parts[1] if len(parts) > 1 else "unknown")
    provider = meta.get("provider", "litellm" if "× litellm" in title else "ollama")
    date_match = re.search(r"日期: (\d{4}-\d{2}-\d{2} \d{2}:\d{2})", lines[1])
    date = datetime.strptime(date_match.group(1), "%Y-%m-%d %H:%M")
    summaries = {}
    for line in lines:
        match = SUMMARY_RE.match(line)
        if not match:
            continue
        values = match.groupdict()
        task = values["task"].strip()
        summaries[task] = values
    run_statuses: dict[str, list[str]] = defaultdict(list)
    current_task = None
    for line in lines:
        if line.startswith("## ") and line[3:].strip() in summaries:
            current_task = line[3:].strip()
        elif current_task and (match := RUN_RE.match(line)):
            run_statuses[current_task].append(match.group("status").strip())
    tasks = {}
    for task, values in summaries.items():
        tasks[task] = TaskResult(
            task=task,
            tier=values["tier"].strip(),
            passed=int(values["passed"]),
            runs=int(values["runs"]),
            silent=int(values["silent"]),
            empty=int(values["empty"]),
            average=float(values["avg"]),
            statuses=Counter(run_statuses.get(task, [])),
        )
    run_meta = _metadata(lines[2]) if len(lines) > 2 and "benchmark_schema=" in lines[2] else {}
    return BenchmarkReport(
        path=path,
        model=model,
        harness=harness,
        provider=provider,
        date=date,
        schema=int(run_meta.get("benchmark_schema", 1)),
        isolated=run_meta.get("isolation") == "verified",
        tasks=tasks,
    )


def short_model(model: str) -> str:
    model = model.removeprefix("bedrock/").removesuffix(":latest")
    replacements = {
        "google.gemma-3-27b-it": "gemma-3-27b",
        "mistral.devstral-2-123b": "devstral-2-123b",
        "nvidia.nemotron-super-3-120b": "nemotron-120b",
        "us.meta.llama4-maverick-17b-instruct-v1:0": "llama4-maverick",
    }
    return replacements.get(model, model)


def status_group(status: str) -> str:
    if status in {"PASS", "SILENT-PASS"}:
        return "PASS"
    if status.startswith("EMPTY"):
        return "EMPTY"
    return status


def task_quality(task: TaskResult, report: BenchmarkReport):
    grouped = Counter()
    for status, count in task.statuses.items():
        grouped[status_group(status)] += count
    return (
        task.passed,
        -grouped["TIMEOUT"],
        -grouped["EMPTY"],
        -grouped["FAIL"],
        -task.average,
        report.date,
    )


def load_dataset(results: Path, manifest_path: Path):
    manifest = json.loads(manifest_path.read_text())
    base = [parse_report(results / name) for name in manifest["selected_files"]]
    keys = [report.key for report in base]
    if len(keys) != len(set(keys)):
        raise ValueError("selection manifest contains duplicate model/harness/provider combinations")
    excluded = manifest["excluded_tasks"]
    rerun_candidates = defaultdict(list)
    for path in results.glob("*.md"):
        if path.name in manifest["selected_files"]:
            continue
        report = parse_report(path)
        if report.schema < 2 or not report.isolated or report.key not in set(keys):
            continue
        for task_id, task in report.tasks.items():
            if task.runs == 5 and task_id in excluded:
                rerun_candidates[(report.key, task_id)].append((report, task))
    coverage = {
        task_id: sum(bool(rerun_candidates[(key, task_id)]) for key in keys)
        for task_id in excluded
    }
    eligible = {task_id for task_id, count in coverage.items() if count == len(keys)}
    task_order = [
        task_id for task_id in next(iter(base)).tasks
        if task_id not in excluded or task_id in eligible
    ]
    dataset = {}
    for report in base:
        chosen = {task_id: report.tasks[task_id] for task_id in task_order if task_id in report.tasks}
        for task_id in eligible:
            candidates = rerun_candidates[(report.key, task_id)]
            _, chosen[task_id] = max(candidates, key=lambda item: task_quality(item[1], item[0]))
        dataset[report.key] = (report, chosen)
    return manifest, dataset, task_order, coverage


def _status_counts(tasks: dict[str, TaskResult]) -> Counter:
    counts = Counter()
    for task in tasks.values():
        for status, count in task.statuses.items():
            counts[status_group(status)] += count
    return counts


def _score(tasks: dict[str, TaskResult]) -> int:
    return sum(task.passed for task in tasks.values())


def _average(tasks: dict[str, TaskResult]) -> float:
    total_runs = sum(task.runs for task in tasks.values())
    return sum(task.average * task.runs for task in tasks.values()) / total_runs


def _esc(value) -> str:
    return html.escape(str(value))


def build_html(manifest, dataset, task_order, coverage) -> str:
    maximum = len(task_order) * 5
    ranked = sorted(
        dataset.values(),
        key=lambda item: (-_score(item[1]), _average(item[1]), item[0].harness, item[0].model),
    )
    harness_counts = defaultdict(Counter)
    for report, tasks in dataset.values():
        harness_counts[report.harness].update(_status_counts(tasks))
    best_by_model = {}
    for report, tasks in ranked:
        best_by_model.setdefault(report.model, (report, tasks))
    perfect = [(report, tasks) for report, tasks in ranked if _score(tasks) == maximum]
    fastest_perfect = min(perfect, key=lambda item: _average(item[1])) if perfect else None

    ranking_rows = []
    for index, (report, tasks) in enumerate(ranked, 1):
        counts = _status_counts(tasks)
        score = _score(tasks)
        ranking_rows.append(
            f"<tr><td>{index}</td><td>{_esc(report.harness)} × {_esc(short_model(report.model))}</td>"
            f"<td><span class='provider {_esc(report.provider)}'>{_esc(report.provider)}</span></td>"
            f"<td><strong>{score}/{maximum}</strong></td><td>{100 * score / maximum:.0f}%</td>"
            f"<td>{_average(tasks):.1f}</td><td>{counts['FAIL']}</td>"
            f"<td>{counts['EMPTY']}</td><td>{counts['TIMEOUT']}</td></tr>"
        )

    heat_rows = []
    for report, tasks in ranked[:15]:
        cells = "".join(f"<td class='score s{tasks[task].passed}'>{tasks[task].passed}</td>" for task in task_order)
        heat_rows.append(
            f"<tr><td>{_esc(report.harness)} × {_esc(short_model(report.model))}</td>"
            f"{cells}<td><strong>{_score(tasks)}</strong></td></tr>"
        )

    harness_rows = []
    for harness in sorted(harness_counts):
        counts = harness_counts[harness]
        harness_rows.append(
            f"<tr><td>{_esc(harness)}</td><td>{counts['PASS']}</td><td>{counts['FAIL']}</td>"
            f"<td>{counts['EMPTY']}</td><td>{counts['TIMEOUT']}</td></tr>"
        )

    model_rows = []
    for model, (report, tasks) in sorted(
        best_by_model.items(), key=lambda item: (-_score(item[1][1]), _average(item[1][1]))
    ):
        model_rows.append(
            f"<tr><td>{_esc(short_model(model))}</td><td>{_esc(report.provider)}</td>"
            f"<td>{_esc(report.harness)}</td><td>{_score(tasks)}/{maximum}</td>"
            f"<td>{_average(tasks):.1f}s</td></tr>"
        )

    coverage_items = "".join(
        f"<li><code>{_esc(task)}</code>: {count}/{len(dataset)} 組已完成可信補跑</li>"
        for task, count in coverage.items()
    )
    excluded_labels = "、".join(f"<code>{_esc(task)}</code>" for task in manifest["excluded_tasks"])
    fastest_note = "尚無滿分組合"
    if fastest_perfect:
        report, tasks = fastest_perfect
        fastest_note = (
            f"{_esc(report.harness)} × {_esc(short_model(report.model))}，"
            f"{_score(tasks)}/{maximum}，每題平均 {_average(tasks):.1f}s"
        )

    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Coding Agent Harness 評測報告</title>
<style>
:root{{--bg:#f6f7fb;--surface:#fff;--text:#18212f;--muted:#657084;--line:#dfe3ea;--accent:#167c5a;--warn:#a66300;--bad:#b32929;--info:#2457b2}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.55 system-ui,sans-serif}}
.page{{max-width:1180px;margin:auto;padding:40px 24px 72px}} h1{{font-size:2rem;margin-bottom:4px}} h2{{margin-top:42px;border-bottom:1px solid var(--line);padding-bottom:8px}}
.lead,.muted{{color:var(--muted)}} .cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:24px 0}}
.card,.note{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px}} .value{{font-size:1.7rem;font-weight:750}}
.note.warn{{border-left:5px solid var(--warn)}} .note.info{{border-left:5px solid var(--info)}}
.table-wrap{{overflow:auto;background:var(--surface);border:1px solid var(--line);border-radius:10px}}
table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}} th,td{{padding:9px 11px;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}} th:first-child,td:nth-child(2){{text-align:left}} th{{background:#eef1f6}}
.provider{{padding:2px 7px;border-radius:999px;background:#e9edf3;font-size:.8rem}} .provider.ollama{{color:#734b00}} .provider.litellm{{color:#2457b2}}
.score{{font-weight:700}} .s5{{background:#dff4e8}} .s4{{background:#edf6df}} .s3{{background:#fff4cf}} .s2,.s1{{background:#fee7d7}} .s0{{background:#f8dada}}
code{{background:#eef1f6;padding:1px 5px;border-radius:4px}} footer{{margin-top:42px;color:var(--muted);font-size:.85rem}}
</style></head><body><main class="page">
<h1>Coding Agent Harness 評測報告</h1>
<p class="lead">依 28 個唯一完整組合重算；歷史污染題在可信補跑完成前不列入排名。</p>
<section class="cards">
<div class="card"><div class="muted">正式模型</div><div class="value">{len(best_by_model)}</div></div>
<div class="card"><div class="muted">Harness</div><div class="value">{len(harness_counts)}</div></div>
<div class="card"><div class="muted">完整組合</div><div class="value">{len(dataset)}</div></div>
<div class="card"><div class="muted">目前滿分</div><div class="value">{maximum}</div></div>
</section>
<div class="note warn"><strong>資料限制：</strong>歷史 fixture 曾遭 benchmark subprocess 修改。{excluded_labels} 暫時全面排除；目前只比較 {len(task_order)} 題 × 5 輪。gemma4:12b 只有一輪前導資料，也不進入正式排名。</div>

<h2>完整排名</h2><p class="muted">依通過數降序，同分依每題平均耗時升序。最快滿分：{fastest_note}。</p>
<div class="table-wrap"><table><thead><tr><th>#</th><th>組合</th><th>Provider</th><th>得分</th><th>通過率</th><th>均速(s)</th><th>FAIL</th><th>EMPTY</th><th>TIMEOUT</th></tr></thead><tbody>{''.join(ranking_rows)}</tbody></table></div>

<h2>前 15 名逐任務矩陣</h2>
<div class="table-wrap"><table><thead><tr><th>組合</th>{''.join(f'<th>{_esc(task.split("-",1)[0])}</th>' for task in task_order)}<th>合計</th></tr></thead><tbody>{''.join(heat_rows)}</tbody></table></div>

<h2>Harness 狀態統計</h2><p class="muted">PASS 包含 SILENT-PASS；所有數字只計入目前共同的 {len(task_order)} 題。</p>
<div class="table-wrap"><table><thead><tr><th>Harness</th><th>PASS</th><th>FAIL</th><th>EMPTY</th><th>TIMEOUT</th></tr></thead><tbody>{''.join(harness_rows)}</tbody></table></div>

<h2>各模型最佳組合</h2>
<div class="table-wrap"><table><thead><tr><th>模型</th><th>Provider</th><th>最佳 Harness</th><th>分數</th><th>均速</th></tr></thead><tbody>{''.join(model_rows)}</tbody></table></div>

<h2>污染題補跑覆蓋</h2><div class="note info"><ul>{coverage_items}</ul><p>某題必須達到 {len(dataset)}/{len(dataset)} 組 isolation-verified 五輪結果，才會重新加入共同排名。</p></div>

<h2>解讀界線</h2><ul>
<li>結果描述的是本次 runner、prompt、provider 與模型版本組合，不單獨證明 harness 或模型的普遍優劣。</li>
<li>opencode 歷史結果顯示明顯工作目錄異常；在修復後補跑前，不推估其可能提升幅度。</li>
<li>Bedrock 結果只證明受測組合的技術可行性；本評測沒有涵蓋成本、限流、長期可靠性或資料治理。</li>
</ul>
<footer>selection schema {_esc(manifest['schema_version'])}；fixture baseline commit {_esc(manifest['fixture_baseline_commit'])}；封存 {_esc(len(manifest['archived_files']))} 份前導或重複資料。</footer>
</main></body></html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=Path("results"))
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    manifest_path = args.manifest or args.results / "selection.json"
    output = args.output or args.results / "report_v2.html"
    manifest, dataset, task_order, coverage = load_dataset(args.results, manifest_path)
    output.write_text(build_html(manifest, dataset, task_order, coverage))
    print(f"wrote {output} ({len(dataset)} combinations, {len(task_order) * 5} points)")


if __name__ == "__main__":
    main()
