import re
import subprocess
import sys
from pathlib import Path

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
