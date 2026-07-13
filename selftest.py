#!/usr/bin/env python3
"""驗證 pi-bench fixtures 與 verify 函式本身可信：

對每個複雜任務 (1) 用原始碼跑 verify → 必須 FAIL
                (2) 套用人工正解再跑 verify → 必須 PASS
任何一項不符就 exit 1。
"""

import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from run_bench import (  # noqa: E402
    FIXTURES, verify_c1, verify_c2, verify_c3, verify_l1, verify_x1, verify_x2,
)

GOOD_TODO = '''\
import json
import sys
from pathlib import Path

DB = Path("todos.json")


def load():
    if DB.exists():
        return json.loads(DB.read_text())
    return {"next_id": 1, "items": []}


def save(data):
    DB.write_text(json.dumps(data))


def main():
    args = sys.argv[1:]
    data = load()
    if args[0] == "add":
        tid = data["next_id"]
        data["items"].append({"id": tid, "text": " ".join(args[1:]), "done": False})
        data["next_id"] = tid + 1
        save(data)
        print(f"added {tid}")
    elif args[0] == "list":
        if not data["items"]:
            print("no todos")
        for it in data["items"]:
            box = "[x]" if it["done"] else "[ ]"
            print(f"{it['id']} {box} {it['text']}")
    elif args[0] == "done":
        tid = int(args[1])
        for it in data["items"]:
            if it["id"] == tid:
                it["done"] = True
                save(data)
                print(f"done {tid}")
                return
        print("not found")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''


def copy_fixture(name):
    d = Path(tempfile.mkdtemp(prefix="selftest-"))
    shutil.copytree(FIXTURES / name, d, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".*", "__pycache__"))
    bin_dir = d / "bin"
    if bin_dir.is_dir():
        for f in bin_dir.iterdir():
            f.chmod(f.stat().st_mode | stat.S_IEXEC)
    return d


def check(label, got, want):
    ok = got[0] == want
    status = "OK " if ok else "!!!"
    print(f"  {status} {label}: 預期 {'PASS' if want else 'FAIL'}, "
          f"得到 {'PASS' if got[0] else 'FAIL'} — {got[1]}")
    return ok


def fix_c1(d):
    f = d / "store.py"
    f.write_text(f.read_text().replace("> qty", ">= qty"))


def fix_c2(d):
    (d / "utils.py").write_text(
        'def normalize_name(name):\n'
        '    return " ".join(name.strip().split()).title()\n')
    (d / "a.py").write_text(
        'from utils import normalize_name\n\n\n'
        'def register_user(users, name):\n'
        '    cleaned = normalize_name(name)\n'
        '    if cleaned in users:\n'
        '        raise ValueError(f"duplicate user: {cleaned}")\n'
        '    users.append(cleaned)\n'
        '    return cleaned\n')
    (d / "b.py").write_text(
        'from utils import normalize_name\n\n\n'
        'def format_badge(name):\n'
        '    return f"[{normalize_name(name)}]"\n')


def fix_c3(d):
    f = d / "config.py"
    f.write_text(f.read_text().replace(
        '"port": raw.get("port", 8000),',
        '"port": int(raw.get("port", 8000)),'))


def fix_l1(d):
    (d / "todo.py").write_text(GOOD_TODO)


def fix_x1(d):
    r = subprocess.run(
        ["./bin/officecli", "convert", "report.docx", "--format", "txt",
         "-o", "report.txt"],
        cwd=d, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"officecli convert 失敗: {r.stderr}")
    words = len((d / "report.txt").read_text().split())
    fix_x1.stdout = f"The document contains {words} words."


def fix_x2(d):
    for cmd in (["./bin/opencli", "open", "http://shop.local/"],
                ["./bin/opencli", "open", "http://shop.local/products"]):
        r = subprocess.run(cmd, cwd=d, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"opencli 失敗: {r.stderr}")
    r = subprocess.run(["./bin/opencli", "text", ".price"], cwd=d,
                       capture_output=True, text=True)
    prices = r.stdout.strip().splitlines()
    fix_x2.stdout = f"The Aurora Lamp costs {prices[1]}." if len(prices) > 1 else r.stdout


CASES = [
    ("C1-crossfile-bug", verify_c1, fix_c1, ""),
    ("C2-refactor-green", verify_c2, fix_c2, ""),
    ("C3-misleading-trace", verify_c3, fix_c3, ""),
    ("L1-todo-spec", verify_l1, fix_l1, ""),
    ("X1-officecli", verify_x1, fix_x1, None),
    ("X2-opencli", verify_x2, fix_x2, None),
]

all_ok = True
for name, verify, fix, raw_stdout in CASES:
    print(f"{name}:")
    # 1) 原始碼必須 FAIL
    d = copy_fixture(name)
    all_ok &= check("原始碼", verify(d, raw_stdout if raw_stdout is not None else ""), False)
    shutil.rmtree(d, ignore_errors=True)
    # 2) 正解必須 PASS
    d = copy_fixture(name)
    fix(d)
    stdout = getattr(fix, "stdout", raw_stdout or "")
    all_ok &= check("正解  ", verify(d, stdout), True)
    shutil.rmtree(d, ignore_errors=True)

print("\n自測結果:", "全部通過 ✅" if all_ok else "有問題 ❌")
sys.exit(0 if all_ok else 1)
