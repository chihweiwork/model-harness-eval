# model-harness-eval: bedrock/us.meta.llama4-maverick-17b-instruct-v1:0 × copilot × litellm
日期: 2026-07-14 18:11  harness=copilot  provider=litellm  runs=5  tiers=smoke,complex,long,cli,real

> ⚠ 此 harness 不支援 per-run 工具限制, 各任務的 tools 欄位未生效。

| 任務 | tier | 通過率 | 靜默通過 | EMPTY | 平均秒數 |
|---|---|---|---|---|---|
| T1-程式理解 | smoke | 0/5 | 0 | 5 | 1.1 |
| T2-修bug | smoke | 0/5 | 0 | 5 | 1.1 |
| T3-寫檔案 | smoke | 0/5 | 0 | 5 | 1.1 |
| T4-bash查資料 | smoke | 0/5 | 0 | 5 | 1.1 |
| C1-跨檔bug | complex | 0/5 | 0 | 5 | 1.1 |
| C2-重構保綠 | complex | 0/5 | 0 | 5 | 1.0 |
| C3-誤導除錯 | complex | 0/5 | 0 | 5 | 1.1 |
| L1-spec建專案 | long | 0/5 | 0 | 5 | 1.1 |
| X1-陌生officecli | cli | 0/5 | 0 | 5 | 1.1 |
| X2-陌生opencli | cli | 0/5 | 0 | 5 | 1.0 |
| R1-agent-browser | real | 0/5 | 0 | 5 | 1.1 |

總計: **0/55**

## T1-程式理解

### run 1 — EMPTY-無痕 (1.2s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

## T2-修bug

### run 1 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

## T3-寫檔案

### run 1 — EMPTY-無痕 (1.4s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

## T4-bash查資料

### run 1 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

## C1-跨檔bug

### run 1 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

## C2-重構保綠

### run 1 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

## C3-誤導除錯

### run 1 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

## L1-spec建專案

### run 1 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

## X1-陌生officecli

### run 1 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

## X2-陌生opencli

### run 1 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

## R1-agent-browser

### run 1 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 2 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 3 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 4 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```

### run 5 — EMPTY-無痕 (1.1s) — 無輸出且完全沒動作; exit=1, stderr尾: or: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None

```
(無輸出)
```

stderr:
```
400 litellm.BadRequestError: BedrockException - {"message":"This model doesn't support tool use in streaming mode."}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0
Available Model Group Fallbacks=None
```
