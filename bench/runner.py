#!/usr/bin/env python3
"""harness × 地端模型評測 runner

用法:
    python3 run_bench.py gemma4:12b                          # 全部 tier, 每題 5 次, harness=pi
    python3 run_bench.py gemma4:12b qwen3.5:9b --runs 3
    python3 run_bench.py gemma4:12b --tier complex,cli --runs 1
    python3 run_bench.py gemma4:12b --harness opencode
    python3 run_bench.py gemma4:12b --harness pi,opencode,copilot   # harness × model 矩陣
"""

import argparse
import hashlib
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

from bench import FIXTURES, RESULTS_DIR, ROOT
from bench.fixture_baseline import (
    BASELINE_COMMIT,
    FixtureBaselineError,
    assert_fixture_tree_unchanged,
    reset_fixture_tree,
    snapshot_fixture_tree,
    validate_fixture_baseline,
)
from bench.harnesses import HARNESSES, PROVIDERS, LITELLM_BASE_URL
from bench.tasks import TASKS, DEFAULT_TIERS


WORKTREE_CHILD_ENV = "BENCH_WORKTREE_CHILD"


def _sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _run_git(args, cwd=ROOT):
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def run_in_disposable_worktree(args):
    worktree = Path(tempfile.mkdtemp(prefix="model-harness-worktree-"))
    shutil.rmtree(worktree)
    _run_git(["worktree", "add", "--detach", str(worktree), args.worktree_source])
    env = {
        **os.environ,
        WORKTREE_CHILD_ENV: "1",
        "BENCH_RESULTS_DIR": str(RESULTS_DIR),
    }
    cmd = [sys.executable, "run_bench.py", *sys.argv[1:], "--no-worktree-isolation"]
    try:
        return subprocess.run(cmd, cwd=worktree, env=env).returncode
    finally:
        removed = subprocess.run(
            ["git", "worktree", "remove", "--force", str(worktree)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if removed.returncode:
            print(
                f"warning: failed to remove worktree {worktree}: "
                f"{removed.stderr.strip() or removed.stdout.strip()}",
                file=sys.stderr,
            )


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


def run_once(harness, provider, model, task):
    d = prepare_dir(task)
    source_before = snapshot_fixture_tree(FIXTURES)
    try:
        protected = {name: _sha(d / name) for name in task.get("protected", [])}
        snap = _snapshot(d)

        cmd, extra_env = HARNESSES[harness]["build"](
            model, provider, task["tools"], task["prompt"], d
        )
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
        try:
            assert_fixture_tree_unchanged(FIXTURES, source_before)
        finally:
            shutil.rmtree(d, ignore_errors=True)


def select_tasks(tiers, requested=None):
    """Select tasks by tier and optional stable task prefixes such as C2,L1."""
    tasks = [task for task in TASKS if task["tier"] in tiers]
    if not requested:
        return tasks
    prefixes = [value.strip().upper() for value in requested.split(",") if value.strip()]
    by_prefix = {task["id"].split("-", 1)[0].upper(): task for task in tasks}
    unknown = [prefix for prefix in prefixes if prefix not in by_prefix]
    if unknown:
        available = ",".join(by_prefix)
        raise ValueError(
            f"未知 task: {', '.join(unknown)}（目前 tier 可用: {available}）"
        )
    return [by_prefix[prefix] for prefix in prefixes]


def check_litellm_running():
    """檢查 LiteLLM proxy 是否運行"""
    try:
        from urllib.request import Request
        # 使用 /v1/models 更快，不會測試所有模型
        req = Request(f"{LITELLM_BASE_URL}/v1/models")
        req.add_header("Authorization", "Bearer sk-1234")
        with urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except (URLError, Exception):
        return False


def ensure_litellm(auto_start=False):
    """確保 LiteLLM proxy 運行（如果需要）"""
    if check_litellm_running():
        return True

    if not auto_start:
        print(f"\n❌ Error: LiteLLM proxy not running at {LITELLM_BASE_URL}", file=sys.stderr)
        print(f"→ Start with: ./litellm.sh start", file=sys.stderr)
        print(f"→ Or use --auto-start-litellm flag", file=sys.stderr)
        sys.exit(1)

    # 自動啟動
    print(f"→ Starting LiteLLM proxy...")
    script = Path(__file__).parent.parent / "litellm.sh"
    if not script.exists():
        print(f"❌ Error: {script} not found", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run([str(script), "start"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to start LiteLLM:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    print("✓ LiteLLM started")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("models", nargs="*")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--tier", default=",".join(DEFAULT_TIERS),
                    help="逗號分隔: smoke,complex,long,cli,real")
    ap.add_argument("--task", default=None,
                    help="只跑指定 task prefix，例如 C2,C3,L1,X1")
    ap.add_argument("--harness", default="pi",
                    help="逗號分隔: " + ",".join(HARNESSES))
    ap.add_argument("--provider", default="ollama",
                    help="逗號分隔: " + ",".join(PROVIDERS))
    ap.add_argument("--auto-start-litellm", action="store_true",
                    help="自動啟動 LiteLLM proxy（如果未運行）")
    ap.add_argument("--fixture-source", default="HEAD",
                    help="每次跑前用這個 Git commit/tree 初始化 fixtures")
    ap.add_argument("--no-reset-fixtures", action="store_true",
                    help="不要在 benchmark 前自動從 Git tree 還原 fixtures")
    ap.add_argument("--doctor-fixtures", action="store_true",
                    help="只從 Git tree 還原 fixtures 並驗證，不執行 benchmark")
    ap.add_argument("--worktree-source", default="HEAD",
                    help="每次 benchmark 用這個 Git commit/tree 建立 disposable worktree")
    ap.add_argument("--no-worktree-isolation", action="store_true",
                    help="不要建立 disposable worktree；直接在目前 checkout 執行")
    args = ap.parse_args()

    if args.doctor_fixtures:
        try:
            changed = reset_fixture_tree(FIXTURES, args.fixture_source)
            fingerprint = validate_fixture_baseline(FIXTURES)
        except FixtureBaselineError as exc:
            sys.exit(str(exc))
        if changed:
            print("restored fixtures:")
            for relative in changed:
                print(f"  {relative}")
        else:
            print("fixtures already clean")
        print(f"baseline_commit={BASELINE_COMMIT}")
        print(f"baseline_fingerprint={fingerprint}")
        return
    if not args.models:
        ap.error("需要至少一個 model，或使用 --doctor-fixtures")
    if not args.no_worktree_isolation and not os.environ.get(WORKTREE_CHILD_ENV):
        sys.exit(run_in_disposable_worktree(args))

    tiers = [t.strip() for t in args.tier.split(",") if t.strip()]
    try:
        tasks = select_tasks(tiers, args.task)
    except ValueError as exc:
        ap.error(str(exc))
    if not tasks:
        sys.exit(f"沒有符合 tier {tiers} 的任務")
    harnesses = [h.strip() for h in args.harness.split(",") if h.strip()]
    unknown = [h for h in harnesses if h not in HARNESSES]
    if unknown:
        sys.exit(f"未知 harness: {', '.join(unknown)}（可用: {', '.join(HARNESSES)}）")
    providers = [p.strip() for p in args.provider.split(",") if p.strip()]
    unknown_p = [p for p in providers if p not in PROVIDERS]
    if unknown_p:
        sys.exit(f"未知 provider: {', '.join(unknown_p)}（可用: {', '.join(PROVIDERS)}）")

    if not args.no_reset_fixtures:
        reset_fixture_tree(FIXTURES, args.fixture_source)
    baseline_fingerprint = validate_fixture_baseline(FIXTURES)

    # 檢查 LiteLLM 是否需要運行
    if "litellm" in providers:
        ensure_litellm(auto_start=args.auto_start_litellm)

    RESULTS_DIR.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")

    for harness, provider, model in [(h, p, m) for h in harnesses for p in providers for m in args.models]:
        tools_note = (not HARNESSES[harness]["tools_supported"]
                      and any(t["tools"] for t in tasks))
        print(f"\n{'=' * 64}\nharness: {harness}   provider: {provider}   模型: {model}   runs={args.runs}   tiers={','.join(tiers)}")
        if tools_note:
            print("⚠ 此 harness 不支援 per-run 工具限制, 各任務的 tools 欄位未生效")
        print("=" * 64)
        summary, all_runs = [], []
        for task in tasks:
            results = []
            for i in range(args.runs):
                print(f"  {task['id']} run {i + 1}/{args.runs} ...", end="", flush=True)
                res = run_once(harness, provider, model, task)
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
        report = RESULTS_DIR / f"{harness}_{provider}_{safe_model}_{stamp}.md"
        lines = [f"# model-harness-eval: {model} × {harness} × {provider}",
                 f"日期: {time.strftime('%Y-%m-%d %H:%M')}  harness={harness}  provider={provider}  runs={args.runs}  tiers={','.join(tiers)}",
                 ("benchmark_schema=2  isolation=verified  "
                  f"baseline_commit={BASELINE_COMMIT}  "
                  f"baseline_fingerprint={baseline_fingerprint}  "
                  f"tasks={','.join(t['id'].split('-', 1)[0] for t in tasks)}")]
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
