# model-harness-eval

模型 × coding agent harness × provider 的能力評估框架。這個 repo 用可重複、可驗證的任務回答一個問題：同一個模型搭配不同 harness 時，實際能完成到哪一級 coding agent 任務。

核心原則是不信模型自述完成；每個 task 都用程式化 verifier 檢查結果，例如跑 pytest、執行產出的程式、比對檔案與 stdout。每題可跑多輪，用通過率與 EMPTY 次數觀察穩定性。

## 支援矩陣

| 類別 | 選項 |
|---|---|
| Harness | `pi`, `opencode`, `copilot`, `codex` |
| Provider | `ollama`, `litellm` |
| Task tier | `smoke`, `complex`, `long`, `cli`, `real` |
| 報告輸出 | `results/<harness>_<provider>_<model>_<timestamp>.md` |

## Provider 用法

`--provider` 決定 runner 怎麼把同一個 model name 接到不同後端。支援值定義在 `bench/harnesses.py`：

| Provider | 用途 | 預設 endpoint | 需求 |
|---|---|---|---|
| `ollama` | 本機模型 | `http://localhost:11434` | Ollama 正在跑，模型已 pull/註冊到對應 harness |
| `litellm` | LiteLLM proxy，例如 AWS Bedrock | `http://localhost:4000` | `./litellm.sh start` 已啟動，API key 預設 `sk-1234` |

`--provider` 可接受逗號分隔清單；runner 會產生 `harness × provider × model` 矩陣：

```bash
uv run python run_bench.py gemma4:12b \
  --provider ollama,litellm \
  --harness pi,copilot \
  --tier smoke --runs 1
```

非預設 endpoint 用環境變數覆蓋：

```bash
export OLLAMA_BASE_URL=http://localhost:11434
export LITELLM_BASE_URL=http://localhost:4000
```

runner 對 provider 的實際映射：

| Harness | `--provider ollama` | `--provider litellm` |
|---|---|---|
| `pi` | `pi --provider ollama --model <model>` | `pi --provider litellm --model <model>`；需在 `~/.pi/agent/models.json` 有同名 provider |
| `opencode` | `opencode run --model ollama/<model>` | `opencode run --model litellm/<model>`；需在 `opencode.jsonc` 有同名 provider 與 `apiKey` |
| `copilot` | 注入 `COPILOT_PROVIDER_TYPE=openai`, `COPILOT_PROVIDER_BASE_URL=<OLLAMA_BASE_URL>/v1`, `COPILOT_MODEL=<model>` | 注入 `COPILOT_PROVIDER_TYPE=openai`, `COPILOT_PROVIDER_BASE_URL=<LITELLM_BASE_URL>/v1`, `COPILOT_PROVIDER_API_KEY=sk-1234`, `COPILOT_MODEL=<model>` |
| `codex` | `codex exec --oss --local-provider ollama -m <model>` | 注入 `OPENAI_BASE_URL=<LITELLM_BASE_URL>`, `OPENAI_API_KEY=sk-1234`，再跑 `codex exec -m <model>` |

當 provider 清單包含 `litellm` 時，runner 會先打 `LITELLM_BASE_URL/v1/models` 檢查 proxy；未啟動時可加 `--auto-start-litellm` 讓 runner 呼叫 `./litellm.sh start`。

## 專案結構

```text
model-harness-eval/
├── run_bench.py                 # 評測 CLI wrapper
├── bench/
│   ├── __init__.py              # 路徑常數
│   ├── harnesses.py             # harness/provider command builder
│   ├── runner.py                # 執行引擎、CLI、report 產生
│   └── tasks.py                 # task 定義、setup、verify 函式
├── tests/                       # verifier 自身的 pytest 測試
├── fixtures/                    # 複雜/CLI task 的起始專案
├── results/                     # benchmark Markdown 報告
├── litellm.sh                   # 本機 LiteLLM + PostgreSQL 管理腳本
├── setup_litellm_db.sh          # 建立 LiteLLM PostgreSQL database/user
├── litellm_config.yaml.example  # LiteLLM model routing 範本
└── README_LITELLM.md            # LiteLLM/harness 詳細設定筆記
```

## 快速開始

本 repo 的測試與 benchmark 指令以 `uv run` 為準。

