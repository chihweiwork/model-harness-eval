"""Generate the full-matrix analysis for results/new-run Markdown reports."""

from __future__ import annotations

import argparse
import html
from collections import Counter
from pathlib import Path

from bench.report import _average, _score, _status_counts, parse_report, short_model


TASK_IDS = ["T1", "T2", "T3", "T4", "C1", "C2", "C3", "L1", "X1", "X2", "R1"]
COMMON_MODELS = {
    "devstral-2-123b",
    "gemma4:31b",
    "laguna-xs-2.1",
    "ornith:35b",
    "nemotron-120b",
}
INCOMPATIBLE_MODELS = {"gemma-3-27b", "llama4-maverick"}
HARNESS_COLORS = {
    "pi": "#3f6db5",
    "codex": "#32734a",
    "copilot": "#7053b6",
    "opencode": "#c84f49",
}
MODEL_SIZE_INFO = {
    "devstral-2-123b": (123, None, "模型 ID"),
    "gemma4:31b": (31, None, "模型 ID"),
    "laguna-xs-2.1": (33, 3, "使用者補充：MoE"),
    "ornith:35b": (35, None, "模型 ID"),
    "nemotron-120b": (120, None, "模型 ID"),
}


def esc(value) -> str:
    return html.escape(str(value))


def logical_model(report) -> str:
    name = short_model(report.model)
    if name in {"mistral.devstral-2-123", "devstral-2-123b"}:
        return "devstral-2-123b"
    return name


def has_wrong_devstral_id(report) -> bool:
    return report.model.endswith("mistral.devstral-2-123")


def model_name(report) -> str:
    return logical_model(report)


def task_by_id(report, task_id):
    return next(task for key, task in report.tasks.items() if key.startswith(f"{task_id}-"))


def combination(report) -> str:
    return f"{report.harness} × {model_name(report)}"


def select_reports(paths):
    """Select the newest run for each logical model/harness/provider cell."""
    grouped = {}
    for path in paths:
        report = parse_report(path)
        key = logical_model(report), report.harness, report.provider
        grouped.setdefault(key, []).append(report)
    selected = []
    superseded = []
    for candidates in grouped.values():
        winner = max(
            candidates,
            key=lambda report: (
                report.date,
                report.model.endswith("mistral.devstral-2-123b"),
            ),
        )
        selected.append(winner)
        superseded.extend(report for report in candidates if report is not winner)
    return selected, superseded


def status_counts(reports):
    return sum((_status_counts(report.tasks) for report in reports), Counter())


def ranked_reports(reports):
    return sorted(reports, key=lambda report: (-_score(report.tasks), _average(report.tasks)))


def capability_reports(reports):
    """Reports eligible for model, harness, task, and speed comparisons."""
    return [
        report for report in reports
        if logical_model(report) in COMMON_MODELS and not has_wrong_devstral_id(report)
    ]


def incompatible_reports(reports):
    return [report for report in reports if logical_model(report) in INCOMPATIBLE_MODELS]


def harness_comparison_models(reports):
    """Models with one valid report for every harness."""
    operational = capability_reports(reports)
    harnesses = set(HARNESS_COLORS)
    return {
        model for model in COMMON_MODELS
        if {report.harness for report in operational if logical_model(report) == model} == harnesses
    }


def scatter_svg(reports) -> str:
    plotted = capability_reports(reports)
    width, height = 920, 420
    left, right, top, bottom = 64, 24, 32, 54
    max_seconds = max(_average(report.tasks) for report in plotted) * 1.08

    def x(seconds):
        return left + seconds / max_seconds * (width - left - right)

    def y(score):
        return top + (55 - score) / 15 * (height - top - bottom)

    grid = []
    for score in (40, 45, 50, 55):
        yy = y(score)
        grid.append(
            f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" class="grid"/>'
            f'<text x="{left-10}" y="{yy+4:.1f}" text-anchor="end">{score}</text>'
        )
    for seconds in range(0, 181, 30):
        if seconds > max_seconds:
            break
        xx = x(seconds)
        grid.append(
            f'<line x1="{xx:.1f}" y1="{top}" x2="{xx:.1f}" y2="{height-bottom}" class="grid"/>'
            f'<text x="{xx:.1f}" y="{height-bottom+24}" text-anchor="middle">{seconds}s</text>'
        )
    dots = []
    for report in plotted:
        score = _score(report.tasks)
        title = f"{combination(report)}: {score}/55, {_average(report.tasks):.1f}s"
        dots.append(
            f'<circle cx="{x(_average(report.tasks)):.1f}" cy="{y(score):.1f}" '
            f'r="{7 + max(score - 45, 0) * .45:.1f}" fill="{HARNESS_COLORS[report.harness]}" '
            f'fill-opacity=".72" stroke="{HARNESS_COLORS[report.harness]}" stroke-width="1.5">'
            f'<title>{esc(title)}</title></circle>'
        )
    legend = "".join(
        f'<g transform="translate({left + index * 118},12)"><circle r="6" fill="{color}"/>'
        f'<text x="10" y="4">{esc(harness)}</text></g>'
        for index, (harness, color) in enumerate(HARNESS_COLORS.items())
    )
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="速度與品質散佈圖">'
        f'<style>.grid{{stroke:#ddd8cf;stroke-width:1}}text{{font:12px system-ui;fill:#57534e}}</style>'
        f'<rect x="{left}" y="{top}" width="{x(60)-left:.1f}" height="{y(50)-top:.1f}" fill="#e9f2ea"/>'
        f'<text x="{left+8}" y="{top+16}" fill="#32734a">理想區</text>{legend}{"".join(grid)}'
        f'{"".join(dots)}<text x="{width/2}" y="{height-8}" text-anchor="middle">每任務平均耗時（秒）</text>'
        f'<text transform="translate(16 {height/2}) rotate(-90)" text-anchor="middle">得分 /55</text></svg>'
    )


