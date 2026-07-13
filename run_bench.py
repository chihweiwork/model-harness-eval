#!/usr/bin/env python3
"""harness × 地端模型評測 v3

用法:
    python3 run_bench.py gemma4:12b                          # 全部 tier, 每題 5 次, harness=pi
    python3 run_bench.py gemma4:12b qwen3.5:9b --runs 3
    python3 run_bench.py gemma4:12b --tier complex,cli --runs 1
    python3 run_bench.py gemma4:12b --harness opencode
    python3 run_bench.py gemma4:12b --harness pi,opencode,copilot   # harness × model 矩陣

Harness: pi(預設) / opencode / copilot — 三者都接 Ollama 地端模型。
Tier: smoke(簡單) / complex(多檔coding) / long(長程) / cli(陌生CLI) / real(真實工具, 需 --tier 指定)
每個任務在乾淨 tempdir 以 harness 非互動模式執行, 用程式驗證結果, 統計 pass@1 與空轉(EMPTY)率。
結果輸出到終端 + results/<harness>_<model>_<timestamp>.md
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path

BENCH_DIR = Path(__file__).parent
FIXTURES = BENCH_DIR / "fixtures"
RESULTS_DIR = BENCH_DIR / "results"

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

# ---------------------------------------------------------------- harness


def build_pi_cmd(model, tools, prompt):
    cmd = ["pi", "--provider", "ollama", "--model", model, "-p", prompt]
    if tools:
        cmd[1:1] = ["--tools", tools]
    return cmd, {"PI_OFFLINE": "1", "PI_SKIP_VERSION_CHECK": "1"}


def build_opencode_cmd(model, tools, prompt):
    # 無 per-run 工具限制旗標, tools 忽略(報告會註記)
    # 需要 ~/.config/opencode/opencode.jsonc 註冊 ollama provider(見 README)
    # 預設格式混雜橫幅/工具日誌/ANSI 色碼, 改用 JSON 事件流再抽 text 事件
    cmd = ["opencode", "run", "--model", f"ollama/{model}", "--auto",
           "--format", "json", prompt]
    return cmd, {}


def extract_opencode_text(stdout):
    """從 opencode 的 JSONL 事件流抽出模型給使用者的文字(type=text)。"""
    texts = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "text":
            texts.append(ev.get("part", {}).get("text", ""))
    return "\n".join(t for t in texts if t)


def build_copilot_cmd(model, tools, prompt):
    # BYOK 模式接本地 Ollama(copilot help providers)
    # 內建工具名稱未文件化, 無法精確對應 --available-tools, tools 忽略(報告會註記)
    cmd = ["copilot", "-p", prompt, "--allow-all-tools", "-s", "--no-color",
           "--no-custom-instructions", "--no-ask-user", "--no-auto-update"]
    return cmd, {"COPILOT_PROVIDER_BASE_URL": f"{OLLAMA_BASE_URL}/v1",
                 "COPILOT_MODEL": model}


HARNESSES = {
    "pi": dict(build=build_pi_cmd, tools_supported=True, extract=None),
    "opencode": dict(build=build_opencode_cmd, tools_supported=False,
                     extract=extract_opencode_text),
    "copilot": dict(build=build_copilot_cmd, tools_supported=False, extract=None),
}

# ---------------------------------------------------------------- smoke 素材

CALC_PY = '''\
def add(a, b):
    return a - b  # bug

def multiply(a, b):
    result = 0
    for _ in range(b):
        result += a
    return result

if __name__ == "__main__":
    assert add(2, 3) == 5, "add failed"
    assert multiply(3, 4) == 12, "multiply failed"
    print("all tests passed")
'''

DATA_CSV = "id,name,score\n" + "\n".join(f"{i},user{i},{i * 7 % 100}" for i in range(1, 43)) + "\n"

INVENTORY_PY = '''\
"""Simple inventory manager."""

STOCK = {"apple": 10, "banana": 5}

def take(item, n):
    if STOCK.get(item, 0) >= n:
        STOCK[item] -= n
        return True
    return False

def restock(item, n):
    STOCK[item] = STOCK.get(item, 0) + n
'''

# ---------------------------------------------------------------- 驗證函式


def _pytest(d: Path, *args):
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", *args],
        cwd=d, capture_output=True, text=True, timeout=120,
    )


def _tail(r):
    out = (r.stdout or "") + (r.stderr or "")
    return out.strip().splitlines()[-1] if out.strip() else "(無輸出)"


def verify_c1(d, stdout):
    r = _pytest(d)
    return r.returncode == 0, f"pytest → {_tail(r)}"


def verify_c2(d, stdout):
    r = _pytest(d)
    if r.returncode != 0:
        return False, f"pytest → {_tail(r)}"
    if not (d / "utils.py").exists():
        return False, "pytest 過了但沒有建立 utils.py"
    a, b = (d / "a.py").read_text(), (d / "b.py").read_text()
    if "utils" not in a or "utils" not in b:
        return False, "utils.py 存在但 a.py/b.py 沒有使用它"
    return True, "pytest 通過, 共用邏輯已抽到 utils.py"


def verify_c3(d, stdout):
    r = subprocess.run(
        [sys.executable, "main.py"], cwd=d,
        capture_output=True, text=True, timeout=60,
    )
    if r.returncode != 0 or "admin 8081" not in r.stdout:
        return False, f"main.py → {_tail(r)}"
    # 根因檢查: config 層必須回傳 int port(修 config.py 或 settings.json 皆可),
    # 只在 server.py 貼 int() 繃帶不算修根因
    r2 = subprocess.run(
        [sys.executable, "-c",
         "from config import load_config; import sys;"
         "sys.exit(0 if isinstance(load_config()['port'], int) else 1)"],
        cwd=d, capture_output=True, text=True, timeout=60,
    )
    if r2.returncode != 0:
        return False, "main.py 能跑但只治標(config port 仍是字串, 根因未修)"
    return True, f"main.py → {_tail(r)}, 根因已修"


def verify_l1(d, stdout):
    if not (d / "todo.py").exists():
        return False, "todo.py 沒有被建立"
    r = _pytest(d, "test_todo.py")
    return r.returncode == 0, f"pytest → {_tail(r)}"


def verify_x1(d, stdout):
    txts = list(d.glob("*.txt"))
    if not txts:
        return False, "沒有產生任何 .txt 輸出檔"
    s = stdout.lower()
    if not (re.search(r"\b45\b", s) or "forty-five" in s or "forty five" in s):
        return False, f"有輸出檔 {txts[0].name} 但回答中沒有正確字數 45"
    return True, f"產出 {txts[0].name} 且回答正確字數 45"


def verify_x2(d, stdout):
    ok = "149.50" in stdout
    return ok, "回答含正確價格 149.50" if ok else "回答中找不到 149.50"


def verify_r1(d, stdout):
    ok = "example domain" in stdout.lower()
    return ok, "回答含頁面標題 Example Domain" if ok else "回答中找不到 Example Domain"


# --- smoke ---

def setup_t1(d):
    (d / "inventory.py").write_text(INVENTORY_PY)


def verify_t1(d, stdout):
    s = stdout.lower()
    ok = "take" in s and "restock" in s
    return ok, "有提到 take 和 restock" if ok else "回答沒有涵蓋兩個函式"


def setup_t2(d):
    (d / "calc.py").write_text(CALC_PY)


def verify_t2(d, stdout):
    r = subprocess.run([sys.executable, "calc.py"], cwd=d,
                       capture_output=True, text=True, timeout=30)
    return "all tests passed" in r.stdout, f"calc.py → {_tail(r)}"


def verify_t3(d, stdout):
    f = d / "fizzbuzz.py"
    if not f.exists():
        return False, "fizzbuzz.py 沒有被建立"
    r = subprocess.run([sys.executable, "fizzbuzz.py"], cwd=d,
                       capture_output=True, text=True, timeout=30)
    lines = r.stdout.strip().splitlines()
    if len(lines) < 15:
        return False, f"輸出只有 {len(lines)} 行"
    ok = lines[2].strip().lower() == "fizz" and lines[14].strip().lower() == "fizzbuzz"
    return ok, f"第3行={lines[2]!r} 第15行={lines[14]!r}"


def setup_t4(d):
    (d / "data.csv").write_text(DATA_CSV)


def verify_t4(d, stdout):
    ok = bool(re.search(r"\b42\b", stdout))
    return ok, "回答含正確筆數 42" if ok else "回答中找不到 42"


# ---------------------------------------------------------------- 任務表

TASKS = [
    # smoke
    dict(id="T1-程式理解", tier="smoke", setup=setup_t1, verify=verify_t1, timeout=300,
         tools="read,grep,find,ls",
         prompt="Read inventory.py and explain what each function does, mentioning each function by name."),
    dict(id="T2-修bug", tier="smoke", setup=setup_t2, verify=verify_t2, timeout=300, tools=None,
         prompt="Read calc.py, find the bug, fix it, then run 'python3 calc.py' to verify the fix works."),
    dict(id="T3-寫檔案", tier="smoke", setup=None, verify=verify_t3, timeout=300, tools=None,
         prompt="Create fizzbuzz.py that prints FizzBuzz from 1 to 15 (one per line: Fizz for multiples of 3, Buzz for 5, FizzBuzz for both). Run it to verify."),
    dict(id="T4-bash查資料", tier="smoke", setup=setup_t4, verify=verify_t4, timeout=300,
         tools="read,bash",
         prompt="data.csv has a header row. Use bash to count how many data rows (excluding header) it has, and state the number clearly."),
    # complex
    dict(id="C1-跨檔bug", tier="complex", fixture="C1-crossfile-bug", verify=verify_c1,
         timeout=600, tools=None, protected=["test_report.py"],
         prompt="The tests in this project are failing. Run 'python3 -m pytest -q', track down the root cause, and fix it so all tests pass. Do not modify test_report.py."),
    dict(id="C2-重構保綠", tier="complex", fixture="C2-refactor-green", verify=verify_c2,
         timeout=600, tools=None, protected=["test_ab.py"],
         prompt="a.py and b.py contain duplicated name-normalization logic. Refactor: extract the shared logic into a new utils.py and make both a.py and b.py use it. All tests must still pass (run 'python3 -m pytest -q' to verify). Do not modify test_ab.py."),
    dict(id="C3-誤導除錯", tier="complex", fixture="C3-misleading-trace", verify=verify_c3,
         timeout=600, tools=None, protected=["main.py"],
         prompt="Running 'python3 main.py' crashes. Find the root cause, fix it, and verify that 'python3 main.py' prints the startup banner successfully. Do not modify main.py."),
    # long
    dict(id="L1-spec建專案", tier="long", fixture="L1-todo-spec", verify=verify_l1,
         timeout=900, tools=None, protected=["SPEC.md", "test_todo.py"],
         prompt="Read SPEC.md and implement todo.py exactly as specified. Verify by running 'python3 -m pytest test_todo.py -q' and iterate until all tests pass. Do not modify SPEC.md or test_todo.py."),
    # cli
    dict(id="X1-陌生officecli", tier="cli", fixture="X1-officecli", verify=verify_x1,
         timeout=600, tools="read,bash",
         prompt="This directory contains report.docx and a command-line tool at ./bin/officecli that you have never seen before. Use the tool to convert report.docx to plain text saved as report.txt, then state clearly how many words the document body contains."),
    dict(id="X2-陌生opencli", tier="cli", fixture="X2-opencli", verify=verify_x2,
         timeout=600, tools="read,bash",
         prompt="Use the ./bin/opencli tool (run './bin/opencli --help' first to learn it) to browse the site starting at http://shop.local/ and find the price of the 'Aurora Lamp' product. State the price clearly."),
    # real (真實已安裝的 agent-browser)
    dict(id="R1-agent-browser", tier="real", fixture=None, setup=None, verify=verify_r1,
         timeout=600, tools="read,bash",
         prompt="Use the 'agent-browser' command-line tool to open https://example.com and tell me the page title."),
]

DEFAULT_TIERS = ["smoke", "complex", "long", "cli", "real"]


# ---------------------------------------------------------------- 執行

def _sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def prepare_dir(task) -> Path:
    d = Path(tempfile.mkdtemp(prefix="pibench-"))
    fixture = task.get("fixture")
    if fixture:
        src = FIXTURES / fixture
        shutil.copytree(
            src, d, dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(".*", "__pycache__"),
        )
        bin_dir = d / "bin"
        if bin_dir.is_dir():
            for f in bin_dir.iterdir():
                f.chmod(f.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    elif task.get("setup"):
        task["setup"](d)
    return d


def _snapshot(d: Path):
    return {str(p.relative_to(d)): _sha(p) for p in d.rglob("*") if p.is_file()}


STATUS_MARK = {
    "PASS": "✅", "SILENT-PASS": "✅(silent)", "FAIL": "❌", "TIMEOUT": "⏰",
    "EMPTY-無痕": "⬜", "EMPTY-有動工": "⬜(有動工)", "TAMPERED": "🚫",
}


def run_once(harness, model, task):
    d = prepare_dir(task)
    try:
        protected = {name: _sha(d / name) for name in task.get("protected", [])}
        snap = _snapshot(d)

        cmd, extra_env = HARNESSES[harness]["build"](model, task["tools"], task["prompt"])
        env = {**os.environ, **extra_env}

        t0 = time.time()
        try:
            r = subprocess.run(cmd, cwd=d, capture_output=True, text=True,
                               timeout=task["timeout"], env=env)
            stdout, stderr, rc, timed_out = r.stdout, r.stderr or "", r.returncode, False
        except subprocess.TimeoutExpired as e:
            def _dec(x):
                return x.decode() if isinstance(x, bytes) else (x or "")
            stdout, stderr, rc, timed_out = _dec(e.stdout), _dec(e.stderr), None, True
        elapsed = round(time.time() - t0, 1)

        extract = HARNESSES[harness]["extract"]
        if extract:
            stdout = extract(stdout)

        err_note = f"exit={rc}, stderr尾: {stderr.strip()[-200:] or '無'}"
        tampered = [n for n, h in protected.items()
                    if not (d / n).exists() or _sha(d / n) != h]

        def run_verify():
            try:
                return task["verify"](d, stdout)
            except Exception as ex:
                return False, f"驗證出錯: {ex}"

        if timed_out:
            status, ok, detail = "TIMEOUT", False, f"逾時(>{task['timeout']}s); {err_note}"
        elif tampered:
            status, ok, detail = "TAMPERED", False, f"違規修改保護檔案: {', '.join(tampered)}"
        elif not stdout.strip():
            after = _snapshot(d)
            touched = [k for k in set(after) | set(snap) if after.get(k) != snap.get(k)]
            if not touched:
                status, ok, detail = "EMPTY-無痕", False, f"無輸出且完全沒動作; {err_note}"
            else:
                v_ok, v_detail = run_verify()
                if v_ok:
                    status, ok = "SILENT-PASS", True
                    detail = f"無文字輸出但實際完成任務 ({v_detail})"
                else:
                    status, ok = "EMPTY-有動工", False
                    detail = f"改了{len(touched)}個檔案但未完成 ({v_detail}); {err_note}"
        else:
            v_ok, v_detail = run_verify()
            status, ok, detail = ("PASS", True, v_detail) if v_ok else ("FAIL", False, v_detail)

        return dict(ok=ok, status=status, seconds=elapsed, detail=detail,
                    stdout=stdout.strip(), stderr=stderr.strip()[-500:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("models", nargs="+")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--tier", default=",".join(DEFAULT_TIERS),
                    help="逗號分隔: smoke,complex,long,cli,real")
    ap.add_argument("--harness", default="pi",
                    help="逗號分隔: " + ",".join(HARNESSES))
    args = ap.parse_args()

    tiers = [t.strip() for t in args.tier.split(",") if t.strip()]
    tasks = [t for t in TASKS if t["tier"] in tiers]
    if not tasks:
        sys.exit(f"沒有符合 tier {tiers} 的任務")
    harnesses = [h.strip() for h in args.harness.split(",") if h.strip()]
    unknown = [h for h in harnesses if h not in HARNESSES]
    if unknown:
        sys.exit(f"未知 harness: {', '.join(unknown)}(可用: {', '.join(HARNESSES)})")

    RESULTS_DIR.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")

    for harness, model in [(h, m) for h in harnesses for m in args.models]:
        tools_note = (not HARNESSES[harness]["tools_supported"]
                      and any(t["tools"] for t in tasks))
        print(f"\n{'=' * 64}\nharness: {harness}   模型: {model}   runs={args.runs}   tiers={','.join(tiers)}")
        if tools_note:
            print("⚠ 此 harness 不支援 per-run 工具限制, 各任務的 tools 欄位未生效")
        print("=" * 64)
        summary, all_runs = [], []
        for task in tasks:
            results = []
            for i in range(args.runs):
                print(f"  {task['id']} run {i + 1}/{args.runs} ...", end="", flush=True)
                res = run_once(harness, model, task)
                mark = STATUS_MARK[res["status"]]
                print(f" {mark} ({res['seconds']}s) {res['detail']}")
                results.append(res)
            passed = sum(r["ok"] for r in results)
            silent = sum(r["status"] == "SILENT-PASS" for r in results)
            empties = sum(r["status"].startswith("EMPTY") for r in results)
            avg = round(sum(r["seconds"] for r in results) / len(results), 1)
            summary.append(dict(task=task["id"], tier=task["tier"], passed=passed,
                                runs=args.runs, silent=silent, empties=empties, avg=avg))
            all_runs.append((task, results))

        print(f"\n{'任務':<20}{'通過':>8}{'靜默':>6}{'EMPTY':>8}{'平均秒':>8}")
        for s in summary:
            print(f"  {s['task']:<20}{s['passed']}/{s['runs']:>4}{s['silent']:>6}"
                  f"{s['empties']:>8}{s['avg']:>8}")
        total_p = sum(s["passed"] for s in summary)
        total_r = sum(s["runs"] for s in summary)
        print(f"\n  總計: {total_p}/{total_r} ({100 * total_p // total_r}%)")

        safe_model = model.replace(":", "_").replace("/", "_")
        report = RESULTS_DIR / f"{harness}_{safe_model}_{stamp}.md"
        lines = [f"# model-harness-eval: {model} × {harness}",
                 f"日期: {time.strftime('%Y-%m-%d %H:%M')}  harness={harness}  runs={args.runs}  tiers={','.join(tiers)}"]
        if tools_note:
            lines.append("\n> ⚠ 此 harness 不支援 per-run 工具限制, 各任務的 tools 欄位未生效。")
        lines += ["", "| 任務 | tier | 通過率 | 靜默通過 | EMPTY | 平均秒數 |",
                  "|---|---|---|---|---|---|"]
        for s in summary:
            lines.append(f"| {s['task']} | {s['tier']} | {s['passed']}/{s['runs']} "
                         f"| {s['silent']} | {s['empties']} | {s['avg']} |")
        lines.append(f"\n總計: **{total_p}/{total_r}**\n")
        for task, results in all_runs:
            lines.append(f"## {task['id']}\n")
            for i, r in enumerate(results, 1):
                lines.append(f"### run {i} — {r['status']} ({r['seconds']}s) — {r['detail']}\n")
                lines.append(f"```\n{r['stdout'] or '(無輸出)'}\n```\n")
                if r["stderr"]:
                    lines.append(f"stderr:\n```\n{r['stderr']}\n```\n")
        report.write_text("\n".join(lines))
        print(f"  報告: {report}")


if __name__ == "__main__":
    main()
