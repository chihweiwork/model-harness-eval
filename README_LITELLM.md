# LiteLLM + Harness 設定指南

本文檔說明如何設定 LiteLLM proxy 連接 AWS Bedrock，並配置各個 coding agent harness（pi、opencode、copilot、codex）使用它。

## 目錄

- [前置需求](#前置需求)
- [LiteLLM 設置](#litellm-設置)
- [Harness 配置](#harness-配置)
- [運行評測](#運行評測)
- [故障排除](#故障排除)

---

## 前置需求

### 1. PostgreSQL
```bash
# 安裝
sudo apt install postgresql

# 確認運行
pg_isready
```

### 2. Python 依賴
```bash
pip install 'litellm[proxy]' prisma

# 生成 Prisma client（在 LiteLLM 安裝目錄）
cd /path/to/miniconda3/lib/python3.12/site-packages/litellm/proxy
prisma generate
```

### 3. AWS Bedrock 憑證
```bash
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
export AWS_DEFAULT_REGION="us-west-2"
```

---

## LiteLLM 設置

### 步驟 1：創建數據庫（一次性）

```bash
sudo bash setup_litellm_db.sh
```

這會創建：
- 數據庫：`litellm`
- 用戶：`litellm` / 密碼：`litellm_password`

### 步驟 2：配置模型

編輯 `litellm_config.yaml`：

```yaml
model_list:
  - model_name: bedrock/nvidia.nemotron-super-3-120b
    litellm_params:
      model: bedrock/nvidia.nemotron-super-3-120b

  - model_name: bedrock/mistral.devstral-2-123b
    litellm_params:
      model: bedrock/mistral.devstral-2-123b

  # 更多模型...

litellm_settings:
  drop_params: true

general_settings:
  master_key: "sk-1234"
```

### 步驟 3：啟動 LiteLLM

```bash
./litellm.sh start
```

### 步驟 4：驗證

```bash
./litellm.sh status
./litellm.sh test
```

### LiteLLM 管理命令

| 命令 | 說明 |
|------|------|
| `./litellm.sh start` | 啟動 LiteLLM |
| `./litellm.sh stop` | 停止 LiteLLM |
| `./litellm.sh restart` | 重啟（修改 config 後） |
| `./litellm.sh status` | 查看運行狀態和模型列表 |
| `./litellm.sh test` | 測試 API 連通性 |
| `./litellm.sh logs -f` | 查看即時日誌 |
| `./litellm.sh db` | 連接到 PostgreSQL |
| `./litellm.sh clean` | 清理日誌（保留數據庫） |

---

## Harness 配置

所有 harness 都需要 LiteLLM 在 `http://localhost:4000` 運行。

### 1. Pi

配置文件：`~/.pi/agent/models.json`

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
        },
        {
          "id": "bedrock/mistral.devstral-2-123b",
          "name": "Devstral 123B (Bedrock)",
          "contextWindow": 128000,
          "maxTokens": 16384
        }
      ]
    }
  }
}
```

**使用 Ollama（本地模型）**：

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [
        {
          "id": "gemma4:12b",
          "name": "Gemma 4 12B",
          "contextWindow": 8192
        }
      ]
    }
  }
}
```

**運行評測**：
```bash
# LiteLLM (Bedrock)
python3 run_bench.py bedrock/nvidia.nemotron-super-3-120b \
  --provider litellm --harness pi --tier smoke --runs 1

# Ollama (本地)
python3 run_bench.py gemma4:12b \
  --provider ollama --harness pi --tier smoke --runs 1
```

---

### 2. OpenCode

配置文件：`~/.config/opencode/opencode.jsonc`

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "litellm": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LiteLLM Proxy",
      "options": {
        "baseURL": "http://localhost:4000/v1",
        "apiKey": "sk-1234"
      },
      "models": {
        "bedrock/nvidia.nemotron-super-3-120b": {
          "name": "Nemotron 120B (Bedrock)"
        },
        "bedrock/mistral.devstral-2-123b": {
          "name": "Devstral 123B (Bedrock)"
        }
      }
    },
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": {
        "baseURL": "http://localhost:11434/v1"
      },
      "models": {
        "gemma4:12b": { "name": "Gemma 4 12B" }
      }
    }
  }
}
```

**運行評測**：
```bash
# LiteLLM
python3 run_bench.py bedrock/nvidia.nemotron-super-3-120b \
  --provider litellm --harness opencode --tier smoke --runs 1

# Ollama
python3 run_bench.py gemma4:12b \
  --provider ollama --harness opencode --tier smoke --runs 1
```

---

### 3. Copilot

**使用環境變數**（推薦）：

```bash
# LiteLLM (Bedrock)
export COPILOT_PROVIDER_TYPE=openai
export COPILOT_PROVIDER_BASE_URL=http://localhost:4000/v1
export COPILOT_PROVIDER_API_KEY=sk-1234
export COPILOT_MODEL=bedrock/nvidia.nemotron-super-3-120b