def grouped_speed_svg(reports, group_by, label_by, group_order) -> str:
    """Render average speed as labeled points grouped by model or harness."""
    grouped = {group: [] for group in group_order}
    for report in capability_reports(reports):
        grouped[group_by(report)].append(report)
    grouped = {group: items for group, items in grouped.items() if items}
    width, left, right, top, bottom = 920, 170, 46, 42, 42
    row_height = 28
    group_gap = 20
    height = top + bottom + sum(len(items) * row_height + group_gap for items in grouped.values())
    max_seconds = max(_average(report.tasks) for items in grouped.values() for report in items) * 1.08

    def x(seconds):
        return left + seconds / max_seconds * (width - left - right)

    grid = []
    step = 30
    for seconds in range(0, int(max_seconds) + step, step):
        if seconds > max_seconds:
            break
        xx = x(seconds)
        grid.append(
            f'<line x1="{xx:.1f}" y1="{top-12}" x2="{xx:.1f}" y2="{height-bottom}" class="grid"/>'
            f'<text x="{xx:.1f}" y="{height-12}" text-anchor="middle">{seconds}s</text>'
        )
    marks = []
    cursor = top
    for group, items in grouped.items():
        items = sorted(items, key=lambda report: _average(report.tasks))
        middle = cursor + (len(items) - 1) * row_height / 2
        marks.append(f'<text x="{left-14}" y="{middle+4:.1f}" text-anchor="end" class="group">{esc(group)}</text>')
        for report in items:
            seconds = _average(report.tasks)
            xx = x(seconds)
            color = HARNESS_COLORS[report.harness]
            label = f"{label_by(report)}  {seconds:.1f}s"
            marks.append(
                f'<line x1="{left}" y1="{cursor}" x2="{xx:.1f}" y2="{cursor}" class="stem"/>'
                f'<circle cx="{xx:.1f}" cy="{cursor}" r="6" fill="{color}"/>'
                f'<text x="{xx+10:.1f}" y="{cursor+4}">{esc(label)}</text>'
            )
            cursor += row_height
        cursor += group_gap
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="分組速度比較">'
        '<style>.grid{stroke:#e4e0d9;stroke-width:1}.stem{stroke:#bbb4aa;stroke-width:1}'
        'text{font:12px system-ui;fill:#57534e}.group{font-weight:700;fill:#1c1917}</style>'
        f'{"".join(grid)}{"".join(marks)}</svg>'
    )
def bar_rows(items, value, maximum, suffix="") -> str:
    rows = []
    for label, item in items:
        number = value(item)
        rows.append(
            f'<div class="bar-row"><span>{esc(label)}</span><div class="bar-track">'
            f'<div class="bar-fill" style="width:{number / maximum * 100:.1f}%"></div></div>'
            f'<strong>{number:.1f}{suffix}</strong></div>'
        )
    return "".join(rows)


TASK_EVIDENCE = {
    "T1": ("讀檔與程式理解", "stdout 同時含 take、restock", "弱", "只驗關鍵字，未核對解釋是否正確"),
    "T2": ("定位並修正單檔 bug", "執行 calc.py 印出 all tests passed", "中", "驗證實際程式行為，但題目只有單一明顯 bug"),
    "T3": ("建立可執行檔案", "fizzbuzz.py 存在；第 3/15 行正確", "中", "未逐行驗證完整 1–15 輸出"),
    "T4": ("用 shell 查資料", "stdout 出現數字 42", "弱", "未證明真的讀取 data.csv 或使用 bash"),
    "C1": ("跨檔追根因與邊界條件", "受保護 pytest：剛好庫存、超賣、混合訂單", "強", "能區分修根因與繞過測試"),
    "C2": ("保綠重構與抽共用邏輯", "pytest 通過；utils.py 存在且 a/b 引用 utils", "中", "有結構檢查，但字串引用仍可能被表面滿足"),
    "C3": ("抵抗誤導堆疊並修根因", "main.py 受保護；banner 正確且 config port 為 int", "強", "明確拒絕只在 server.py 治標"),
    "L1": ("依規格完成持久化 CLI", "受保護的 9 個端到端 pytest 全通過", "強", "涵蓋格式、持久化、冪等、錯誤碼與 ID"),
    "X1": ("探索陌生 Office CLI", "產生任一 .txt；stdout 回答 45", "中偏弱", "未核對 txt 內容，也未證明使用 officecli"),
    "X2": ("探索陌生瀏覽 CLI", "stdout 出現 149.50", "弱", "未驗 session、導覽路徑或 opencli 使用紀錄"),
    "R1": ("操作真實 agent-browser", "stdout 出現 Example Domain", "弱", "未證明工具真的啟動；已知答案可能被直接輸出"),
}

TASK_FIXTURES = {
    "T1": "單檔 inventory.py；只需解釋 take/restock",
    "T2": "calc.py 的 add 誤用減法；需修檔並執行驗證",
    "T3": "空目錄建立 fizzbuzz.py；檢查第 3、15 行",
    "T4": "42 筆 CSV；回答需含 42",
    "C1": "store.py 的 > 邊界錯誤；受保護測試涵蓋剛好售完、超賣、混合訂單",
    "C2": "a.py/b.py 重複 normalize；必須建立 utils.py 且兩檔引用",
    "C3": "settings.json 的 port 是字串；須在 config 邊界轉成 int，main.py 受保護",
    "L1": "依 SPEC 實作持久化 todo CLI；9 個端到端測試",
    "X1": "用陌生 officecli 轉換自訂 OFFX 容器；建立 txt 並回答 45 字",
    "X2": "用具 session 狀態的 opencli 導覽本地站；回答 Aurora Lamp 149.50",
    "R1": "呼叫真實 agent-browser 開啟 example.com；回答頁面標題",
}


def task_evidence_rows(reports) -> str:
    operational = capability_reports(reports)
    rows = []
    for task_id in TASK_IDS:
        capability, verifier, strength, boundary = TASK_EVIDENCE[task_id]
        passed = sum(task_by_id(report, task_id).passed for report in operational)
        maximum = len(operational) * 5
        rows.append(
            f"<tr><td><strong>{task_id}</strong></td><td>{esc(capability)}</td>"
            f"<td>{esc(verifier)}</td><td>{esc(strength)}</td>"
            f"<td>{passed}/{maximum}</td><td>{esc(boundary)}</td></tr>"
        )
    return "".join(rows)


