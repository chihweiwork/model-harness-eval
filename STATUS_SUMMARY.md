# 當前設定狀態

## ✅ 已完成

### 1. LiteLLM 基礎設施
- [x] `litellm.sh` - 管理腳本（start/stop/restart/status/test/db/logs/clean）
- [x] `setup_litellm_db.sh` - PostgreSQL 數據庫設置腳本
- [x] `litellm_config.yaml` - 模型配置（4個 Bedrock 模型）
- [x] PostgreSQL 集成和健康檢查
- [x] Prisma client 生成完成

### 2. Harness 配置方式已記錄
- [x] Pi: `~/.pi/agent/models.json`
- [x] OpenCode: `~/.config/opencode/opencode.jsonc`
- [x] Copilot: 環境變數方式
- [x] Codex: `~/.codex/config.toml` + 環境變數

### 3. 文檔
- [x] `README_LITELLM.md` - 完整設定指南
- [x] `STATUS_SUMMARY.md` - 當前狀態總結（本文件）

## 🎯 下一步操作

### 1. 創建數據庫（一次性）
```bash
sudo bash setup_litellm_db.sh
```

### 2. 啟動 LiteLLM
```bash
./litellm.sh start
```

### 3. 驗證運行
```bash
./litellm.sh status
./litellm.sh test
```

### 4. 運行第一個評測
```bash
python3 run_bench.py bedrock/nvidia.nemotron-super-3-120b \
  --provider litellm --harness pi --tier smoke --runs 1
```

## 📋 配置確認清單

- [ ] PostgreSQL 已安裝並運行（`pg_isready`）
- [ ] 數據庫 `litellm` 已創建（`sudo bash setup_litellm_db.sh`）
- [ ] AWS 環境變數已設置（`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`）
- [ ] Prisma client 已生成（已完成）
- [ ] LiteLLM 能成功啟動（`./litellm.sh start`）
- [ ] API 測試通過（`./litellm.sh test`）
- [ ] Harness 配置已更新（根據 README_LITELLM.md）

## 🔧 當前配置的模型

從 `litellm_config.yaml`：
1. `bedrock/nvidia.nemotron-super-3-120b` - NVIDIA Nemotron 120B
2. `bedrock/mistral.devstral-2-123b` - Mistral Devstral 123B (Coding專用)
3. `bedrock/us.meta.llama4-maverick-17b-instruct-v1:0` - Llama 4 Maverick 17B
4. `bedrock/google.gemma-3-27b-it` - Google Gemma 3 27B

## 📁 關鍵文件

```
.
├── litellm.sh                  # LiteLLM 管理腳本
├── setup_litellm_db.sh         # 數據庫設置腳本
├── litellm_config.yaml         # 模型配置
├── README_LITELLM.md           # 完整設定指南
├── STATUS_SUMMARY.md           # 當前狀態（本文件）
├── bench/
│   ├── harnesses.py           # Harness 構建邏輯
│   ├── runner.py              # 評測執行引擎
│   └── tasks.py               # 任務定義
├── run_bench.py               # 評測入口
└── .litellm.pid/.litellm.log  # 運行時文件（gitignored）
```

## ⚠️ 重要提醒

1. **數據庫必須先創建**：`sudo bash setup_litellm_db.sh`
2. **AWS 憑證必須設置**：LiteLLM 需要訪問 Bedrock
3. **API Key 一致性**：所有 harness 配置的 API key 都應該是 `sk-1234`
4. **LiteLLM 必須運行**：評測前確認 `./litellm.sh status` 顯示運行中

## 🐛 已知限制

1. **LiteLLM 不支持 SQLite**：必須使用 PostgreSQL
2. **Prisma schema 硬編碼**：只支持 PostgreSQL provider
3. **需要數據庫**：即使不需要多用戶，LiteLLM 也要求有數據庫存儲 API keys

## 📞 支援

遇到問題時：
1. 查看 `README_LITELLM.md` 的故障排除章節
2. 檢查 LiteLLM 日誌：`./litellm.sh logs --tail 100`
3. 測試數據庫連接：`./litellm.sh db`
4. 測試 API：`./litellm.sh test`