```bash
# 安裝/同步 Python 依賴
uv sync

# 驗證 verifier 與 fixture 正解
uv run pytest
uv run pytest -v

# 完整評測：預設 provider=ollama, harness=pi, runs=5, tiers=all
uv run python run_bench.py gemma4:12b

# 短測：只跑 complex 和 cli，每題一輪
uv run python run_bench.py gemma4:12b --runs 1 --tier complex,cli

# harness 矩陣
uv run python run_bench.py gemma4:12b --harness pi,opencode,copilot,codex

# 只補跑指定 task（prefix 以逗號分隔）
uv run python run_bench.py gemma4:12b --runs 5 --task C2,C3,L1,X1

# 依 results/selection.json 重建彙總報告
uv run python -m bench.report --results results
```

## 隔離與恢復

正式 benchmark 預設使用 Git disposable worktree，不使用 container。runner 會先從 Git tree 建立 `/tmp/model-harness-worktree-*`，子程序在該 worktree 裡執行，結果寫回主 checkout 的 `results/`，結束後移除 worktree。

這個設計的重點：

- 主 checkout 的 `fixtures/` 不會被 agent 直接改到。
- benchmark 跑的是已提交版本，預設來源是 `HEAD`。
- 如果 benchmark 中斷，最多留下 `/tmp/model-harness-worktree-*`；主 checkout 不需要手動回復。
- 沒有 Docker/container 流程；LiteLLM/Ollama 仍使用目前文件描述的本機服務。

子程序開始 benchmark 前，仍會用 Git tree 初始化該 worktree 內的 `fixtures/`（預設 `--fixture-source HEAD`），再用 Git 歷史固定的 fixture blob fingerprint 驗證題目基線，並在每輪後確認 agent 沒有改到該 worktree 的來源 `fixtures/`。基線不符或來源遭修改時會立即中止，不會繼續產生可計分結果。

常用恢復與隔離命令：

```bash
# 只恢復/驗證主 checkout 的 fixtures，不跑模型
uv run python run_bench.py --doctor-fixtures

# 從指定 known-good commit 建 worktree 並初始化 fixtures
uv run python run_bench.py <model> \
  --worktree-source <commit> \
  --fixture-source <commit>

# 開發 runner 時才直接使用目前 checkout；正式 benchmark 不要加
uv run python run_bench.py <model> --no-worktree-isolation
```

正式 benchmark 前要先 commit runner 變更；因為預設 worktree 來源是 `HEAD`，未提交的 runner 修改不會進入 disposable worktree。

如果有中斷後殘留的 disposable worktree，可先查看：

```bash
git worktree list
```

`pyproject.toml` 也定義了 `run-bench` entry point；等價用法：

```bash
uv run run-bench gemma4:12b --runs 1 --tier smoke
```

首次跑 X1 officecli fixture 前，先產生素材：

```bash
uv run python fixtures/X1-officecli/.build.py
```

## LiteLLM 啟動 workflow

`--provider litellm` 會把 harness 接到 `http://localhost:4000` 的 OpenAI-compatible LiteLLM proxy。這是跑 Bedrock 或其他雲端模型的主要 workflow。

### 一次性準備

```bash
# 系統依賴
sudo apt install postgresql

# LiteLLM proxy CLI 必須在 PATH 上；若使用目前 Python 環境，可用：
uv pip install 'litellm[proxy]' prisma

# 建立實際設定檔，填入要路由的模型
cp litellm_config.yaml.example litellm_config.yaml

# 建立 PostgreSQL database/user
sudo bash setup_litellm_db.sh
```

`setup_litellm_db.sh` 會建立：

- database: `litellm`
- user: `litellm`
- password: `litellm_password`
- connection string: `postgresql://litellm:litellm_password@localhost:5432/litellm`

`litellm.sh` 支援用環境變數覆蓋 DB 設定：`LITELLM_DB_HOST`, `LITELLM_DB_PORT`, `LITELLM_DB_NAME`, `LITELLM_DB_USER`, `LITELLM_DB_PASSWORD`。

### 啟動與驗證

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-west-2

./litellm.sh start
./litellm.sh status
./litellm.sh test
./litellm.sh logs --tail 100
```

常用管理：

```bash
./litellm.sh restart
./litellm.sh stop
./litellm.sh db
./litellm.sh clean
```

runner 在偵測到 `--provider litellm` 時會檢查 proxy；也可以要求它自動呼叫 `./litellm.sh start`：

```bash
uv run python run_bench.py bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0 \
  --provider litellm --harness pi --tier smoke --runs 1 --auto-start-litellm