def harness_task_scores(reports, harness, denominator=True):
    cells = [report for report in capability_reports(reports) if report.harness == harness]
    maximum = len(cells) * 5
    values = [sum(task_by_id(report, task_id).passed for report in cells) for task_id in TASK_IDS]
    if denominator:
        return [f"{value}/{maximum}" for value in values]
    return values


def build_markdown(reports, superseded=()) -> str:
    operational = capability_reports(reports)
    incompatible = incompatible_reports(reports)
    fair_models = harness_comparison_models(reports)
    ranked = ranked_reports(operational)
    counts = status_counts(operational)
    total_score = sum(_score(report.tasks) for report in operational)
    total_maximum = len(operational) * 55
    rows = []
    for index, report in enumerate(ranked, 1):
        rows.append(
            f"| {index} | {combination(report)} | {report.provider} | "
            f"{_score(report.tasks)}/55 | {_average(report.tasks):.1f}s |"
        )
    evidence_rows = []
    for task_id in TASK_IDS:
        capability, verifier, strength, boundary = TASK_EVIDENCE[task_id]
        passed = sum(task_by_id(report, task_id).passed for report in operational)
        evidence_rows.append(
            f"| {task_id} | {capability} | {verifier} | {strength} | "
            f"{passed}/{len(operational) * 5} | {boundary} |"
        )
    harness_rows = []
    for harness in ("pi", "copilot", "codex", "opencode"):
        cells = [
            report for report in operational
            if report.harness == harness and logical_model(report) in fair_models
        ]
        score = sum(_score(report.tasks) for report in cells)
        speed = sum(_average(report.tasks) for report in cells) / len(cells)
        harness_rows.append(f"| {harness} | {score}/{len(cells) * 55} | {score / (len(cells) * 55):.1%} | {speed:.1f}s |")
    harness_task_rows = []
    for harness in ("pi", "copilot", "codex", "opencode"):
        values = harness_task_scores(operational, harness)
        harness_task_rows.append(f"| {harness} | {' | '.join(values)} |")
    model_speed_rows = []
    for model in sorted(COMMON_MODELS):
        cells = {report.harness: report for report in operational if logical_model(report) == model}
        speeds = [_average(report.tasks) for report in cells.values()]
        values = [f"{_average(cells[harness].tasks):.1f}s" if harness in cells else "排除" for harness in ("pi", "copilot", "codex", "opencode")]
        model_speed_rows.append(
            f"| {model} | " + " | ".join(values) + f" | {sum(speeds) / len(speeds):.1f}s |"
        )
    harness_speed_rows = []
    for harness in ("pi", "copilot", "codex", "opencode"):
        cells = {logical_model(report): report for report in operational if report.harness == harness}
        speeds = [_average(report.tasks) for report in cells.values()]
        values = [f"{_average(cells[model].tasks):.1f}s" if model in cells else "排除" for model in sorted(COMMON_MODELS)]
        harness_speed_rows.append(
            f"| {harness} | " + " | ".join(values) + f" | {sum(speeds) / len(speeds):.1f}s |"
        )
    size_rows = []
    for model in sorted(COMMON_MODELS):
        total, active, source = MODEL_SIZE_INFO[model]
        cells = [report for report in operational if logical_model(report) == model]
        size_rows.append(
            f"| {model} | {total}B | {f'{active}B' if active else '未提供'} | {source} | "
            f"{sum(_score(report.tasks) for report in cells)}/{len(cells) * 55} | "
            f"{sum(_average(report.tasks) for report in cells) / len(cells):.1f}s |"
        )
    return f"""# Coding Agent Harness 新跑評測分析

分析範圍：{len(operational)} 個模型 × Harness 組合，11 任務 × 5 輪，共 {total_maximum:,} 個 run。

## 結論與建議

1. `pi × laguna` 是本輪速度與品質雙冠；`codex × laguna` 的 0.1 秒差距小於實務上可判定的效應大小，兩者可視為同一領先級。
2. 若重視跨 harness 可移植性，`gemma4:31b` 是最穩選擇，但平均耗時從 Pi 的 62.1 秒到 Copilot 的 155.7 秒，harness 成本差達 2.5 倍。
3. 五模型公平比較為：Pi 266/275、Copilot 266/275、Codex 263/275、OpenCode 252/275。Pi 與 Copilot 同分，但 Pi 的端到端均速較快。
4. Devstral 在 Pi 為 48/55，其餘三個 harness 各 52/55；共同弱點是 R1 與 C3。
5. 在 {len(operational)} 個有效組合中，R1、C2 與 X1 是主要失分區，但 verifier 強度不同，不能把每一分當成等距能力量尺。
6. `gemma4:31b` 在 11 題 × 4 harness 全部 20/20；Laguna 除 R1 17/20 外其餘全滿。

| 使用情境 | 推薦組合 | 理由 |
|---|---|---|
| 最佳整體 | pi × laguna-xs-2.1 | 55/55、17.3s，且唯一支援 per-run 工具限制 |
| 幾乎同級替代 | codex × laguna-xs-2.1 | 55/55、17.4s |
| 跨 harness 穩定 | gemma4:31b | 四個 harness 全部 55/55 |
| Bedrock 首選 | copilot × nemotron-120b | 54/55、23.3s |
| Bedrock 備選 | pi × nemotron-120b | 54/55、34.4s，支援工具限制 |

下一步應替 T4、X1、X2、R1 增加命令 trace，並讓 X1 verifier 核對輸出內容；Llama 4 則應改用受支援的 tool-use API 模式後再測。

## 執行摘要

- 冠軍：`pi × laguna-xs-2.1`，55/55，平均 17.3 秒；`codex × laguna-xs-2.1` 同為 55/55，平均 17.4 秒。
- 穩定性冠軍：`gemma4:31b` 在四個 harness 全部 55/55，是唯一跨 harness 全滿分模型。
- 共有 6 個滿分組合。能力矩陣合計 {total_score}/{total_maximum}（{total_score / total_maximum:.1%}）。
- 能力矩陣狀態：PASS {counts['PASS']}、FAIL {counts['FAIL']}、EMPTY {counts['EMPTY']}、TIMEOUT {counts['TIMEOUT']}。
- `opencode` 舊報告中的 CWD 系統性故障已不再出現；本輪 `gemma4:31b` 55/55、`laguna` 54/55。

## Harness 公平比較

| Harness | 五模型得分 | 通過率 | 組合均速 |
|---|---:|---:|---:|
{chr(10).join(harness_rows)}

Harness 公平比較使用五個 harness 皆有正確資料的 Devstral、Gemma4、Laguna、Ornith、Nemotron，共 275 分。Pi 與 Copilot 同為 266/275，Pi 的組合均速較快。這不是完全受控的純 Harness 實驗：只有 Pi 真正套用每題 `tools` 限制，另外三個 harness 忽略該欄位，因此分數差不能全部歸因於 Harness 本身。

| Harness | T1 | T2 | T3 | T4 | C1 | C2 | C3 | L1 | X1 | X2 | R1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(harness_task_rows)}

- Pi：C1、C2、L1、X2 都是 25/25；弱點集中在 T1 22/25 與 X1 23/25。
- Copilot：C1、T2–T4、X1/X2 全滿；C2/C3 各 23/25，R1 22/25。
- Codex：T1/T2/T4/X2 全滿；C1 22/25，顯示 Nemotron 的跨檔邊界修復與模型交互較弱。
- OpenCode：C2 20/25、X1 19/25、R1 20/25；主要損失在保綠重構與多步 CLI，而不是一般寫檔。

## 能力排名

列出能完成 agent loop 的 {len(operational)} 個正式組合。

| # | 組合 | Provider | 得分 | 均速 |
|---:|---|---|---:|---:|
{"".join(row + chr(10) for row in rows)}
## 測試設計與證據強度

| 題目 | 測試能力 | 實際通過條件 | 證據強度 | 可執行組合通過 | 解讀界線 |
|---|---|---|---|---:|---|
{"".join(row + chr(10) for row in evidence_rows)}

分數不是等距的能力量尺。C1、C3、L1 有受保護測試或根因型檢查，PASS 證據較強；T1、T4、X2、R1 主要靠 stdout 關鍵字，可能被猜中，較適合視為基本可用性訊號。C2 與 X1 同時檢查檔案副作用，但結構與內容驗證仍有限。

### Fixture 與失敗代表什麼

- C1 的唯一根因是 `reserve()` 使用 `>` 而非 `>=`。失敗通常代表沒有找出「庫存剛好等於需求」的邊界條件，而非一般語法能力不足。
- C2 要求在測試維持全綠時建立真正共用的 `utils.py`。實際失敗包含只建立檔案卻未讓 `a.py`/`b.py` 使用，以及測試通過但未完成重構，能測到「行為正確但結構不符」。
- C3 故意讓 traceback 落在 `server.py`，真正修正點是 `config.py` 的型別正規化。Devstral 多次只在下游把程式跑通，卻留下字串 port，因此被根因 verifier 正確拒絕。
- L1 是最完整的規格實作題，涵蓋跨程序持久化、輸出格式、idempotent done、錯誤碼與 ID 不重用；98/100 顯示可執行模型對清楚規格的實作普遍穩定。
- X1/X2 測陌生 CLI 探索。X1 的常見失敗是已產生 `report.txt`，卻沒有回答正確的 45；X2 的失敗則是沒有完成 stateful 導覽或沒有輸出 149.50。
- R1 雖然通過率最低，但 verifier 只找 `Example Domain`，所以 FAIL 可指出流程沒有交付答案，PASS 卻不能證明真的使用 agent-browser。

## 相容性診斷（不計能力分數）

- Gemma 3 27B：四個 harness 都無法形成可執行 agent loop，常輸出原始 `tool_code` 或虛構檔案內容。這反映工具協議不相容，不足以判定 coding 能力。
- Llama 4 Maverick：四個 harness 都被 Bedrock streaming tool-use 拒絕。應先改成受支援的 API 模式再重跑，現有 0/55 不列模型能力。

## 速度與模型大小

### 依模型看速度（Harness 為欄位）

| 模型 | Pi | Copilot | Codex | OpenCode | 有效 Harness 均速 |
|---|---:|---:|---:|---:|---:|
{chr(10).join(model_speed_rows)}

### 依 Harness 看速度（模型為欄位）

| Harness | Devstral 123B | Gemma4 31B | Laguna XS 2.1 | Nemotron 120B | Ornith 35B | 五模型均速 |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(harness_speed_rows)}

### 模型大小比較

| 模型 | 總參數 | 每 token 啟用 | 規格來源 | 有效 Harness 得分 | 有效 Harness 均速 |
|---|---:|---:|---|---:|---:|
{chr(10).join(size_rows)}

Laguna XS 2.1 是 33B total parameter、每 token 啟用 3B 的 MoE；這是它能在本地機器保持低延遲的重要架構背景，但本次資料不能把速度差單獨歸因於 active parameters。其他模型目前只採模型 ID 中可見的總參數，不推測每 token 啟用量。Bedrock 與 Ollama 的硬體、網路及 provider 路徑不同，因此表中是端到端速度，不是純模型吞吐。

## 統計與設計限制

- 每格只有 5 次，1 次成敗就是 20 個百分點；目前沒有信賴區間、p95、token 或成本資料。
- Ollama 與 Bedrock 的硬體、網路和 provider 路徑不同，跨 provider 的秒數只能看端到端體感，不能直接解讀為模型純推理速度。
- 題目分數皆為 1 run 1 分，但 verifier 強度不同；55/55 不是標準化能力量尺。
- 只有 Pi 落實 per-run 工具限制，Harness 比較同時包含工具政策差異。
- 報告能說明這批固定 prompt、版本與環境的結果，不能外推到所有 coding 任務。

## 附錄：資料口徑

| 資料 | 檔數 | 原因 | 處理方式 |
|---|---:|---|---|
| 正確模型 ID 且可完成 agent loop | {len(operational)} | 可作能力分析 | 納入能力、任務與速度分析 |
| Devstral `123` × Pi/Copilot/OpenCode | {len(superseded)} | 模型 ID 錯誤，三者均已有 `123b` 結果 | 完全排除，由正確 ID 跑次取代 |
| Gemma 3 27B × 四 harness | 4 | 未形成可執行工具呼叫 | 僅列相容性診斷，不列能力排名 |
| Llama 4 Maverick × 四 harness | 4 | Bedrock streaming tool-use API 拒絕 | 僅列相容性診斷，不列能力排名 |

原始資料共 {len(reports) + len(superseded)} 份。報告按邏輯模型 × harness × provider 選最新跑次。Pi 的舊 Devstral 49/55 使用 `mistral.devstral-2-123`，由 `123b` 的 48/55 取代；Copilot 與 OpenCode 的舊 0/55 亦不納入能力分數。

報告結論僅適用於此次 runner、prompt、模型版本與 provider 組合。
"""


