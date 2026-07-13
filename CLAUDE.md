# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 這是什麼

評測「地端模型(Ollama)× coding agent harness」能力的框架,harness 可選 pi / opencode / GitHub Copilot CLI(三者都接地端模型)。核心原則:不信模型的自我宣稱,每個任務都由程式化 verify 函式實際檢查(跑 pytest、執行產出、比對輸出),且每題跑多輪量化穩定性。

## 常用指令

```bash
# 先跑自測,確認 fixtures 與 verify 函式本身可信(任何一項不符會 exit 1)
python3 selftest.py

# 完整評測(11 任務 × 每題 5 輪)
python3 run_bench.py gemma4:12b

# 多模型、控制輪數、只跑特定 tier
python3 run_bench.py gemma4:12b qwen3.5:9b --runs 1 --tier complex,cli

# 換 harness(預設 pi)、或跑 harness × model 矩陣
python3 run_bench.py gemma4:12b --harness pi,opencode,copilot
```

前置需求:`pi` CLI 已安裝且 `~/.pi/agent/models.json` 已註冊 Ollama 模型、`pytest` 可用。X1 素材需先產生一次:`python3 fixtures/X1-officecli/.build.py`(runner 複製 fixture 時排除點開頭檔案,模型看不到產生邏輯)。

沒有獨立的 lint/test 設定;`selftest.py` 就是這個 repo 的測試。

## 架構

兩個 Python 檔案,無外部依賴(標準庫 + pytest):

**run_bench.py** — 一切的中心:
- `HARNESSES` registry:每個 harness 一個 build 函式 `(model, tools, prompt) -> (cmd, extra_env)` + metadata(`tools_supported`、`extract`)。pi 用 `--tools` 限工具;opencode/copilot 無對等機制(報告自動註記)。opencode 走 `--format json`,由 `extract_opencode_text()` 從 JSONL 事件流抽 type=text 作為模型輸出;copilot 用 BYOK 環境變數(`COPILOT_PROVIDER_BASE_URL`)接地端 Ollama。**新增 harness 就是加一個 build 函式 + registry 條目**。
- `TASKS` list 定義全部 11 個任務:id、tier、fixture 或 inline `setup` 函式、`verify` 函式、timeout、`tools`(工具限制)、`protected`(禁改檔案)、prompt。
- 每輪流程 `run_once(harness, model, task)`:建全新 tempdir(fixture 複製時排除 `.` 開頭檔案與 `__pycache__`,`bin/` 自動 chmod +x)→ 記保護檔案 SHA-256 → 以 tempdir 為 cwd 用 harness 非互動模式執行 → 依序判定 TIMEOUT / TAMPERED / EMPTY / verify → 銷毀 tempdir。
- 判定有優先序:保護檔案 SHA 變了直接 TAMPERED(防「把測試改到會過」);stdout 為空但檔案有變動且 verify 通過 → SILENT-PASS(仍算過)。
- 報告寫到 `results/<model>_<timestamp>.md`,含每輪完整模型輸出。

**selftest.py** — 評測的可信度契約,對每個複雜任務做雙向檢查:
1. 原始 fixture 直接跑 verify → 必須 FAIL(bug 真的存在、驗證不放水)
2. 套用 `fix_*` 人工正解再跑 verify → 必須 PASS(驗證不誤殺正解;X1/X2 的正解是真的去執行 mock CLI)

**fixtures/** — 每個複雜任務的起始專案。慣例:點開頭檔案(如 `.build.py`)不會被複製給模型;`bin/` 下是自製 mock CLI(X1 officecli、X2 opencli)。

## 新增任務時

1. 在 `TASKS` 加一筆;有多檔案就建 fixture 目錄,簡單任務用 inline setup 函式。
2. 寫對應 `verify_*`;驗證要防假解(參考 verify_c2 的三重檢查、verify_c3 的根因檢查——治標繃帶會被抓出來)。
3. 若是 fixture 任務,在 `selftest.py` 的 `CASES` 補上 `fix_*` 正解,並確認 `python3 selftest.py` 全綠後才能拿去評測模型。
4. 測試類檔案記得列入 `protected`。

## 已知限制(改 runner 前先看)

- runner 主要依 stdout 判定;EMPTY 的真正死因可能在 stderr(已記錄尾段但診斷仍不完整,計畫用 `pi --mode json` 抓事件流)。
- gemma4:12b 在 C1 有系統性 EMPTY(5/5),原因調查中,嫌疑是 `~/.pi/agent/models.json` 的重複條目。
- 詳見 README「已知限制與待辦」。
