# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 這是什麼

評測「模型 × coding agent harness × provider」能力的框架。harness 可選 pi / opencode / copilot / codex；provider 可選 ollama（地端模型）或 litellm（透過 litellm proxy 接 AWS Bedrock 等雲端模型）。核心原則:不信模型的自我宣稱,每個任務都由程式化 verify 函式實際檢查(跑 pytest、執行產出、比對輸出),且每題跑多輪量化穩定性。

## 常用指令

```bash
# 跑測試,確認 fixtures 與 verify 函式本身可信
pytest

# 完整評測(11 任務 × 每題 5 輪, 預設 provider=ollama)
python3 run_bench.py gemma4:12b

# 多模型、控制輪數、只跑特定 tier
python3 run_bench.py gemma4:12b qwen3.5:9b --runs 1 --tier complex,cli

# 換 harness(預設 pi)、或跑 harness × model 矩陣
python3 run_bench.py gemma4:12b --harness pi,opencode,copilot,codex

# 用 litellm provider 測 Bedrock 模型(需先啟動 litellm proxy)
python3 run_bench.py bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0 --provider litellm --harness copilot

# harness × provider × model 完整矩陣
python3 run_bench.py gemma4:12b --provider ollama,litellm --harness pi,copilot
```

前置需求:`pi` CLI 已安裝且 `~/.pi/agent/models.json` 已註冊 Ollama 模型、`pytest` 可用。X1 素材需先產生一次:`python3 fixtures/X1-officecli/.build.py`(runner 複製 fixture 時排除點開頭檔案,模型看不到產生邏輯)。

litellm 前置需求:啟動 litellm proxy Docker（`docker run -d -p 4000:4000 -v $(pwd)/litellm_config.yaml:/app/config.yaml -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_REGION_NAME ghcr.io/berriai/litellm:main-latest --config /app/config.yaml`），並在 `~/.config/opencode/opencode.jsonc` 設定 litellm provider。

## 架構

`bench/` package 按職責拆分,`run_bench.py` 是瘦入口:

**bench/harnesses.py** — harness registry:
- 每個 harness 一個 build 函式 `(model, provider, tools, prompt) -> (cmd, extra_env)` + metadata(`tools_supported`、`extract`)。
- `PROVIDERS = ("ollama", "litellm")`,各 build 函式根據 provider 切換 CLI 參數與環境變數。`LITELLM_BASE_URL` 預設 `http://localhost:4000`。
- pi 用 `--tools` 限工具;opencode/copilot/codex 無對等機制(報告自動註記)。
- opencode 走 `--format json`,由 `extract_opencode_text()` 從 JSONL 事件流抽 type=text;copilot 用 BYOK 環境變數接地端 Ollama。
- **新增 harness 就是加一個 build 函式 + `HARNESSES` dict 條目**。

**bench/tasks.py** — 任務定義與驗證:
- `TASKS` list 定義全部 11 個任務:id、tier、fixture 或 inline `setup` 函式、`verify` 函式、timeout、`tools`、`protected`、prompt。
- 所有 `verify_*` 和 `setup_*` 函式在此。
- 驗證要防假解(參考 verify_c2 的三重檢查、verify_c3 的根因檢查)。

**bench/runner.py** — 執行引擎:
- `prepare_dir()` 建全新 tempdir → 記保護檔案 SHA-256 → 以 tempdir 為 cwd 用 harness 非互動模式執行 → 依序判定 TIMEOUT / TAMPERED / EMPTY / verify → 銷毀 tempdir。
- 判定優先序:保護檔案 SHA 變了直接 TAMPERED;stdout 為空但檔案有變動且 verify 通過 → SILENT-PASS。
- `main()` 含 CLI argparse（`--provider`、`--harness`、`--runs`、`--tier`）與報告產生,報告寫到 `results/<harness>_<provider>_<model>_<timestamp>.md`。

**tests/** — pytest 測試(取代舊 selftest.py):
- `conftest.py`:`copy_fixture` helper 與 `fix_*` 正解函式。
- `test_verify_complex.py`:C1/C2/C3 雙向檢查。
- `test_verify_long.py`:L1 雙向檢查。
- `test_verify_cli.py`:X1/X2 雙向檢查。
- 每個 fixture 任務驗證兩個方向:原始必須 FAIL(bug 真的存在)、套用正解必須 PASS(驗證不誤殺)。

**fixtures/** — 每個複雜任務的起始專案。慣例:點開頭檔案(如 `.build.py`)不會被複製給模型;`bin/` 下是自製 mock CLI(X1 officecli、X2 opencli)。

## 新增任務時

1. 在 `bench/tasks.py` 的 `TASKS` 加一筆;有多檔案就建 fixture 目錄,簡單任務用 inline setup 函式。
2. 寫對應 `verify_*`(同檔案)。
3. 若是 fixture 任務,在 `tests/conftest.py` 補 `fix_*` 正解,在對應 tier 的 test 檔補雙向測試,`pytest` 全綠後才能拿去評測模型。
4. 測試類檔案記得列入 `protected`。

## 已知限制(改 runner 前先看)

- runner 主要依 stdout 判定;EMPTY 的真正死因可能在 stderr(已記錄尾段但診斷仍不完整,計畫用 `pi --mode json` 抓事件流)。
- gemma4:12b 在 C1 有系統性 EMPTY(5/5),原因調查中,嫌疑是 `~/.pi/agent/models.json` 的重複條目。
- 詳見 README「已知限制與待辦」。