def build_html(reports, superseded=()) -> str:
    operational = capability_reports(reports)
    incompatible = incompatible_reports(reports)
    fair_models = harness_comparison_models(reports)
    ranked = ranked_reports(operational)
    counts = status_counts(operational)
    perfect = [report for report in ranked if _score(report.tasks) == 55]
    fastest = perfect[0]
    slowest = max(perfect, key=lambda report: _average(report.tasks))

    ranking_rows = []
    for index, report in enumerate(ranked, 1):
        score = _score(report.tasks)
        ranking_rows.append(
            f"<tr><td>{index}</td><td><strong>{esc(combination(report))}</strong></td>"
            f"<td><span class='provider'>{esc(report.provider)}</span></td>"
            f"<td class='score'>{score}/55</td><td>{score / 55:.0%}</td><td>{_average(report.tasks):.1f}s</td></tr>"
        )

    heat_rows = []
    for report in ranked:
        cells = "".join(
            f"<td class='heat h{task_by_id(report, task_id).passed}'>{task_by_id(report, task_id).passed}</td>"
            for task_id in TASK_IDS
        )
        heat_rows.append(
            f"<tr><td>{esc(combination(report))}</td><td><span class='provider'>{esc(report.provider)}</span></td>"
            f"{cells}<td class='score'>{_score(report.tasks)}</td></tr>"
        )

    common_rows = []
    common_stats = []
    for harness in ("pi", "copilot", "codex", "opencode"):
        cells = [
            report for report in operational
            if report.harness == harness and logical_model(report) in fair_models
        ]
        score = sum(_score(report.tasks) for report in cells)
        speed = sum(_average(report.tasks) for report in cells) / len(cells)
        maximum = len(cells) * 55
        common_stats.append((harness, score, speed))
        common_rows.append(
            f"<tr><td><strong>{harness}</strong></td><td>{score}/{maximum}</td>"
            f"<td>{score/maximum:.1%}</td><td>{speed:.1f}s</td></tr>"
        )

    model_notes = {
        "laguna-xs-2.1": "速度與品質雙冠",
        "gemma4:31b": "四個 harness 全部滿分",
        "ornith:35b": "快速，但 harness 差異較大",
        "nemotron-120b": "Bedrock 最高分選項",
        "devstral-2-123b": "48–52 分；R1、C3 較弱",
    }
    model_rows = []
    size_rows = []
    for model in sorted(COMMON_MODELS):
        cells = [report for report in operational if logical_model(report) == model]
        best = ranked_reports(cells)[0]
        average_speed = sum(_average(report.tasks) for report in cells) / len(cells)
        total_score = sum(_score(report.tasks) for report in cells)
        total_parameters, active_parameters, size_source = MODEL_SIZE_INFO[model]
        provider = "Ollama" if all(report.provider == "ollama" for report in cells) else "Bedrock"
        model_rows.append((model, provider, best.harness, f"{_score(best.tasks)}/55", f"{_average(best.tasks):.1f}s", model_notes[model]))
        size_rows.append((
            model,
            f"{total_parameters}B",
            f"{active_parameters}B" if active_parameters else "未提供",
            size_source,
            f"{total_score}/{len(cells) * 55}",
            f"{average_speed:.1f}s",
        ))
    model_table = "".join(
        "<tr>" + "".join(f"<td>{esc(value)}</td>" for value in row) + "</tr>"
        for row in model_rows
    )
    size_table = "".join(
        "<tr>" + "".join(f"<td>{esc(value)}</td>" for value in row) + "</tr>"
        for row in size_rows
    )

    speed_items = sorted(
        ((combination(report), report) for report in ranked if _score(report.tasks) >= 49),
        key=lambda item: _average(item[1].tasks),
    )[:15]
    speed_bars = bar_rows(
        speed_items,
        lambda report: _average(report.tasks),
        max(_average(report.tasks) for _, report in speed_items),
        "s",
    )
    model_speed_chart = grouped_speed_svg(
        operational,
        group_by=logical_model,
        label_by=lambda report: report.harness,
        group_order=("devstral-2-123b", "gemma4:31b", "laguna-xs-2.1", "ornith:35b", "nemotron-120b"),
    )
    harness_speed_chart = grouped_speed_svg(
        operational,
        group_by=lambda report: report.harness,
        label_by=logical_model,
        group_order=("pi", "copilot", "codex", "opencode"),
    )
    parameter_items = [(model, values[0]) for model, values in MODEL_SIZE_INFO.items()]
    parameter_bars = bar_rows(parameter_items, lambda size: size, max(size for _, size in parameter_items), "B")

    task_rows = []
    for task_id in TASK_IDS:
        passed = sum(task_by_id(report, task_id).passed for report in operational)
        average = sum(task_by_id(report, task_id).average for report in operational) / len(operational)
        maximum = len(operational) * 5
        task_rows.append(f"<tr><td>{task_id}</td><td>{passed}/{maximum}</td><td>{passed/maximum:.1%}</td><td>{average:.1f}s</td></tr>")

    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Coding Agent Harness 新跑評測報告</title>