```

不要把私有金鑰或私有模型設定寫進 `litellm_config.yaml.example`；實際設定放在 gitignored 的 `litellm_config.yaml`。

## Harness 設定

runner 實際支援的 harness 在 `bench/harnesses.py`。`pi` 支援 per-run `tools` 限制；`opencode`, `copilot`, `codex` 沒有等價限制，報告會標記 tools 欄位未生效。

### pi

Ollama：

- 安裝 `pi` CLI。
- 在 `~/.pi/agent/models.json` 註冊 Ollama provider/model。
- runner 會執行：`pi --provider ollama --model <model> -p <prompt>`。

LiteLLM：

- LiteLLM proxy 啟動後，runner 會執行：`pi --provider litellm --model <model> -p <prompt>`。
- `litellm` 是 Pi 的自訂 provider，必須寫在 `~/.pi/agent/models.json`。

```json
{
  "providers": {
    "litellm": {
      "baseUrl": "http://localhost:4000/v1",
      "api": "openai-completions",
      "apiKey": "sk-1234",
      "models": [
        {
          "id": "bedrock/nvidia.nemotron-super-3-120b",
          "name": "Nemotron 120B (Bedrock)",
          "contextWindow": 128000,
          "maxTokens": 16384
        }
      ]
    }
  }
}
```

範例：

```bash
uv run python run_bench.py gemma4:12b --provider ollama --harness pi --tier smoke --runs 1
uv run python run_bench.py bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0 --provider litellm --harness pi --tier smoke --runs 1
```

### opencode

在 `~/.config/opencode/opencode.jsonc` 註冊 `ollama` 與 `litellm` provider。provider 名稱必須與 runner 使用的 prefix 一致，因為 runner 會用 `ollama/<model>` 或 `litellm/<model>`。

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": {
        "gemma4:12b": { "name": "gemma4:12b" }
      }
    },
    "litellm": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LiteLLM Proxy",
      "options": {
        "baseURL": "http://localhost:4000/v1",
        "apiKey": "sk-1234"
      },
      "models": {
        "bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0": {
          "name": "Claude Sonnet (Bedrock)"
        }
      }
    }
  }
}
```

範例：

```bash
uv run python run_bench.py gemma4:12b --provider ollama --harness opencode --tier smoke --runs 1
uv run python run_bench.py bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0 --provider litellm --harness opencode --tier smoke --runs 1
```

### copilot

安裝 `copilot` CLI。Copilot 的 BYOK 模式由 `COPILOT_PROVIDER_BASE_URL` 啟動，runner 會自行注入所需環境變數。

- Ollama：`COPILOT_PROVIDER_TYPE=openai`, `COPILOT_PROVIDER_BASE_URL=http://localhost:11434/v1`, `COPILOT_MODEL=<model>`
- LiteLLM：`COPILOT_PROVIDER_TYPE=openai`, `COPILOT_PROVIDER_BASE_URL=http://localhost:4000/v1`, `COPILOT_PROVIDER_API_KEY=sk-1234`, `COPILOT_MODEL=<model>`

範例：

```bash
uv run python run_bench.py gemma4:12b --provider ollama --harness copilot --tier smoke --runs 1
uv run python run_bench.py bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0 --provider litellm --harness copilot --tier smoke --runs 1
```

### codex

安裝 `codex` CLI。runner 目前用兩條路徑：

- Ollama: `codex exec --oss --local-provider ollama -m <model> --dangerously-bypass-approvals-and-sandbox <prompt>`
- LiteLLM: `OPENAI_BASE_URL=http://localhost:4000 OPENAI_API_KEY=sk-1234 codex exec -m <model> --dangerously-bypass-approvals-and-sandbox <prompt>`

若你也想在互動式 Codex 使用同一個 LiteLLM endpoint，可在 `~/.codex/config.toml` 加 provider：

```toml
[model_providers.litellm]
name = "LiteLLM Proxy"
base_url = "http://localhost:4000"
wire_api = "responses"
env_key = "OPENAI_API_KEY"
```

範例：

```bash
uv run python run_bench.py gemma4:12b --provider ollama --harness codex --tier smoke --runs 1
uv run python run_bench.py bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0 --provider litellm --harness codex --tier smoke --runs 1
```

## Benchmark 指令範例

```bash
# 單模型、單 harness
uv run python run_bench.py gemma4:12b --provider ollama --harness pi --tier smoke --runs 1

# 多模型比較
uv run python run_bench.py gemma4:12b qwen3.5:9b --provider ollama --harness pi --runs 3

# Harness × model 矩陣
uv run python run_bench.py gemma4:12b --provider ollama --harness pi,opencode,copilot,codex --runs 1

# LiteLLM / Bedrock
uv run python run_bench.py bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0 \
  --provider litellm --harness pi,opencode,copilot,codex --tier smoke --runs 1

# Provider × harness 矩陣
uv run python run_bench.py gemma4:12b \
  --provider ollama,litellm --harness pi,copilot --tier smoke --runs 1
```