# Ollama (本地)
export COPILOT_PROVIDER_TYPE=openai
export COPILOT_PROVIDER_BASE_URL=http://localhost:11434/v1
export COPILOT_PROVIDER_API_KEY=ollama
export COPILOT_MODEL=gemma4:12b
```

**運行評測**：
```bash
# LiteLLM
python3 run_bench.py bedrock/nvidia.nemotron-super-3-120b \
  --provider litellm --harness copilot --tier smoke --runs 1

# Ollama
python3 run_bench.py gemma4:12b \
  --provider ollama --harness copilot --tier smoke --runs 1
```

---

### 4. Codex

配置文件：`~/.codex/config.toml`

```toml
# LiteLLM provider
[model_providers.litellm]
name = "LiteLLM Proxy"
base_url = "http://localhost:4000"
wire_api = "responses"
env_key = "LITELLM_API_KEY"

# Ollama provider
[model_providers.ollama]
name = "Ollama Local"
base_url = "http://localhost:11434"
wire_api = "chat"
```

**設置 API key**：
```bash
export LITELLM_API_KEY="sk-1234"
```

**運行評測**：
```bash
# LiteLLM
python3 run_bench.py bedrock/nvidia.nemotron-super-3-120b \
  --provider litellm --harness codex --tier smoke --runs 1

# Ollama
python3 run_bench.py gemma4:12b \
  --provider ollama --harness codex --tier smoke --runs 1
```

---

## 運行評測

### 單一模型 × 單一 harness

```bash
python3 run_bench.py bedrock/nvidia.nemotron-super-3-120b \
  --provider litellm \
  --harness pi \
  --tier smoke \
  --runs 1
```

### 多模型測試

```bash
python3 run_bench.py \
  bedrock/nvidia.nemotron-super-3-120b \
  bedrock/mistral.devstral-2-123b \
  --provider litellm \
  --harness pi \
  --tier complex \
  --runs 3
```

### Harness 矩陣測試

```bash
python3 run_bench.py bedrock/nvidia.nemotron-super-3-120b \
  --provider litellm \
  --harness pi,opencode,copilot,codex \
  --tier smoke \
  --runs 1
```

### Provider 矩陣測試（Ollama + LiteLLM）

```bash
# 需要兩個模型都配置好
python3 run_bench.py gemma4:12b \
  --provider ollama,litellm \
  --harness pi \
  --tier smoke \
  --runs 1
```

### 完整矩陣（Harness × Provider × Model）

```bash
python3 run_bench.py \
  gemma4:12b \
  bedrock/nvidia.nemotron-super-3-120b \
  --provider ollama,litellm \
  --harness pi,opencode,copilot,codex \
  --tier complex \
  --runs 5
```

---

## 故障排除

### LiteLLM 無法啟動

**檢查 PostgreSQL**：
```bash
pg_isready
sudo systemctl status postgresql
```

**檢查數據庫連接**：
```bash
PGPASSWORD=litellm_password psql -h localhost -U litellm -d litellm -c '\q'
```

**查看日誌**：
```bash
./litellm.sh logs --tail 100
```

### Harness 認證失敗

**確認 LiteLLM 運行**：
```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-1234"
```

**確認 API key 一致**：
- `litellm_config.yaml` 中的 `master_key`
- Harness 配置中的 `apiKey` 或環境變數
- 預設都應該是 `sk-1234`

### 模型無法調用

**檢查 AWS 憑證**：
```bash
aws bedrock list-foundation-models --region us-west-2 | head
```

**檢查模型列表**：
```bash
./litellm.sh status
```

**測試特定模型**：
```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -d '{
    "model": "bedrock/nvidia.nemotron-super-3-120b",
    "messages": [{"role": "user", "content": "Hi"}],
    "max_tokens": 10
  }'
```

---

## 配置摘要

### Provider 對照表

| Provider | 用途 | Base URL | API Key | 數據庫 |
|----------|------|----------|---------|--------|
| **ollama** | 本地模型 | `http://localhost:11434` | `ollama` | 不需要 |
| **litellm** | 雲端模型 (Bedrock) | `http://localhost:4000` | `sk-1234` | PostgreSQL |

### Harness 配置文件位置

| Harness | 配置文件 | 支持 Provider |
|---------|---------|---------------|
| **pi** | `~/.pi/agent/models.json` | ollama, litellm |
| **opencode** | `~/.config/opencode/opencode.jsonc` | ollama, litellm |
| **copilot** | 環境變數 | ollama, litellm |
| **codex** | `~/.codex/config.toml` + 環境變數 | ollama, litellm |

---

## 快速啟動流程

### LiteLLM + Bedrock

```bash
# 1. 設置數據庫（一次性）
sudo bash setup_litellm_db.sh

# 2. 設置 AWS 憑證
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-west-2"

# 3. 啟動 LiteLLM
./litellm.sh start

# 4. 驗證
./litellm.sh test

# 5. 運行評測
python3 run_bench.py bedrock/nvidia.nemotron-super-3-120b \
  --provider litellm --harness pi --tier smoke --runs 1
```

### Ollama + 本地模型

```bash
# 1. 確認 Ollama 運行
ollama list

# 2. 拉取模型（如果需要）
ollama pull gemma4:12b

# 3. 運行評測
python3 run_bench.py gemma4:12b \
  --provider ollama --harness pi --tier smoke --runs 1
```