<style>
:root{{--paper:#fff;--ink:#1c1917;--muted:#68625a;--line:#d8d2c8;--green:#32734a;--blue:#3f6db5;--amber:#a85b00;--red:#b52f2f;--wash:#f7f6f2}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;overflow-x:hidden;background:var(--paper);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Noto Sans TC",sans-serif;letter-spacing:0}}
main{{max-width:1120px;min-width:0;margin:auto;padding:64px 30px 90px}}main>*{{min-width:0}}h1,h2,h3{{font-family:Georgia,"Noto Serif TC",serif;letter-spacing:0;overflow-wrap:anywhere}}h1{{font-size:42px;line-height:1.15;margin:0 0 10px}}h2{{font-size:29px;margin:64px 0 22px;padding-bottom:10px;border-bottom:1px solid var(--line)}}h3{{font-size:21px;margin:28px 0 8px}}p{{max-width:900px;overflow-wrap:anywhere}}.lead{{font-size:18px;color:#37332f;margin:0 0 30px}}.muted{{color:var(--muted)}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin:28px 0 52px}}nav a{{border:1px solid var(--line);border-radius:5px;padding:8px 13px;color:var(--ink);text-decoration:none;background:#fff}}nav a:hover{{border-color:#8f877d;background:var(--wash)}}
.cards{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}}.card{{border:1px solid var(--line);border-radius:6px;padding:18px 20px;min-height:126px}}.label{{font-size:14px;color:var(--muted)}}.value{{font:700 30px/1.25 Georgia,serif;margin:8px 0 4px}}.green{{color:var(--green)}}.blue{{color:var(--blue)}}.amber{{color:var(--amber)}}
.callout{{border-left:4px solid var(--amber);background:#fff9ec;padding:14px 18px;margin:22px 0}}.callout.danger{{border-color:var(--red);background:#fff4f2}}.callout.good{{border-color:var(--green);background:#f1f8f2}}
.table-wrap{{overflow:auto;border:1px solid var(--line);border-radius:6px}}table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}}th,td{{padding:10px 12px;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}}th{{font-size:14px;background:var(--wash)}}th:nth-child(2),td:nth-child(2){{text-align:left}}tr:last-child td{{border-bottom:0}}.score{{color:var(--green);font-weight:750}}.provider{{color:#55419a;font:600 13px ui-monospace,monospace}}.badge{{font-size:11px;border-radius:3px;padding:2px 5px;margin-left:4px}}.badge.bad{{color:#8e2020;background:#fbe0de}}tr.invalid{{background:#fff4f2}}
.heat{{font-weight:700}}.h5{{color:#286c3d}}.h4{{color:#517631}}.h3{{color:#a85b00}}.h2,.h1{{color:#b52f2f}}.h0{{color:#b52f2f;background:#fce4e1}}
.chart{{border:1px solid var(--line);border-radius:6px;padding:14px;background:#fff}}.chart svg{{display:block;width:100%;height:auto}}.split{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}.analysis{{padding:18px 0;border-bottom:1px solid var(--line)}}
.bar-row{{display:grid;grid-template-columns:minmax(190px,2fr) 4fr 58px;gap:12px;align-items:center;margin:9px 0;font-size:14px}}.bar-track{{height:12px;background:#eeeae3}}.bar-fill{{height:100%;background:var(--green)}}.bar-row strong{{text-align:right}}ul{{padding-left:21px}}footer{{margin-top:64px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}}
@media(max-width:760px){{html,body,main{{width:100%;max-width:100%}}main{{padding:36px 16px 60px}}h1{{font-size:32px;word-break:break-all}}.lead{{word-break:break-all}}nav{{max-width:100%;overflow:hidden}}.cards,.split{{grid-template-columns:1fr}}.bar-row{{grid-template-columns:1fr 2fr 52px}}}}
@media print{{nav{{display:none}}main{{max-width:none;padding:20px}}h2{{break-before:page}}#overview h2{{break-before:auto}}.cards,tr,.card,.callout{{break-inside:avoid}}}}
</style></head><body><main>
<header><h1>Coding Agent Harness 新跑評測報告</h1><p class="lead">{len(operational)} 個模型 × Harness 組合，11 任務 × 5 輪，共 {len(operational) * 55:,} runs。2026-07-15 / 16</p></header>
<nav><a href="#recommendations">結論與建議</a><a href="#overview">總覽</a><a href="#ranking">能力排名</a><a href="#matrix">評分矩陣</a><a href="#design">測試設計</a><a href="#scatter">速度 vs 品質</a><a href="#harness">Harness 分析</a><a href="#models">模型分析</a><a href="#errors">錯誤診斷</a><a href="#speed">速度可視化</a><a href="#scope">附錄：資料口徑</a></nav>

<section id="recommendations"><h2>結論與建議</h2><div class="table-wrap"><table><thead><tr><th>推薦</th><th>組合</th><th>Provider</th><th>得分</th><th>均速</th><th>適用場景</th></tr></thead><tbody>
<tr><td>最佳整體</td><td><strong>pi × laguna-xs-2.1</strong></td><td>Ollama</td><td class="score">55/55</td><td>17.3s</td><td>速度、品質與工具限制兼具</td></tr>
<tr><td>同級替代</td><td><strong>codex × laguna-xs-2.1</strong></td><td>Ollama</td><td class="score">55/55</td><td>17.4s</td><td>不需要 per-run 工具限制</td></tr>
<tr><td>跨 harness 最穩</td><td><strong>gemma4:31b</strong></td><td>Ollama</td><td class="score">全 harness 55/55</td><td>62–156s</td><td>優先準確與可移植性</td></tr>
<tr><td>Bedrock 首選</td><td><strong>copilot × nemotron-120b</strong></td><td>LiteLLM</td><td class="score">54/55</td><td>23.3s</td><td>無本地 GPU、需雲端模型</td></tr>
<tr><td>Bedrock 工具限制</td><td><strong>pi × nemotron-120b</strong></td><td>LiteLLM</td><td class="score">54/55</td><td>34.4s</td><td>需 per-run 工具限制</td></tr>
</tbody></table></div>
<ol><li>替 T4、X1、X2、R1 增加命令 trace 或產物內容驗證，才能把 PASS 解讀為工具遵循。</li><li>Llama 4 改用受支援的 tool-use API 模式後才值得重跑。</li><li>正式選型再加入 p95、token、成本與 timeout 重試成本。</li></ol></section>

<section id="overview"><h2>總覽</h2><div class="cards">
<div class="card"><div class="label">正式能力組合</div><div class="value">{len(operational)}</div><div>五個模型 × 四個 Harness</div></div>
<div class="card"><div class="label">能力分析 run</div><div class="value">{len(operational) * 55:,}</div><div>PASS {counts['PASS']} / FAIL {counts['FAIL']} / EMPTY {counts['EMPTY']} / TIMEOUT {counts['TIMEOUT']}</div></div>
<div class="card"><div class="label">冠軍組合</div><div class="value green">55/55</div><div>{esc(combination(fastest))}（{_average(fastest.tasks):.1f}s）</div></div>
<div class="card"><div class="label">滿分組合</div><div class="value">{len(perfect)}</div><div>Laguna 2 組、Gemma4 4 組</div></div>
<div class="card"><div class="label">最速滿分</div><div class="value blue">{_average(fastest.tasks):.1f}s</div><div>{esc(combination(fastest))}</div></div>
<div class="card"><div class="label">最慢滿分</div><div class="value amber">{_average(slowest.tasks):.1f}s</div><div>{esc(combination(slowest))}</div></div>
</div></section>

<section id="ranking"><h2>能力排名</h2><p class="muted">列出能完成 agent loop 的 {len(operational)} 個正式組合。依得分降序，同分依每任務平均耗時升序。</p>
<div class="table-wrap"><table><thead><tr><th>#</th><th>組合</th><th>Provider</th><th>得分</th><th>通過率</th><th>均速</th></tr></thead><tbody>{''.join(ranking_rows)}</tbody></table></div></section>

<section id="matrix"><h2>逐任務評分矩陣</h2><p class="muted">列出全部 {len(operational)} 個有效能力組合，每格為 pass/5。</p>
<div class="table-wrap"><table><thead><tr><th>組合</th><th>Provider</th>{''.join(f'<th>{task}</th>' for task in TASK_IDS)}<th>合計</th></tr></thead><tbody>{''.join(heat_rows)}</tbody></table></div></section>

<section id="design"><h2>測試設計與分數解讀</h2><p>每一分的證據強度不同。下表直接對照 <code>bench/tasks.py</code>、fixture 與雙向 verifier 測試；「強」代表有受保護測試或根因型檢查，「弱」通常只檢查 stdout 關鍵字。</p>
<div class="table-wrap"><table><thead><tr><th>題目</th><th>測試能力</th><th>實際通過條件</th><th>證據</th><th>可執行組合通過</th><th>解讀界線</th></tr></thead><tbody>{task_evidence_rows(reports)}</tbody></table></div>
<div class="callout"><strong>重要：</strong>C1、C3、L1 的 PASS 可較可靠地解讀為實作正確；T1、T4、X2、R1 的 PASS 只能證明答案含預期文字，不能充分證明模型真的讀檔、使用 bash/opencli/agent-browser。X1 雖要求產生 txt，但 verifier 未核對檔案內容。</div></section>

<section id="scatter"><h2>速度 vs 品質散佈圖</h2><p>左上方是理想區域：高分且快速。只畫出完成 agent loop 的 {len(operational)} 個正式組合，避免 API 失敗的亞秒結果污染速度比較。</p><div class="chart">{scatter_svg(reports)}</div></section>

<section id="harness"><h2>Harness 分析</h2>
<div class="callout good"><strong>公平比較口徑：</strong>比較 Devstral、Gemma4、Laguna、Ornith、Nemotron，共 275 分。</div>
<div class="table-wrap"><table><thead><tr><th>Harness</th><th>共同模型得分</th><th>通過率</th><th>組合均速</th></tr></thead><tbody>{''.join(common_rows)}</tbody></table></div>
<div class="split">
<div><div class="analysis"><h3>pi — 與 Copilot 同分、速度領先</h3><p>五模型矩陣 266/275；Laguna 55/55、17.3 秒拿下雙冠。Devstral 為 48/55，主要失分在 T1 與 R1。</p></div><div class="analysis"><h3>codex — 基礎題穩、模型交互明顯</h3><p>五模型矩陣 263/275；Laguna／Ornith 又快又準，主要損失集中在 Nemotron 的跨檔與重構題。</p></div></div>
<div><div class="analysis"><h3>copilot — 與 Pi 同分、速度較慢</h3><p>五模型矩陣 266/275；Nemotron 54/55、Devstral 52/55，但組合均速高於 Pi。</p></div><div class="analysis"><h3>opencode — 瓶頸在多步流程</h3><p>五模型矩陣 252/275；Gemma4 55/55、Laguna 54/55，但 C2、X1、R1 仍是主要失分區。</p></div></div>
</div></section>

<section id="models"><h2>模型分析</h2><div class="table-wrap"><table><thead><tr><th>模型</th><th>Provider</th><th>最佳 Harness</th><th>最佳分數</th><th>均速</th><th>判讀</th></tr></thead><tbody>{model_table}</tbody></table></div>
<h3>Tier 1 — 可正式採用</h3><p><strong>Laguna</strong> 最快，除 R1 外跨 harness 其餘十題全滿；<strong>Gemma4</strong> 是唯一 11 題 × 4 harness 全部 20/20 的模型；<strong>Nemotron</strong> 是最高分 Bedrock 選項。<strong>Devstral</strong> 四份正確 <code>123b</code> 為 Pi 48/55、其餘三者各 52/55；共同弱點集中在 R1 14/20 與 C3 16/20。</p>
<h3>Tier 2 — 協議不可用</h3><p>Gemma 3 會輸出原始 <code>tool_code</code> 文字而非工具呼叫；Llama 4 Maverick 被 Bedrock streaming tool-use 直接拒絕。這些 0 分屬 agent 介面可用性，不是同口徑的 coding 能力分數。</p></section>

<section id="errors"><h2>錯誤診斷</h2><div class="split">
<div class="card"><h3>Streaming tool-use 不相容</h3><p><strong>Llama 4 Maverick × 全 harness</strong></p><p>全部 0/55，核心錯誤為 <code>This model doesn't support tool use in streaming mode</code>。需改 API 模式或更換模型。</p></div>
<div class="card"><h3>工具協議不理解</h3><p><strong>Gemma 3 27B × 全 harness</strong></p><p>會模仿 <code>tool_code</code>、虛構檔案內容或只承諾執行，未真正完成 agent loop，因此 220 輪全失敗。</p></div>
<div class="card"><h3>一般推理與執行失敗</h3><p><strong>有效能力組合</strong></p><p>R1 為 89/100，C2 為 91/100，X1 為 92/100。常見問題為重構未真正共用 utils、CLI 有產物但答案值錯、真實瀏覽器未取到標題；但 stdout-only verifier 也限制了正向證據強度。</p></div>
</div>
<h3>可執行組合的逐題難度</h3><div class="table-wrap"><table><thead><tr><th>任務</th><th>通過</th><th>通過率</th><th>平均耗時</th></tr></thead><tbody>{''.join(task_rows)}</tbody></table></div></section>

<section id="speed"><h2>速度與模型大小</h2>
<h3>綜合組合比較</h3><p>保留原有比較：列出得分至少 49/55 的 {len(speed_items)} 個有效組合；橫條為每任務平均耗時。</p><div class="chart">{speed_bars}</div>
<h3>依模型看速度</h3><p>每列是一個 Harness 標籤，可直接看同一模型換 Harness 後的端到端速度差。</p><div class="chart">{model_speed_chart}</div>
<h3>依 Harness 看速度</h3><p>每列是一個模型標籤，可直接看同一 Harness 搭配不同模型的速度分布。</p><div class="chart">{harness_speed_chart}</div>
<h3>模型參數量比較</h3><div class="chart">{parameter_bars}</div>
<div class="table-wrap"><table><thead><tr><th>模型</th><th>總參數</th><th>每 token 啟用</th><th>規格來源</th><th>有效 Harness 得分</th><th>有效 Harness 均速</th></tr></thead><tbody>{size_table}</tbody></table></div>
<div class="callout"><strong>大小不能直接解釋本表速度：</strong>Laguna XS 2.1 是 33B total、每 token 啟用 3B 的 MoE，因此雖然總參數接近 Gemma4 31B／Ornith 35B，實際啟用量不同。Devstral、Nemotron、Gemma4、Ornith 目前只採模型 ID 顯示的總參數，不推測 active parameters。Bedrock 與 Ollama 又經過不同硬體、網路及 provider 路徑，所以這裡是端到端觀測，不是純模型吞吐 benchmark。</div>
<div class="callout"><strong>複雜度放大：</strong>Codex × Gemma4 的 C3 平均 281.5 秒，是 T4 的 14.9 倍；Pi × Laguna 的 C3 為 30.0 秒，是 T4 的 6.5 倍。Gemma4 雖跨 harness 全滿分，但端到端耗時明顯高於 Laguna。</div></section>

<section id="scope"><h2>附錄：資料口徑</h2><p class="muted">以下只用於交代資料選取與排除規則，不是能力結論。</p><div class="table-wrap"><table><thead><tr><th>資料</th><th>組數／檔數</th><th>原因</th><th>處理</th></tr></thead><tbody>
<tr><td>正確模型 ID 且能完成 agent loop</td><td>{len(operational)}</td><td>可作能力分析</td><td>納入能力、任務與速度分析</td></tr>
<tr><td>Devstral 123 × Pi/Copilot/OpenCode</td><td>{len(superseded)}</td><td>模型 ID 錯誤，三者均已有 123b 結果</td><td>完全排除，由正確 ID 跑次取代</td></tr>
<tr><td>Gemma 3 27B × 四 harness</td><td>4</td><td>未形成可執行工具呼叫</td><td>只列相容性診斷</td></tr>
<tr><td>Llama 4 Maverick × 四 harness</td><td>4</td><td>Bedrock streaming tool-use API 拒絕</td><td>只列相容性診斷</td></tr>
</tbody></table></div><div class="callout"><strong>Devstral ID 稽核：</strong>Pi 的舊 49/55 使用 <code>mistral.devstral-2-123</code>，由 <code>123b</code> 的 48/55 取代；Copilot 與 OpenCode 的舊 0/55 亦不納入能力分數。</div></section>

<footer>來源：results/new-run 內 {len(reports) + len(superseded)} 份 benchmark_schema=2、isolation=verified 原始 Markdown；正式矩陣按邏輯模型 × harness × provider 選最新跑次，共 {len(reports)} 組。報告由 <code>bench/new_run_report.py</code> 重算產生；結論僅適用於此次 runner、prompt、verifier、模型版本與 provider 組合。</footer>
</main></body></html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=Path("results/new-run"))
    parser.add_argument("--html", type=Path, default=None)
    parser.add_argument("--markdown", type=Path, default=None)
    args = parser.parse_args()

    paths = sorted(
        path for path in args.results.glob("*.md")
        if path.name != "analysis-report.md"
    )
    reports, superseded = select_reports(paths)
    if len(reports) != 28:
        raise ValueError(f"expected 28 selected matrix cells, found {len(reports)}")
    if any(len(report.tasks) != 11 for report in reports):
        raise ValueError("every report must contain all 11 tasks")
    if any(not report.isolated or report.schema < 2 for report in reports):
        raise ValueError("all reports must be schema 2 and isolation verified")

    html_path = args.html or args.results / "analysis-report.html"
    markdown_path = args.markdown or args.results / "analysis-report.md"
    html_path.write_text(build_html(reports, superseded))
    markdown_path.write_text(build_markdown(reports, superseded))
    print(
        f"wrote {html_path} and {markdown_path} from {len(reports)} selected reports "
        f"({len(superseded)} superseded)"
    )


if __name__ == "__main__":
    main()