非預設 endpoint 可用：

```bash
export OLLAMA_BASE_URL=http://localhost:11434
export LITELLM_BASE_URL=http://localhost:4000
```

## 任務清單

| Tier | 任務 | 驗證重點 |
|---|---|---|
| `smoke` | T1 程式理解 | 回答提到 `take` 與 `restock` |
| `smoke` | T2 修 bug | 修正 `calc.py` 後執行通過 |
| `smoke` | T3 寫檔案 | 建立 `fizzbuzz.py` 並輸出正確第 3/15 行 |
| `smoke` | T4 bash 查資料 | 正確數出 CSV data rows = 42 |
| `complex` | C1 跨檔 bug | 追到 `store.py` 根因，pytest 全綠 |
| `complex` | C2 重構保綠 | 抽出 `utils.py` 且 `a.py`/`b.py` 使用它 |
| `complex` | C3 誤導除錯 | 修 config 層，`load_config()["port"]` 必須是 int |
| `long` | L1 spec 建專案 | 依 `SPEC.md` 實作 todo CLI，pytest 全綠 |
| `cli` | X1 陌生 officecli | 用 `./bin/officecli` 轉檔並回答 45 words |
| `cli` | X2 陌生 opencli | 從首頁兩跳找到 Aurora Lamp 價格 149.50 |
| `real` | R1 agent-browser | 用真實 `agent-browser` 打開 example.com 並回報 title |

`bench/tasks.py` 是 task 定義的唯一來源；新增 task 時要同步新增 verifier 與測試。

## Runner 判定邏輯

每輪會：

1. 建立全新 tempdir。
2. 複製 fixture，排除點開頭檔案與 `__pycache__`。
3. 對 protected files 記 SHA-256。
4. 用指定 harness/provider/model 非互動執行 prompt。
5. 依序判定 `TIMEOUT`, `TAMPERED`, `EMPTY-*`, `SILENT-PASS`, `PASS`, `FAIL`。
6. 寫入終端摘要與 `results/*.md` 完整 run output。

EMPTY 不是一定完全沒做事：runner 會比對 tempdir 前後 snapshot。若 stdout 空但檔案有改且 verifier 通過，會記為 `SILENT-PASS`。

## 測試與新增任務

測試全部用 `uv run`：

```bash
uv run pytest
uv run pytest -v
```

測試策略是雙向驗證：

- 原始 fixture 必須 fail，證明題目真的有 bug 或缺口。
- 套用 `tests/conftest.py` 的 `fix_*` 正解後必須 pass，證明 verifier 不誤殺。

新增 task 流程：

1. 在 `bench/tasks.py` 加 `setup_*` 或 fixture，並加 `verify_*`。
2. 多檔案題目放在 `fixtures/<task-name>/`。
3. 在 `tests/conftest.py` 補 `fix_*`。
4. 在對應 `tests/test_verify_*.py` 補原始 fail / 正解 pass 測試。
5. 對不能被模型修改的檔案設定 `protected`。
6. 跑 `uv run pytest`。

## 故障排除

### LiteLLM 無法啟動

```bash
pg_isready
sudo systemctl status postgresql
PGPASSWORD=litellm_password psql -h localhost -U litellm -d litellm -c '\q'
./litellm.sh logs --tail 100
```

### LiteLLM API 不通

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-1234"
```

確認三個地方的 key 一致：

- `litellm_config.yaml` 的 `general_settings.master_key`
- harness 設定或環境變數
- runner 預設的 `sk-1234`

### Bedrock 模型無法呼叫

```bash
aws bedrock list-foundation-models --region us-west-2 | head
./litellm.sh status
./litellm.sh test
```

### Harness 工具限制不一致

只有 `pi` 實際套用 `tools` 欄位。`opencode`, `copilot`, `codex` 跑 T1/T4/X1/X2 時仍是全工具可用，報告會自動提示。

## 安全與 git hygiene

不要提交：

- `litellm_config.yaml`
- `.litellm.pid`
- `.litellm.log`
- `.env`
- 真實 AWS credential
- 暫存 workspace 或私有模型金鑰

產出的 benchmark 報告在 `results/`；是否提交取決於你是否要保留該次實驗結果。
